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
from typing import Callable, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    # This will update the lemmas in 'corpus.db'
    updater = StanzaLemmaUpdater('corpus.db')
    updater.update_all_lemmas()
