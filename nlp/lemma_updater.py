# -*- coding: utf-8 -*-
"""
Lemma Updater Module

This module uses Stanza to update lemma information in the corpus database.
It iterates through all sentences, processes them with Stanza, and updates
the lemma for each token.
"""

import sqlite3
import stanza
import logging
import torch
from typing import Callable, Optional, List, Dict, Union, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import transformers
TRANSFORMERS_AVAILABLE = False
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("Transformers library not available for BERTLemmatizer")

class BERTLemmatizer:
    """
    Wrapper for LiProject/BERT-Turkish-Lemmatization-V3 model.
    Handles sentence-level input by processing tokens individually or in context.
    """
    
    def __init__(self, model_path: str = "LiProject/BERT-Turkish-Lemmatization-V3"):
        """
        Initialize the lemmatizer.
        
        Args:
            model_path: Hugging Face model path.
        """
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self.is_loaded = False
        
        if TRANSFORMERS_AVAILABLE:
            self._load_model()
        else:
            logger.error("Transformers library is required for BERTLemmatizer")

    def _load_model(self):
        """Load the model and tokenizer from Hugging Face."""
        try:
            logger.info(f"Loading BERT Lemmatization model: {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)
            
            self.pipeline = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
            self.is_loaded = True
            logger.info("BERT Lemmatization model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load BERT Lemmatization model: {e}")
            self.is_loaded = False

    def lemmatize_word(self, word: str, context: Optional[str] = None) -> str:
        """
        Lemmatize a single word, optionally with context.
        """
        if not self.is_loaded:
            return word.lower()
            
        try:
            if context:
                input_text = f"word: {word} sentence: {context}"
            else:
                input_text = f"word: {word} sentence: {word}"
                
            results = self.pipeline(input_text, max_length=50, num_beams=5)
            if results and 'generated_text' in results[0]:
                return results[0]['generated_text'].strip()
            return word.lower()
        except Exception as e:
            logger.error(f"Error lemmatizing word '{word}': {e}")
            return word.lower()

    def lemmatize_batch(self, words_with_contexts: List[Dict[str, str]]) -> List[str]:
        """
        Lemmatize a batch of words for better performance.
        """
        if not self.is_loaded or not words_with_contexts:
            return [item['word'].lower() for item in words_with_contexts]
            
        try:
            # Saf kelimeleri gönderiyoruz (prefix yok)
            input_texts = [item['word'] for item in words_with_contexts]
                
            # Senin betiğinle aynı parametreler
            # En yüksek doğruluk ve temiz çıktı için altın standart konfigürasyon
            results = self.pipeline(
                input_texts,
                max_new_tokens=256,
                num_beams=6,
                do_sample=False,
                early_stopping=True,
                length_penalty=0.7,
                repetition_penalty=1.1,
                no_repeat_ngram_size=2,
                batch_size=8
            )
            
            lemmas = []
            for res in results:
                lemma = res['generated_text'].strip()
                # Model ne diyorsa onu alıyoruz
                lemmas.append(lemma if lemma else None)
                
            return lemmas
        except Exception as e:
            logger.error(f"Error in batch lemmatization: {e}")
            return [item['word'].lower() for item in words_with_contexts]

def create_bert_lemmatizer(model_path: str = "LiProject/BERT-Turkish-Lemmatization-V3") -> BERTLemmatizer:
    """Factory function for BERTLemmatizer."""
    return BERTLemmatizer(model_path)

class BERTLemmaUpdater:
    """
    Updates the lemma information in the database using LiProject/BERT-Turkish-Lemmatization-V3.
    """
    def __init__(self, db_path: str, progress_callback: Optional[Callable] = None):
        """
        Initializes the updater.

        Args:
            db_path: Path to the SQLite database.
            progress_callback: A function to call with progress updates (e.g., percentage).
        """
        self.db_path = db_path
        self.conn = None
        self.progress_callback = progress_callback
        
        # Initialize the BERT lemmatizer
        try:
            self.lemmatizer = create_bert_lemmatizer()
            if not self.lemmatizer.is_loaded:
                raise RuntimeError("BERT lemmatizer model could not be loaded.")
        except Exception as e:
            logger.error(f"BERT lemmatizer başlatılamadı: {e}")
            raise

    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def update_all_lemmas(self, batch_size: int = 200):
        """
        Updates the 'lemma' column for existing tokens non-destructively.
        Commits changes in batches.
        """
        self.connect()
        if not self.conn:
            logger.error("Veritabanı bağlantısı kurulamadı.")
            return

        cursor = self.conn.cursor()
        
        try:
            # 1. Get all sentences from the database
            cursor.execute("SELECT sent_id, sent_text FROM sentences ORDER BY sent_id")
            sentences = cursor.fetchall()
            total_sentences = len(sentences)
            logger.info(f"Toplam {total_sentences} cümledeki lemmalar BERT ile güncellenecek...")

            if self.progress_callback:
                self.progress_callback(0, "BERT ile lemma güncelleme başlıyor...")

            updates_to_perform = []

            # 2. Process each sentence
            for i, sent_row in enumerate(sentences):
                sent_id = sent_row['sent_id']
                sent_text = sent_row['sent_text']
                
                cursor.execute("SELECT token_id, word FROM tokens WHERE sent_id = ? ORDER BY token_number", (sent_id,))
                db_tokens = cursor.fetchall()

                if not db_tokens:
                    continue

                # Prepare words for batch lemmatization
                words_to_lemmatize = []
                token_ids = []
                for t in db_tokens:
                    words_to_lemmatize.append({'word': t['word'], 'context': sent_text})
                    token_ids.append(t['token_id'])
                
                # Perform batch lemmatization
                lemmas = self.lemmatizer.lemmatize_batch(words_to_lemmatize)
                
                for lemma, token_id in zip(lemmas, token_ids):
                    if lemma:
                        updates_to_perform.append((lemma, token_id))
                
                # 3. Commit batch if size is reached
                if (i + 1) % batch_size == 0:
                    if updates_to_perform:
                        logger.info(f"Cümle #{i+1}: {len(updates_to_perform)} güncelleme kaydediliyor...")
                        cursor.executemany("UPDATE tokens SET lemma = ? WHERE token_id = ?", updates_to_perform)
                        self.conn.commit()
                        updates_to_perform = [] # Reset batch
                    
                    if self.progress_callback:
                        progress = (i + 1) / total_sentences * 100
                        self.progress_callback(progress, f"{i+1}/{total_sentences} cümle işlendi (kaydedildi)...")

            # 4. Commit any remaining updates after the loop
            if updates_to_perform:
                logger.info(f"Kalan {len(updates_to_perform)} güncelleme kaydediliyor...")
                cursor.executemany("UPDATE tokens SET lemma = ? WHERE token_id = ?", updates_to_perform)
                self.conn.commit()

            if self.progress_callback:
                self.progress_callback(100, "İşlem tamamlandı!")

        except Exception as e:
            logger.error(f"Lemma güncelleme sırasında hata: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        finally:
            self.close()

class StanzaLemmaUpdater:
    """
    Updates the lemma information in the database using Stanza.
    """
    def __init__(self, db_path: str, progress_callback: Optional[Callable] = None):
        """
        Initializes the updater.

        Args:
            db_path: Path to the SQLite database.
            progress_callback: A function to call with progress updates (e.g., percentage).
        """
        self.db_path = db_path
        self.conn = None
        self.progress_callback = progress_callback
        
        # Download and initialize the Stanza pipeline for Turkish
        try:
            stanza.download('tr', verbose=False)
            self.nlp = stanza.Pipeline('tr', verbose=False, processors='tokenize,lemma')
        except Exception as e:
            logger.error(f"Stanza pipeline başlatılamadı: {e}")
            raise

    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def update_all_lemmas(self):
        """
        Updates the 'lemma' column for existing tokens non-destructively.
        Commits changes in batches every 200 sentences.
        """
        self.connect()
        if not self.conn:
            logger.error("Veritabanı bağlantısı kurulamadı.")
            return

        cursor = self.conn.cursor()
        
        try:
            # 1. Get all sentences from the database
            cursor.execute("SELECT sent_id, sent_text FROM sentences ORDER BY sent_id")
            sentences = cursor.fetchall()
            total_sentences = len(sentences)
            logger.info(f"Toplam {total_sentences} cümledeki lemmalar güncellenecek...")

            if self.progress_callback:
                self.progress_callback(0, "Stanza ile lemma güncelleme başlıyor...")

            updates_to_perform = []
            commit_batch_size = 200  # Her 200 cümlede bir kaydet

            # 2. Process each sentence
            for i, sent_row in enumerate(sentences):
                sent_id = sent_row['sent_id']
                sent_text = sent_row['sent_text']
                
                cursor.execute("SELECT token_id, start_char, end_char FROM tokens WHERE sent_id = ?", (sent_id,))
                db_tokens = cursor.fetchall()
                token_char_map = { (t['start_char'], t['end_char']): t['token_id'] for t in db_tokens }

                if not token_char_map:
                    continue

                doc = self.nlp(sent_text)
                
                for sentence in doc.sentences:
                    for word in sentence.words:
                        start, end = word.start_char, word.end_char
                        if (start, end) in token_char_map:
                            token_id = token_char_map[(start, end)]
                            new_lemma = word.lemma
                            if new_lemma:
                                updates_to_perform.append((new_lemma, token_id))
                
                # 3. Commit batch if size is reached
                if (i + 1) % commit_batch_size == 0:
                    if updates_to_perform:
                        logger.info(f"Cümle #{i+1}: {len(updates_to_perform)} güncelleme kaydediliyor...")
                        cursor.executemany("UPDATE tokens SET lemma = ? WHERE token_id = ?", updates_to_perform)
                        self.conn.commit()
                        updates_to_perform = [] # Reset batch
                    
                    if self.progress_callback:
                        progress = (i + 1) / total_sentences * 100
                        self.progress_callback(progress, f"{i+1}/{total_sentences} cümle işlendi (kaydedildi)...")

            # 4. Commit any remaining updates after the loop
            if updates_to_perform:
                logger.info(f"Kalan {len(updates_to_perform)} güncelleme kaydediliyor...")
                cursor.executemany("UPDATE tokens SET lemma = ? WHERE token_id = ?", updates_to_perform)
                self.conn.commit()

            if self.progress_callback:
                self.progress_callback(100, "İşlem tamamlandı!")

        except Exception as e:
            logger.error(f"Lemma güncelleme sırasında hata: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        finally:
            self.close()

if __name__ == '__main__':
    # Example usage
    # This will update the lemmas in 'corpus.db' using the new BERT model
    # Note: Make sure 'corpus.db' exists or provide the correct path
    import os
    db_path = 'corpus.db'
    if not os.path.exists(db_path):
        logger.warning(f"Veritabanı bulunamadı: {db_path}. Lütfen doğru yolu kontrol edin.")
    else:
        updater = BERTLemmaUpdater(db_path)
        updater.update_all_lemmas()
