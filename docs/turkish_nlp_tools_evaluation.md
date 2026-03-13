# Türkçe NLP Araçları Değerlendirmesi

Bu doküman, projemizde kullanılan Türkçe Doğal Dil İşleme (NLP) araçlarının bir karşılaştırmasını ve seçim kriterlerini sunar.

## 🚀 Karşılaştırılan Araçlar

### 1. spaCy (Turkish Model)
spaCy, endüstri standardı bir NLP kütüphanesidir ve `tr_core_news_sm` modeli ile Türkçe desteği sunar.

- **Artıları**:
  - Hızlı ve verimli.
  - POS tagging, lemmatization ve dependency parsing desteği tam.
  - Python ekosistemi ile mükemmel uyum.
- **Eksileri**:
  - Türkçe modelleri bazen morfolojik olarak karmaşık kelimelerde yanılabilir.
  - Python 3.14+ sürümlerinde kurulum sorunları olabilir (Python 3.11-3.13 önerilir).

### 2. Custom BERT (Hugging Face)
Projemize entegre edilen `Sarpyy/LiSyntaxDeneme` (checkpoint-3375) modeli, derin öğrenme tabanlı bir yaklaşımdır.

- **Artıları**:
  - **En yüksek doğruluk**: Bağlamsal (context-aware) analiz yapar.
  - Modern NLP standardı (Transformers).
  - Güven skorları (confidence scores) sunar.
- **Eksileri**:
  - Diğerlerine göre daha yavaş (GPU yoksa).
  - Bellek (RAM) kullanımı daha yüksek.
  - Şu an için dependency parsing desteği entegre edilmemiştir.

### 3. Simple Regex Tokenizer (Fallback)
Herhangi bir kütüphane gerektirmeyen, Python'un standart regex modülünü kullanan bir sistem.

- **Artıları**:
  - Sıfır bağımlılık (Zero dependency).
  - Işık hızında.
  - Her zaman çalışır (garanti fallback).
- **Eksileri**:
  - Sadece kelimeleri ayırır (Tokenization).
  - POS tagging veya Lemma desteği yoktur.
  - Dilbilimsel analiz için yetersizdir.

## 📊 Karşılaştırma Tablosu

| Özellik | spaCy | BERT (Custom) | Simple |
|---------|-------|---------------|--------|
| Hız | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Doğruluk (POS) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Lemmatization | ✅ | ✅ (Heuristic) | ❌ |
| Dependency Parsing | ✅ | ❌ | ❌ |
| Kurulum Kolaylığı | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Türkçe Karakter Uyumu | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🏆 Seçim Rehberi

1. **Hız ve Temel Analiz**: `Simple` backend seçin. (KWIC ve Frekans için yeterli)
2. **Akademik ve Derinlemesine Analiz**: `BERT` backend seçin. (En doğru POS etiketleme)
3. **Tam Dilbilimsel Analiz**: `spaCy` backend seçin. (Dependency tree ve morph özellikleri için)

## 🛠️ Kurulum Notları

### spaCy Türkçe
```bash
pip install spacy
python -m spacy download tr_core_news_sm
```

### BERT Backend
Model otomatik olarak Hugging Face'den indirilir. `transformers` ve `torch` kütüphanelerinin kurulu olması yeterlidir.

## 🏁 Sonuç
Projemiz, kullanıcıya esneklik sağlamak için bu üç backend'i de destekler. Varsayılan olarak (eğer kütüphaneler mevcutsa) **BERT** veya **spaCy** önerilir; aksi takdirde sistem otomatik olarak **Simple** moduna geçer.
