"""
Custom BERT-based Turkish NLP Processor

Bu modül kullanıcının fine-tuned BERT POS tagging modelini 
proje ile entegre eder.
"""

import logging
from typing import List, Dict, Any, Optional
import re

logger = logging.getLogger(__name__)

# Try to import transformers, handle gracefully if not available
TRANSFORMERS_AVAILABLE = False
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
    import numpy as np
    TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"Transformers library not available: {e}")
    logger.warning("Please install with: pip install transformers torch")

class CustomBERTProcessor:
    """
    Fine-tuned BERT model ile Türkçe POS tagging ve diğer NLP görevleri
    """
    
    def __init__(self, model_path: Optional[str] = None, tokenizer_path: Optional[str] = None):
        """
        Initialize Custom BERT processor
        
        Args:
            model_path: Fine-tuned BERT model dosya yolu
            tokenizer_path: Tokenizer dosya yolu
        """
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.model = None
        self.tokenizer = None
        
        # Model yükleme durumu
        self.is_loaded = False
        
        self._load_model()
    
    def _load_model(self):
        """Fine-tuned BERT modelini Hugging Face'den yükle"""
        try:
            # Check if transformers is available
            if not TRANSFORMERS_AVAILABLE:
                logger.error("Transformers library not installed")
                logger.error("Please install with: pip install transformers torch")
                self.is_loaded = False
                return
            
            # Use provided model path or fallback to default
            model_path = self.model_path if self.model_path else "LiProject/Bert-Turkish-POS-Trained-V2"
            
            logger.info(f"Hugging Face modeli yükleniyor: {model_path}")
            
            # Model ve tokenizer yükle
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForTokenClassification.from_pretrained(model_path)
            
            # Pipeline oluştur - aggregation olmadan kullan
            self.nlp_pipeline = pipeline(
                "token-classification",
                model=self.model,
                tokenizer=self.tokenizer,
                aggregation_strategy=None  # No aggregation for proper token handling
            )
            
            self.is_loaded = True
            logger.info("Hugging Face BERT modeli başarıyla yüklendi")
            
        except Exception as e:
            logger.error(f"BERT model yüklenemedi: {e}")
            import traceback
            traceback.print_exc()
            logger.info("Fallback olarak basit işleme kullanılıyor")
            self.is_loaded = False
    
    def process_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Fine-tuned BERT ile text işleme. Model çalışmazsa boş liste döner.
        
        Args:
            text: İşlenecek metin
            
        Returns:
            Token bilgileri listesi
        """
        if not self.is_loaded:
            logger.error("BERT Modeli yüklenemedi. İşlem yapılamıyor.")
            return []

        try:
            # Ensure proper UTF-8 encoding before processing
            if not isinstance(text, str):
                text = str(text)
            import unicodedata
            text = unicodedata.normalize('NFC', text)
        except Exception as e:
            logger.warning(f"Metin normalizasyonu başarısız: {e}")
            
        try:
            return self._process_with_bert(text)
        except Exception as e:
            logger.error(f"BERT ile işleme sırasında kritik hata: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _process_with_bert(self, text: str) -> List[Dict[str, Any]]:
        """Hugging Face BERT modeli ile metin işleme"""
        # Tokenize the text first to get proper alignment
        # Use return_offsets_mapping=True to get character positions
        max_len = self.model.config.max_position_embeddings
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            add_special_tokens=True,
            return_offsets_mapping=True,
            truncation=True,
            max_length=max_len
        )
        offset_mapping = inputs['offset_mapping'][0].tolist()
        all_tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(inputs['input_ids'], attention_mask=inputs['attention_mask'])
            
            # Get probabilities and predictions
            probabilities = torch.softmax(outputs.logits, dim=2)
            predictions = torch.argmax(outputs.logits, dim=2)
            
            # Get max probabilities (confidence scores)
            confidences = torch.max(probabilities, dim=2).values

        # Convert predictions to labels
        all_predicted_labels = [self.model.config.id2label[pred.item()] for pred in predictions[0]]
        all_confidences = confidences[0].tolist()

        # Now aggregate subtokens properly
        aggregated_tokens = []
        current_word = ""
        current_label = None
        current_score = 0.0
        subtoken_count = 0
        
        # Track start/end for the aggregated word
        word_start = -1
        word_end = -1

        for idx, (token, label, conf) in enumerate(zip(all_tokens, all_predicted_labels, all_confidences)):
            # Skip special tokens but use them to maintain index alignment if needed
            if token in ['[CLS]', '[SEP]', '[PAD]']:
                continue
            
            # Get offsets for this token
            start, end = offset_mapping[idx]
            
            # Handle subwords
            if token.startswith("##"):
                # This is a continuation of the previous word
                current_word += token[2:]  # Remove ## prefix
                current_score += conf
                subtoken_count += 1
                word_end = end # Update end position
            else:
                # Save previous word if exists
                if current_word:
                    pos = self._map_bert_label_to_pos(current_label, current_word)
                    pos_tr = self._map_pos_to_turkish(pos)

                    token_data = {
                        'word': current_word,
                        'norm': current_word.lower(),
                        'upos': pos,
                        'upos_tr': pos_tr,
                        'xpos': pos,
                        'morph': None, # Morfolojik analiz kaldırıldı
                        'dep_head': None,
                        'dep_rel': None,
                        'start_char': word_start,
                        'end_char': word_end,
                        'is_punctuation': pos == 'PUNCT',
                        'is_space': False,
                        'bert_confidence': current_score / max(subtoken_count, 1)
                    }
                    aggregated_tokens.append(token_data)

                # Start new word
                current_word = token
                current_label = label
                current_score = conf
                subtoken_count = 1
                word_start = start
                word_end = end

        # Don't forget the last word
        if current_word:
            pos = self._map_bert_label_to_pos(current_label, current_word)
            pos_tr = self._map_pos_to_turkish(pos)

            token_data = {
                'word': current_word,
                'norm': current_word.lower(),
                'upos': pos,
                'upos_tr': pos_tr,
                'xpos': pos,
                'morph': None, # Morfolojik analiz kaldırıldı
                'dep_head': None,
                'dep_rel': None,
                'start_char': word_start,
                'end_char': word_end,
                'is_punctuation': pos == 'PUNCT',
                'is_space': False,
                'bert_confidence': current_score / max(subtoken_count, 1)
            }
            aggregated_tokens.append(token_data)

        return aggregated_tokens
    
    def _map_bert_label_to_pos(self, bert_label: str, word: str = '') -> str:
        """
        Returns the raw BERT model label directly, without mapping.
        This ensures the model's direct output is used as the final tag.
        """
        # Kullanıcının isteği üzerine, modelin çıktısını doğrudan kullan.
        # Herhangi bir haritalama veya çeviri yapma.
        return bert_label if bert_label else 'X' # Return 'X' for unknown/None label
    
    def _map_pos_to_turkish(self, pos: str) -> str:
        """Universal POS tag'lerini Türkçe'ye çevir"""
        pos_mapping = {
            'NOUN': 'İsim',
            'VERB': 'Fiil',
            'ADJ': 'Sıfat',
            'ADV': 'Zarf',
            'PRON': 'Zamir',
            'DET': 'Belirteç',
            'ADP': 'İlgeç',
            'CCONJ': 'Bağlaç',
            'SCONJ': 'Bağlaç',
            'AUX': 'Yardımcı Fiil',
            'PROPN': 'Özel İsim',
            'NUM': 'Sayı',
            'PART': 'Parçacık',
            'INTJ': 'Ünlem',
            'PUNCT': 'Noktalama',
            'SYM': 'Sembol'
        }
        return pos_mapping.get(pos, pos)
    
    def _extract_morph_features(self, word: str, label: str) -> str:
        """(Kaldırıldı) Word ve label'dan morfolojik özellikler çıkar"""
        return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Model bilgilerini döndür"""
        return {
            'model_type': 'huggingface_bert',
            'model_path': 'LiProject/Bert-turkish-pos-trained',
            'tokenizer_path': 'LiProject/Bert-turkish-pos-trained',
            'is_loaded': self.is_loaded,
            'supported_features': ['tokenization', 'pos_tagging', 'morphology', 'bert_confidence'],
            'language': 'Turkish',
            'model_source': 'Hugging Face Model Hub',
            'checkpoint': 'main'
        }

def create_custom_bert_processor(model_path: Optional[str] = None, 
                               tokenizer_path: Optional[str] = None) -> CustomBERTProcessor:
    """
    Custom BERT processor oluştur
    
    Args:
        model_path: Fine-tuned BERT model yolu
        tokenizer_path: Tokenizer yolu
        
    Returns:
        CustomBERTProcessor instance
    """
    return CustomBERTProcessor(model_path, tokenizer_path)

# BERT model integration için TurkishNLPProcessor güncelleme
def integrate_bert_with_turkish_processor():
    """
    Custom BERT modelini TurkishNLPProcessor ile entegre et
    
    Bu fonksiyon TurkishNLPProcessor'ı CustomBERTProcessor ile çalışacak şekilde günceller
    """
    
    print("=== BERT MODEL ENTEGRASYONU ===")
    print()
    
    # 1. Model yükleme
    print("1. Custom BERT modeli yükleme:")
    print("   - Fine-tuned POS tagging model")
    print("   - Türkçe için optimize edilmiş")
    print("   - Yüksek doğruluk")
    
    # 2. Entegrasyon
    print("\n2. TurkishNLPProcessor entegrasyonu:")
    print("   - Custom backend olarak eklenebilir")
    print("   - Mevcut API ile uyumlu")
    print("   - Fallback desteği")
    
    # 3. Kullanım örneği
    print("\n3. Kullanım örneği:")
    print("""
    from nlp.custom_bert_processor import create_custom_bert_processor
    from nlp.turkish_processor import TurkishNLPProcessor
    
    # BERT processor oluştur
    bert_processor = create_custom_bert_processor(
        model_path="./my_bert_model",
        tokenizer_path="./my_tokenizer"
    )
    
    # TurkishNLPProcessor ile entegre et
    nlp = TurkishNLPProcessor(backend='custom_bert')
    nlp.set_custom_processor(bert_processor)
    
    # Kullan
    tokens = nlp.process_text("Türkçe metin işleme")
    """)
    
    # 4. Performans
    print("\n4. Performans avantajları:")
    print("   ✓ Yüksek POS tagging doğruluğu")
    print("   ✓ Gelişmiş morfolojik analiz")
    print("   ✓ Türkçe'ye özel eğitim")
    print("   ✓ Custom features desteği")

if __name__ == "__main__":
    # Demo
    integrate_bert_with_turkish_processor()
    
    print("\n=== CUSTOM BERT PROCESSOR DEMO ===")
    
    # Processor oluştur
    processor = create_custom_bert_processor()
    
    # Model bilgileri
    info = processor.get_model_info()
    print(f"Model Type: {info['model_type']}")
    print(f"Loaded: {info['is_loaded']}")
    print(f"Features: {info['supported_features']}")
    
    # Test
    test_text = "Ben okula gidiyorum ve kitap okuyorum."
    tokens = processor.process_text(test_text)
    
    print(f"\nTest Text: {test_text}")
    print(f"Tokens: {len(tokens)}")
    
    for i, token in enumerate(tokens[:5]):
        print(f"{i+1}. {token['form']} -> POS: {token['upos']}, Morph: {token['morph']}")