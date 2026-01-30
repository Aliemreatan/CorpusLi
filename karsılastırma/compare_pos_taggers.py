import os
import sys
import time
import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from pathlib import Path
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Add project root to path to import nlp modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Bu modüllerin projenizde var olduğunu varsayıyoruz
from nlp.turkish_processor import TurkishNLPProcessor
from nlp.custom_bert_processor import CustomBERTProcessor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelComparator:
    def __init__(self):
        self.results = []
        self.models = {}
        self.sample_sentences = [
    # --- KATEGORİ 1: EŞ SESLİ KELİMELER (HOMONYMS) ---
    "Çayın kenarında oturup sıcak bir çay içtik.",
    "Yüz kere söyledim, şu yastığın kılıfını yüz.",
    "Bu yaz, bana sık sık mektup yaz.",
    "Ocak ayında yeni bir ocak satın aldık.",
    "Kır saçlı adam, odunları dizinde kır.",
    "Atı alan Üsküdar'ı geçti, sen o taşı at.",
    "Ben bu benleri yüzümden aldırmak istiyorum.",
    "Kaz gelecek yerden tavuk esirgenmez, toprağı kaz.",
    "Dolu yağarken bardak tamamen dolu muydu?",
    "Kara görününce gemidekiler kara kara düşünmeye başladı.",
    "Kara kızın kısa kayışını kasışına kızmayışına şaşmamışsın da, kuru kazın kızıp kayısı kazışına şaşmış kalmışsın.",

    # --- KATEGORİ 2: SIFAT / ZARF AYRIMI (ADJ vs ADV) ---
    "Hızlı araba yolda hızlı gidiyordu.",
    "Güzel konuşan insan güzel düşünür.",
    "Doğru insanla doğru zamanda karşılaşmak zordur.",
    "Tahtayı doğru kessen iyi olurdu.",
    "Yalnız adam, evde yalnız yaşıyordu.",
    "Genç, yaşlılara yer verdi.",
    "Hasta çocuk hasta yatağında yatıyor.",

    # --- KATEGORİ 3: DEVRİK VE KARMAŞIK CÜMLELER ---
    "Gidiyorum gündüz gece, bilmiyorum ne haldeyim.",
    "Sakla samanı, gelir zamanı.",
    "Ağır ağır çıkacaksın bu merdivenlerden.",
    "Görmedim ömrümde böyle bir rezalet.",
    "Severim fırtınalı havalarda denizi izlemeyi.",
    "Anlatamıyorum derdimi kimselere.",

    # --- KATEGORİ 4: ÇEKİM EKLERİ VE MORFOLOJİ ---
    "Çekoslovakyalılaştıramadıklarımızdan mısınız?",
    "Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine.",
    "Evdeki hesap çarşıya uymaz.",
    "Gözlükçüden aldığım gözlüğü gözlüğümün kabına koydum.",
    "Kitaplıktaki kitapları kitapçığa kaydettim.",

    # --- KATEGORİ 5: SORU VE ÜNLEM İFADELERİ ---
    "Sen de mi Brütüs?",
    "Ah, elim yandı!",
    "Eyvah, otobüsü kaçırdım!",
    "Bunu sana kim söyledi, Ali mi Veli mi?",
    "Neden benimle gelmedin, korktun mu?",
    
    # --- KATEGORİ 6: ÖZEL İSİMLER VE KESME İŞARETLERİ ---
    "Türkiye'nin başkenti Ankara'dır ve Anıtkabir oradadır.",
    "TBMM'nin açılış tarihi 23 Nisan 1920'dir.",
    "Ayşe'nin kedisi Minnoş, Van Gölü'ne düştü.",
    "İngilizce'yi ve Almanca'yı aynı anda öğreniyor.",
    "Dr. Ahmet Bey, Prof. Dr. Mehmet ile görüştü.",

    # --- KATEGORİ 7: BELİRSİZLİK VE ZAMİRLER ---
    "O, bu akşam bize gelecek.",
    "O kitabı bana ver.",
    "Bu, çok zor bir soru.",
    "Bu soruyu çözmek zor.",
    "Şu ağacı görüyor musun?",     
    "Şunu bana uzatır mısın?",

    # --- KATEGORİ 8: FİİLİMSİLER (GERUNDS/PARTICIPLES) ---
    "Koşmak sağlığa yararlıdır.",
    "Gelen gideni aratır.",
    "Gülerek yanıma geldi.",
    "Okumuş adamın hali başka olur.",
    "Dolmuş durağa yanaştı."
    ]

    
    def load_existing_models(self):
        """Load models already integrated into the project"""
        logger.info("Loading existing project models...")
        
        # 1. Simple / Regex
        try:
            self.models['Project_Simple'] = TurkishNLPProcessor(backend='simple')
            logger.info("Loaded: Project_Simple")
        except Exception as e:
            logger.error(f"Failed to load Project_Simple: {e}")

        # 2. SpaCy
        try:
            import spacy
            try:
                self.models['Project_SpaCy'] = TurkishNLPProcessor(backend='spacy')
                logger.info("Loaded: Project_SpaCy")
            except OSError:
                 logger.warning("SpaCy model 'tr_core_news_sm' not found. Skipping SpaCy.")
        except Exception as e:
             logger.warning(f"SpaCy could not be loaded: {e}. Skipping.")

        # 3. Custom BERT (LiProject)
        try:
            self.models['Project_CustomBERT'] = CustomBERTProcessor(model_path="LiProject/Bert-turkish-pos-trained")
            logger.info("Loaded: Project_CustomBERT (LiProject)")
        except Exception as e:
            logger.error(f"Failed to load Project_CustomBERT: {e}")

    def load_extra_models(self):
        """Load extra models explicitly for comparison"""
        logger.info("Loading EXTRA models for comparison...")
        
        # Extra 1: Stanza
        try:
            import stanza
            logger.info("Loading Stanza (this might take a while if downloading models)...")
            try:
                self.models['Extra_Stanza'] = stanza.Pipeline('tr', processors='tokenize,pos', verbose=False, use_gpu=False)
                logger.info("Loaded: Extra_Stanza")
            except Exception:
                logger.info("Downloading Stanza Turkish models...")
                stanza.download('tr')
                self.models['Extra_Stanza'] = stanza.Pipeline('tr', processors='tokenize,pos', verbose=False, use_gpu=False)
                logger.info("Loaded: Extra_Stanza")
        except ImportError:
            logger.warning("Stanza library not installed. Skipping.")
        except Exception as e:
            logger.warning(f"Could not load Stanza: {e}")

        # Extra 2: Zeyrek (FIX APPLIED: NLTK Download)
        try:
            import zeyrek
            import nltk
            logger.info("Loading Zeyrek...")
            
            # Zeyrek için gerekli NLTK 'punkt' verisini kontrol et ve indir
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('tokenizers/punkt_tab')
            except LookupError:
                logger.info("NLTK 'punkt' verisi eksik, indiriliyor...")
                nltk.download('punkt')
                nltk.download('punkt_tab')
            
            self.models['Extra_Zeyrek'] = zeyrek.MorphAnalyzer()
            logger.info("Loaded: Extra_Zeyrek")
        except ImportError:
            logger.warning("Zeyrek library not installed. Skipping.")
        except Exception as e:
            logger.warning(f"Could not load Zeyrek: {e}")

        # Extra 3: ozcangundes/bert-base-turkish-cased-pos
        model_name = "ozcangundes/bert-base-turkish-cased-pos"
        try:
            logger.info(f"Downloading/Loading Extra Model: {model_name}")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForTokenClassification.from_pretrained(model_name)
            nlp_pipeline = pipeline("token-classification", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
            
            self.models['Extra_OzcanBert'] = nlp_pipeline
            logger.info(f"Loaded: Extra_OzcanBert")
        except Exception as e:
            logger.warning(f"Could not load extra model {model_name}: {e}")

    # -------------------------------------------------------------------------
    # GÜNCELLENMİŞ FONKSİYON: Noktalama İşaretlerini Ayıran Akıllı Birleştirme
    # -------------------------------------------------------------------------
    def predict_and_merge(self, text, tokenizer, model):
        """
        BERT çıktısını işler. 
        - WordPiece parçalarını (##) birleştirir.
        - Kesme işaretiyle ayrılanları (Üsküdar'ı) birleştirir.
        - ANCAK nokta, virgül gibi cümle sonu işaretlerini (geçti,) ayırır.
        """
        # 1. Tokenize et
        inputs = tokenizer(text, return_tensors="pt", return_offsets_mapping=True)
        offset_mapping = inputs.pop("offset_mapping")[0]
        
        # 2. Modeli çalıştır
        with torch.no_grad():
            outputs = model(**inputs)
        
        predictions = torch.argmax(outputs.logits, dim=2)[0]
        id2label = model.config.id2label

        merged_tokens = []
        tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
        # Asla birleşmemesi gereken noktalama işaretleri listesi
        split_punctuations = {'.', ',', '!', '?', ';', ':', '...', '"', ')', ']', '}', '-'}

        # [CLS] ve [SEP] atla
        for i in range(1, len(tokens) - 1):
            token = tokens[i]
            label_id = predictions[i].item()
            current_label = id2label[label_id]
            start, end = offset_mapping[i]
            
            # WordPiece '##' temizliği
            is_subword = token.startswith("##")
            clean_token = token[2:] if is_subword else token

            # --- Birleştirme Karar Mekanizması ---
            should_merge = False
            
            if merged_tokens:
                prev_end = merged_tokens[-1]["end"]
                is_adjacent = (start == prev_end) # Karakterler fiziksel olarak değiyor mu?
                
                # Kural 1: Eğer '##' ile başlıyorsa kesinlikle birleşir (kelime kökü parçasıdır)
                if is_subword:
                    should_merge = True
                
                # Kural 2: Eğer fiziksel olarak bitişikse...
                elif is_adjacent:
                    # ...VE şu anki token "ayırıcı noktalama" (virgül, nokta vb.) DEĞİLSE birleştir.
                    if clean_token not in split_punctuations:
                        should_merge = True

            if not merged_tokens or not should_merge:
                # YENİ TOKEN BAŞLAT
                merged_tokens.append({
                    "word": clean_token,
                    "label": current_label, 
                    "start": start.item(),
                    "end": end.item()
                })
            else:
                # ÖNCEKİNE EKLE (MERGE)
                merged_tokens[-1]["word"] += clean_token
                merged_tokens[-1]["end"] = end.item()
                # Etiketi güncellemiyoruz (İlk parça esastır)

        final_output = [(item["word"], item["label"]) for item in merged_tokens]
        return final_output
    # -------------------------------------------------------------------------

    def normalize_pos_output(self, raw_output, model_name):
        """Normalize output from different models to a standard format list of (word, pos) tuples."""
        normalized = []
        try:
            if model_name == 'Project_Simple':
                for token in raw_output:
                    normalized.append((token['word'], token['upos']))
            elif model_name == 'Project_SpaCy':
                for token in raw_output:
                    normalized.append((token['word'], token['upos']))
            elif model_name == 'Project_CustomBERT':
                for token in raw_output:
                    normalized.append((token['word'], token['upos']))
            elif model_name == 'Extra_OzcanBert':
                for entity in raw_output:
                    tag = entity['entity_group']
                    word = entity['word']
                    normalized.append((word, tag))
            elif model_name == 'Extra_Stanza':
                for sent in raw_output.sentences:
                    for word in sent.words:
                        normalized.append((word.text, word.upos))
            elif model_name == 'Extra_Zeyrek':
                # FIX APPLIED: Zeyrek güvenli ayrıştırma
                for word_analysis in raw_output:
                    try:
                        word_surface = word_analysis[0]
                        parses = word_analysis[1]
                        
                        if not parses:
                            # Parse yoksa ve noktalamaysa PUNCT, değilse UNK
                            if word_surface in {'.', ',', '!', '?', ';', ':'}:
                                pos = "PUNCT"
                            else:
                                pos = "UNK"
                        else:
                            primary_pos = parses[0].pos
                            if primary_pos == "Unk":
                                pos = "UNK"
                            else:
                                pos = self._map_zeyrek_pos(primary_pos)
                        
                        normalized.append((word_surface, pos))
                    except Exception as ze:
                        normalized.append((word_analysis[0], "ERROR"))
                        
        except Exception as e:
            logger.error(f"Error normalizing output for {model_name}: {e}")
        return normalized

    def _map_zeyrek_pos(self, zeyrek_pos):
        mapping = {
            'Noun': 'NOUN', 'Verb': 'VERB', 'Adj': 'ADJ', 'Adv': 'ADV',
            'Pron': 'PRON', 'Det': 'DET', 'Conj': 'CCONJ', 'Interj': 'INTJ',
            'Punc': 'PUNCT', 'Num': 'NUM', 'Postp': 'ADP', 'Ques': 'PART', 'Dup': 'X'
        }
        return mapping.get(zeyrek_pos, zeyrek_pos)

    def run_comparison(self):
        logger.info("Starting comparison...")
        comparison_data = []
        
        for i, sentence in enumerate(self.sample_sentences):
            logger.info(f"Processing sentence {i+1}/{len(self.sample_sentences)}")
            sent_results = {'Sentence_ID': i, 'Sentence_Text': sentence}
            
            for model_name, model in self.models.items():
                start_time = time.time()
                try:
                    # --- CUSTOM BERT İÇİN ÖZEL MANTIK ---
                    if model_name == 'Project_CustomBERT':
                        if hasattr(model, 'tokenizer') and hasattr(model, 'model'):
                            normalized_tokens = self.predict_and_merge(sentence, model.tokenizer, model.model)
                            output = None 
                        else:
                            output = model.process_text(sentence)
                            normalized_tokens = None
                    
                    # --- DİĞER MODELLER ---
                    elif model_name == 'Project_Simple':
                        output = model.process_text(sentence)
                        normalized_tokens = None
                    elif model_name == 'Project_SpaCy':
                        output = model.process_text(sentence)
                        normalized_tokens = None
                    elif model_name == 'Extra_OzcanBert':
                        output = model(sentence)
                        normalized_tokens = None
                    elif model_name == 'Extra_Stanza':
                        output = model(sentence)
                        normalized_tokens = None
                    elif model_name == 'Extra_Zeyrek':
                        output = model.analyze(sentence)
                        normalized_tokens = None
                    else:
                        output = None
                        normalized_tokens = []

                    end_time = time.time()
                    duration = end_time - start_time
                    
                    if normalized_tokens is None and output is not None:
                        normalized_tokens = self.normalize_pos_output(output, model_name)
                    
                    tag_string = " | ".join([f"{w}/{t}" for w, t in normalized_tokens])
                    sent_results[f"{model_name}_Tags"] = tag_string
                    sent_results[f"{model_name}_Time"] = duration
                    
                except Exception as e:
                    logger.error(f"Error running {model_name} on sentence {i}: {e}")
                    sent_results[f"{model_name}_Tags"] = "ERROR"
                    sent_results[f"{model_name}_Time"] = 0
            
            comparison_data.append(sent_results)
            
        return pd.DataFrame(comparison_data)

    def benchmark_speed_on_corpus(self, corpus_path):
        logger.info(f"Benchmarking speed on {corpus_path}...")
        try:
            with open(corpus_path, 'r', encoding='utf-8') as f:
                text = f.read()[:2000]
                logger.info(f"Text length for benchmark: {len(text)} chars")
        except Exception as e:
            logger.error(f"Could not read corpus file: {e}")
            return {}

        speed_results = {}
        for model_name, model in self.models.items():
            start_time = time.time()
            try:
                if model_name == 'Project_Simple': model.process_text(text)
                elif model_name == 'Project_SpaCy': model.process_text(text)
                elif model_name == 'Project_CustomBERT': model.process_text(text)
                elif model_name == 'Extra_OzcanBert': model(text)
                elif model_name == 'Extra_Stanza': model(text)
                elif model_name == 'Extra_Zeyrek': model.analyze(text)
                
                duration = time.time() - start_time
                speed_results[model_name] = duration
                logger.info(f"{model_name} took {duration:.4f} seconds")
            except Exception as e:
                logger.error(f"{model_name} failed benchmark: {e}")
                speed_results[model_name] = None
        return speed_results

def main():
    comparator = ModelComparator()
    
    # 1. Modelleri Yükle
    comparator.load_existing_models()
    comparator.load_extra_models()
    
    if not comparator.models:
        logger.error("No models loaded! Exiting.")
        return

    # 2. Kalitatif Karşılaştırmayı Çalıştır
    df_qualitative = comparator.run_comparison()
    
    # 3. Sonuçları Kaydet
    output_dir = os.path.join(project_root, "karsılastırma")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Klasör oluşturuldu: {output_dir}")
        
    output_csv = os.path.join(output_dir, "pos_model_karsilastirma.csv")
    df_qualitative.to_csv(output_csv, index=False)
    logger.info(f"Qualitative results saved to {output_csv}")
    
    # 4. Hız Testini Çalıştır
    corpus_file = os.path.join(project_root, "sample_turkish_corpus", "kitap_metni.txt")
    if not os.path.exists(corpus_file):
        dummy_path = os.path.join(project_root, "dummy_corpus.txt")
        with open(dummy_path, "w", encoding="utf-8") as f:
            f.write("Bu bir deneme metnidir. " * 100)
        corpus_file = dummy_path
        
    speed_results = comparator.benchmark_speed_on_corpus(corpus_file)
    
    # 5. Rapor Oluştur
    report_path = os.path.join(output_dir, "karsilastirma_ozeti.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Türkçe POS Tagger Karşılaştırma Raporu\n\n")
        f.write(f"*Rapor Tarihi: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        f.write("## 1. Hız Performansı (2000 karakterlik metin üzerinde)\n")
        f.write("| Model | Süre (saniye) | Durum |\n")
        f.write("|-------|---------------|-------|\n")
        for model, duration in speed_results.items():
            dur_str = f"{duration:.4f}" if duration is not None else "Hata"
            status = "✅ Aktif" if duration is not None else "❌ Yüklenemedi"
            f.write(f"| {model} | {dur_str} | {status} |\n")
            
        f.write("\n## 2. Model Detayları\n")
        f.write("- **Project_Simple:** Regex ve kural tabanlı basit yaklaşım.\n")
        f.write("- **Project_SpaCy:** SpaCy `tr_core_news_sm` modeli.\n")
        f.write("- **Project_CustomBERT:** Projedeki `LiProject/Bert-turkish-pos-trained`.\n")
        f.write("- **Extra_OzcanBert:** HuggingFace `ozcangundes/bert-base-turkish-cased-pos`.\n")
        f.write("- **Extra_Stanza:** Stanford NLP `stanza` kütüphanesi (Türkçe modeli).\n")
        f.write("- **Extra_Zeyrek:** Zemberek'in Python portu (Morfolojik Analiz).\n")
        
        f.write("\n## 3. Detaylı Cümle Analizleri\n")
        f.write("Aşağıda her bir örnek cümlenin farklı modeller tarafından nasıl etiketlendiği gösterilmiştir:\n\n")
        
        for i, row in df_qualitative.iterrows():
            f.write(f"### Cümle {i+1}: \"{row['Sentence_Text']}\"\n")
            f.write("| Model | Etiketlenmiş Çıktı (Kelime/TAG) |\n")
            f.write("| :--- | :--- |\n")
            
            for col in df_qualitative.columns:
                if "_Tags" in col:
                    model_name = col.replace("_Tags", "")
                    tags = row[col]
                    f.write(f"| **{model_name}** | {tags} |\n")
            f.write("\n---\n\n")

    logger.info(f"Report saved to {report_path}")

if __name__ == "__main__":
    main()