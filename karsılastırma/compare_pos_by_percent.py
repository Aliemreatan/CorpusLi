import os
import sys
import logging
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from tqdm import tqdm
import warnings
import torch

# 1. ZEYREK LOGLARINI KAPAT (Terminali temizlemek için)
logging.getLogger("zeyrek").setLevel(logging.ERROR)

# Uyarıları gizle
warnings.filterwarnings("ignore")

# Proje kök dizini ayarı
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# NLP Modülleri
from nlp.turkish_processor import TurkishNLPProcessor
from nlp.custom_bert_processor import CustomBERTProcessor

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("Benchmark")

# -----------------------------------------------------------------------------
# 1. ALTIN STANDART VERİ SETİ (GROUND TRUTH)
# -----------------------------------------------------------------------------
GOLD_STANDARD_DATA = [
    # --- KOLAY CÜMLELER ---
    ("Ali eve geldi.", ["NOUN", "NOUN", "VERB", "PUNCT"]),
    ("Bugün hava çok güzel.", ["NOUN", "NOUN", "ADV", "ADJ", "PUNCT"]),
    ("Kırmızı elma masada duruyor.", ["ADJ", "NOUN", "NOUN", "VERB", "PUNCT"]),
    ("Benimle gel.", ["PRON", "VERB", "PUNCT"]),
    ("Kitabı okudum.", ["NOUN", "VERB", "PUNCT"]),
    
    # --- EŞ SESLİ KELİMELER ---
    ("Bu yaz tatile gideceğiz.", ["DET", "NOUN", "NOUN", "VERB", "PUNCT"]),
    ("Bana bir mektup yaz.", ["PRON", "DET", "NOUN", "VERB", "PUNCT"]),
    ("Yüzünü yıkadı.", ["NOUN", "VERB", "PUNCT"]),
    ("Denizde yüz.", ["NOUN", "VERB", "PUNCT"]),
    ("Yüz lira ver.", ["NUM", "NOUN", "VERB", "PUNCT"]),
    ("Ocak ayında kar yağar.", ["NOUN", "NOUN", "NOUN", "VERB", "PUNCT"]),
    ("Atı alan Üsküdar'ı geçti.", ["NOUN", "VERB", "NOUN", "VERB", "PUNCT"]),
    ("Topu bana at.", ["NOUN", "PRON", "VERB", "PUNCT"]),
    
    # --- SIFAT / ZARF ---
    ("Hızlı araba kaza yaptı.", ["ADJ", "NOUN", "NOUN", "VERB", "PUNCT"]),
    ("Araba hızlı gidiyordu.", ["NOUN", "ADV", "VERB", "PUNCT"]),
    ("Güzel bir gün.", ["ADJ", "DET", "NOUN", "PUNCT"]),
    ("Güzel konuş.", ["ADV", "VERB", "PUNCT"]),
    ("Doğru yolu bul.", ["ADJ", "NOUN", "VERB", "PUNCT"]),
    
    # --- ZAMİRLER ---
    ("O, bize gelecek.", ["PRON", "PRON", "VERB", "PUNCT"]),
    ("O kitabı ver.", ["DET", "NOUN", "VERB", "PUNCT"]),
    ("Bu çok zor.", ["PRON", "ADV", "ADJ", "PUNCT"]),
    ("Bu soru zor.", ["DET", "NOUN", "ADJ", "PUNCT"]),
    
    # --- DİĞER ---
    ("Koşmak faydalıdır.", ["VERB", "NOUN", "ADJ", "PUNCT"]),
    ("Gelen gideni aratır.", ["VERB", "ADJ", "VERB", "PUNCT"]),
    ("Türkiye'nin başkenti Ankara'dır.", ["NOUN", "NOUN", "NOUN", "PUNCT"]),
    ("Sen de mi geldin?", ["PRON", "CCONJ", "PART", "VERB", "PUNCT"]),
    ("Ah, elim yandı!", ["INTJ", "NOUN", "VERB", "PUNCT"]),
    ("Neden gelmedin?", ["ADV", "VERB", "PUNCT"]),
    ("Dr. Ahmet geldi.", ["NOUN", "NOUN", "VERB", "PUNCT"])
]

