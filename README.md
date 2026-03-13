# 🇹🇷 Corpus Data Manipulator (CDM)

**Corpus Data Manipulator**, Türkçe metin korpuslarını işlemek, analiz etmek, düzenlemek ve görselleştirmek için geliştirilmiş **Sketch Engine benzeri** kapsamlı bir masaüstü uygulamasıdır.

Bu proje; büyük metin verilerini (TXT, JSON, XML) veritabanına aktarır, **BERT tabanlı Yapay Zeka** modelleriyle dilbilimsel analiz (POS Tagging) yapar ve kullanıcılara KWIC, Collocation, Word Sketch gibi gelişmiş arama imkanları sunar.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

---

## 🚀 Özellikler

### 🧠 1. Gelişmiş NLP Altyapısı
*   **Çoklu Backend Desteği:** `Simple` (Hızlı), `spaCy` ve **`Custom BERT`**.
*   **BERT Entegrasyonu:** Hugging Face modelleri (`LiProject/Bert-turkish-pos-trained`) ile yüksek doğrulukta POS etiketleme.
*   **Re-Tagging:** Mevcut veritabanını tek tıkla BERT ile yeniden analiz etme.

### 📊 2. Analiz Araçları
*   **KWIC (Key Word In Context):** Kelimeyi bağlamıyla birlikte görüntüleme.
*   **Frekans Analizi:** Corpus'taki en sık kelimeler.
*   **Collocation (Eşdizimlilik):** PMI, T-Score ve Log-Likelihood ile kelime ilişkileri.
*   **Word Sketch:** Kelimenin gramer ilişkilerini (Özne, Nesne vb.) çıkarma.
*   **CQL (Corpus Query Language):** Karmaşık sorgular yazabilme. Örn: `[pos="ADJ"] [lemma="insan"]`

### 🎨 3. Görselleştirme
*   **Kelime Bulutu (Word Cloud):** Corpus özetini görsel olarak sunar.
*   **Grafikler:** En sık kelimeler (Bar Chart) ve POS dağılımı (Pie Chart).

### 🛠️ 4. Corpus ve Veri Yönetimi
*   **Çoklu Format:** `.txt`, `.json`, `.xml` dosyalarını otomatik tanır ve işler.
*   **Veritabanı Editörü:** Analiz sonuçlarını ve token hatalarını elle (Excel benzeri arayüzle) düzeltebilme.
*   **Akademik Export:** Verileri **CoNLL-U** formatında dışa aktarma.

---

## 💻 Kurulum

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/Aliemreatan/corpus_manipulator.git
cd corpus_manipulator
```

### 2. Sanal Ortam Oluşturun (Önerilen)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Gereksinimleri Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Dil Modellerini İndirin (Opsiyonel ama Önerilen)
Tam performans için spaCy modellerini indirin (BERT otomatik iner).

```bash
# spaCy Türkçe Modeli
python -m spacy download tr_core_news_sm
```


---

## 🎮 Kullanım

Uygulamanın grafik arayüzünü (GUI) başlatmak için:

```bash
python run_gui.py
```

### Adım Adım Rehber

1.  **Veritabanı Oluştur:** "Veritabanı" sekmesinden yeni bir `.db` dosyası oluşturun.
2.  **Veri Yükle:** "İçeri Aktarma" sekmesinden metin dosyalarınızın olduğu klasörü seçin ve yükleyin.
3.  **Analiz Yap:** "Analiz" sekmesinden KWIC, Frekans veya CQL araması yapın.
4.  **Görselleştir:** "Görselleştirme" sekmesinden grafikler oluşturun.
5.  **Düzenle:** "Araçlar" -> "Veritabanı Editörü" ile hatalı etiketleri elle düzeltin.

---

## 🔎 CQL (Corpus Query Language) Rehberi

Analiz sekmesinde "CQL" seçeneğini seçerek şu sorguları yapabilirsiniz:

| Sorgu | Açıklama |
|-------|----------|
| `[form="ev"]` | "ev" kelimesini bulur. |
| `[pos="ADJ"] [lemma="insan"]` | Sıfat + "insan" kökü (örn: "güzel insanlar"). |
| `[pos="NOUN"] [pos="VERB"]` | İsim ardından gelen Fiil. |
| `[lemma="git"] [] [pos="VERB"]` | "git" kökü + herhangi bir kelime + Fiil. |

---

## 📁 Proje Yapısı

```
corpus_manipulator/
├── gui/                  # Grafik Arayüz kodları (Visualizer, Editor vb.)
├── nlp/                  # Dil işleme (BERT ve spaCy entegrasyonu)
├── database/             # Veritabanı şeması ve SQL işlemleri
├── query/                # Arama motoru ve CQL parser
├── ingestion/            # Dosya okuma ve işleme
├── run_gui.py            # Ana başlatıcı
├── update_db_with_bert.py # BERT güncelleme aracı
└── requirements.txt      # Bağımlılıklar
```

---

## 🤝 Katkıda Bulunma

Hataları bildirmek veya özellik eklemek için lütfen "Issues" veya "Pull Request" kullanın.

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