# -----------------------------------------------------------------------------
# 2. TAG NORMALİZASYON KATMANI
# -----------------------------------------------------------------------------
def normalize_tag(raw_tag, model_source):
    if raw_tag is None: return "NOUN"
    raw_tag = str(raw_tag).upper()
    
    # --- CustomBERT ---
    if model_source == 'CustomBERT':
        if 'NOUN' in raw_tag or 'AD' in raw_tag: return 'NOUN'
        if 'VERB' in raw_tag or 'FİİL' in raw_tag: return 'VERB'
        if 'ADJ' in raw_tag or 'SIFAT' in raw_tag: return 'ADJ'
        if 'ADV' in raw_tag or 'BELİRTEÇ' in raw_tag or 'ZARF' in raw_tag: return 'ADV'
        if 'PRON' in raw_tag or 'ADIL' in raw_tag: return 'PRON'
        if 'DET' in raw_tag or 'BELİRLEYİCİ' in raw_tag: return 'DET'
        if 'PUNCT' in raw_tag or 'NOKTALAMA' in raw_tag: return 'PUNCT'
        if 'NUM' in raw_tag: return 'NUM'
        if 'CONJ' in raw_tag: return 'CCONJ'
        if 'ADP' in raw_tag or 'İLGEÇ' in raw_tag: return 'ADP'
        if 'QUESTION' in raw_tag or 'SORU' in raw_tag: return 'PART'
        if 'INTJ' in raw_tag: return 'INTJ'
        return 'NOUN'
        
    # --- Zeyrek ---
    elif model_source == 'Zeyrek':
        if 'NOUN' in raw_tag: return 'NOUN'
        if 'VERB' in raw_tag: return 'VERB'
        if 'ADJ' in raw_tag: return 'ADJ'
        if 'ADV' in raw_tag: return 'ADV'
        if 'PRON' in raw_tag: return 'PRON'
        if 'DET' in raw_tag: return 'DET'
        if 'PUNC' in raw_tag: return 'PUNCT'
        if 'NUM' in raw_tag: return 'NUM'
        if 'CONJ' in raw_tag: return 'CCONJ'
        if 'POSTP' in raw_tag: return 'ADP'
        if 'QUES' in raw_tag: return 'PART'
        if 'INTERJ' in raw_tag: return 'INTJ'
        return 'NOUN'

    # --- Stanza ---
    else:
        if raw_tag == 'PROPN': return 'NOUN'
        if raw_tag == 'AUX': return 'VERB'
        return raw_tag

# -----------------------------------------------------------------------------
# 3. DOĞRULUK HESAPLAMA
# -----------------------------------------------------------------------------
class AccuracyBenchmark:
    def __init__(self):
        self.models = {}

    def load_models(self):
        # 1. CustomBERT
        try:
            logger.info("Yükleniyor: CustomBERT...")
            self.models['CustomBERT'] = CustomBERTProcessor(model_path="LiProject/Bert-turkish-pos-trained")
        except: pass

        # 2. Stanza
        try:
            import stanza
            logger.info("Yükleniyor: Stanza...")
            self.models['Stanza'] = stanza.Pipeline('tr', processors='tokenize,pos', verbose=False, use_gpu=False)
        except: pass

        # 3. Zeyrek
        try:
            import zeyrek
            import nltk
            logger.info("Yükleniyor: Zeyrek...")
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('tokenizers/punkt_tab')
            except LookupError:
                nltk.download('punkt')
                nltk.download('punkt_tab')
            self.models['Zeyrek'] = zeyrek.MorphAnalyzer()
        except: pass
        
        # 4. Simple
        try:
            self.models['Simple'] = TurkishNLPProcessor(backend='simple')
            logger.info("Yükleniyor: Simple...")
        except: pass

    # CustomBERT Merge Helper
    def predict_custom_bert(self, text, model_wrapper):
        if hasattr(model_wrapper, 'tokenizer') and hasattr(model_wrapper, 'model'):
            tokenizer = model_wrapper.tokenizer
            model = model_wrapper.model
        else: return []

        inputs = tokenizer(text, return_tensors="pt", return_offsets_mapping=True)
        offset_mapping = inputs.pop("offset_mapping")[0]
        with torch.no_grad():
            outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=2)[0]
        id2label = model.config.id2label
        tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
        merged_tokens = []
        split_punctuations = {'.', ',', '!', '?', ';', ':', '...', '"', ')', ']', '}', '-'}
        
        for i in range(1, len(tokens) - 1):
            token = tokens[i]
            label_id = predictions[i].item()
            current_label = id2label[label_id]
            start, end = offset_mapping[i]
            is_subword = token.startswith("##")
            clean_token = token[2:] if is_subword else token
            
            should_merge = False
            if merged_tokens:
                prev_end = merged_tokens[-1]["end"]
                is_adjacent = (start == prev_end)
                if is_subword: should_merge = True
                elif is_adjacent and clean_token not in split_punctuations: should_merge = True
            
            if not merged_tokens or not should_merge:
                merged_tokens.append({"word": clean_token, "label": current_label, "end": end.item()})
            else:
                merged_tokens[-1]["word"] += clean_token
                merged_tokens[-1]["end"] = end.item()
        
        return [(m["word"], m["label"]) for m in merged_tokens]

    def run_benchmark(self):
        logger.info(f"Benchmark başlatılıyor... Toplam Cümle: {len(GOLD_STANDARD_DATA)}")
        model_predictions = {m: [] for m in self.models.keys()}
        all_ground_truth = []

        for sentence, expected_tags in tqdm(GOLD_STANDARD_DATA, desc="Cümleler İşleniyor"):
            all_ground_truth.extend(expected_tags)
            
            for model_name, model in self.models.items():
                pred_tags_raw = []
                try:
                    # --- MODEL TAHMİNLERİ ---
                    if model_name == 'CustomBERT':
                        raw_output = self.predict_custom_bert(sentence, model)
                        pred_tags_raw = [x[1] for x in raw_output]
                        
                    elif model_name == 'Stanza':
                        doc = model(sentence)
                        # Kelime kelime değil, boşluk bazlı almaya çalışalım ki sayı tutsun
                        for sent in doc.sentences:
                            for word in sent.words:
                                pred_tags_raw.append(word.upos)
                                
                    elif model_name == 'Zeyrek':
                        # ZEYREK CRASH FIX:
                        analysis = model.analyze(sentence)
                        for word_res in analysis:
                            # word_res: ('Kelime', [Parse1, Parse2...])
                            if word_res[1]: 
                                # Parse varsa
                                pred_tags_raw.append(word_res[1][0].pos)
                            else:
                                # Parse yoksa (Noktalama veya UNK)
                                if str(word_res[0]) in {'.',',','!','?','"',"'",';',':'}:
                                    pred_tags_raw.append('Punc')
                                else:
                                    pred_tags_raw.append('Noun')

                    elif model_name == 'Simple':
                        out = model.process_text(sentence)
                        pred_tags_raw = [x['upos'] for x in out]
                    
                    # --- NORMALİZASYON ---
                    normalized_preds = [normalize_tag(t, model_name) for t in pred_tags_raw]
                    
                    # --- HİZALAMA (ALIGNMENT) ---
                    # Modeller noktalamayı ayırdığı için token sayısı artabilir.
                    # Hedef uzunluğa zorluyoruz.
                    target_len = len(expected_tags)
                    
                    if len(normalized_preds) > target_len:
                        normalized_preds = normalized_preds[:target_len]
                    elif len(normalized_preds) < target_len:
                        # Eksik kaldıysa MISMATCH ile doldur
                        normalized_preds.extend(['MISMATCH'] * (target_len - len(normalized_preds)))
                    
                    model_predictions[model_name].extend(normalized_preds)

                except Exception as e:
                    # Hata olursa logla ama döngüyü kırma
                    # logger.error(f"{model_name} Hatası: {e}") 
                    model_predictions[model_name].extend(['ERROR'] * len(expected_tags))

        # --- SKORLAMA ---
        results = []
        for model_name, preds in model_predictions.items():
            acc = accuracy_score(all_ground_truth, preds)
            precision, recall, f1, _ = precision_recall_fscore_support(all_ground_truth, preds, average='weighted', zero_division=0)
            
            results.append({
                "Model": model_name,
                "Doğruluk (Accuracy)": f"%{acc*100:.2f}",
                "F1-Score": f"{f1:.4f}",
                "Hata Oranı": f"%{(1-acc)*100:.2f}"
            })
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    benchmark = AccuracyBenchmark()
    benchmark.load_models()
    
    if not benchmark.models:
        print("Hiçbir model yüklenemedi!")
        sys.exit()
        
    df_results = benchmark.run_benchmark()
    
    print("\n" + "="*60)
    print("🚀 DOĞRULUK KARŞILAŞTIRMA SONUCU")
    print("="*60)
    print(df_results.to_markdown(index=False))
    print("="*60 + "\n")
    
    # Kaydet
    out_dir = os.path.join(project_root, "karsılastırma")
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    df_results.to_csv(os.path.join(out_dir, "benchmark_scores.csv"), index=False)