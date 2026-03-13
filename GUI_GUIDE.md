# Corpus Data Manipulator - GUI Kullanım Kılavuzu

## 🎮 GUI Uygulaması Başlatma

### Hızlı Başlangıç
```bash
cd corpus_manipulator
py run_gui.py
```

### GUI Özellikleri
- **Tkinter Tabanlı**: Python standart kütüphanesi
- **Kullanıcı Dostu**: Tuşlarla kolay kontrol
- **Türkçe Arayüz**: Türkçe etiketler ve mesajlar
- **Gerçek Zamanlı**: İlerleme takibi
- **Hata Yönetimi**: Kullanıcı dostu hata mesajları

## 🖥️ Ana Ekran Bölümleri

### 1. Veritabanı Yapılandırması
- **Veritabanı Dosyası**: SQLite dosya seçimi
- **Gözat Butonu**: Dosya yolu seçimi
- **Oluştur Butonu**: Yeni veritabanı oluşturma

### 2. Corpus İçeri Aktarma
- **Metin Klasörü**: TXT dosyalarını içeren klasör seçimi
- **NLP Backend**: 
  - `simple`: Hızlı, temel (önerilen)
  - `spaCy`: Gelişmiş (Python 3.13 gerekli)
  - `custom_bert`: Kendi modeliniz
- **İçeri Aktar Butonu**: Batch processing

### 3. Corpus Düzenleme (YENİ!)
- **Dosya Aç**: Mevcut corpus dosyalarını düzenleme
- **Yeni Dosya**: Boş dosya oluşturma
- **Kaydet**: Değişiklikleri diske kaydetme
- **Veritabanını Güncelle**: Düzenlenen metni NLP işleyip veritabanına ekleme
- **Metin Düzenleyici**: Tam özellikli metin editörü

### 5. Dosya Düzenleme (YENİ!)
- **JSON Aç**: Kaydedilmiş JSON analiz sonuçlarını düzenleme
- **XML Aç**: Kaydedilmiş XML analiz sonuçlarını düzenleme
- **TXT Aç**: Kaydedilmiş TXT dosyalarını düzenleme
- **Kaydet/Farklı Kaydet**: Düzenlenen dosyaları kaydetme
- **Doğrula**: JSON/XML format doğrulama
- **Format Düzenleyici**: Yapısal veri düzenleme

### 6. Analiz Seçenekleri
- **Analiz Türü**:
  - `KWIC`: Anahtar kelime bağlamlı arama
  - `Frequency`: Frekans analizi
  - `Collocation`: Kelime ortaklık analizi
  - `Word Sketch`: Dependency tabanlı analiz
- **Aranacak Kelime**: Hedef kelime girişi
- **Pencere Boyutu**: Bağlam aralığı (1-20)
- **Analiz Yap Butonu**: İşlem başlatma
- **İstatistikler**: Veritabanı bilgileri

### 5. Sonuçlar Alanı
- **Görüntüleme**: Scrollable text alanı
- **Temizle**: Sonuçları temizleme
- **Kaydet**: TXT dosyasına export

### 6. Durum Çubuğu
- **İşlem Durumu**: Gerçek zamanlı güncellemeler
- **Hata Mesajları**: Kullanıcı bilgilendirmesi

## 📊 GUI Kullanım Senaryoları

### Senaryo 1: Yeni Corpus Oluşturma
1. **Veritabanı Oluştur**:
   - "Veritabanı Oluştur" butonuna tıklayın
   - İstediğiniz dosya adını girin (örn: `my_corpus.db`)
   
2. **Metin Klasörü Seç**:
   - "Gözat" ile metin dosyalarınızın bulunduğu klasörü seçin
   - Backend olarak `simple` seçin (en güvenilir)

3. **İçeri Aktar**:
   - "Corpus'u İçeri Aktar" butonuna tıklayın
   - İşlem tamamlanana kadar bekleyin
   - Durum çubuğundan ilerlemeyi takip edin

### Senaryo 2: KWIC Analizi
1. **Analiz Türü**: "kwic" seçin
2. **Aranacak Kelime**: İlgili kelimeyi girin (örn: "ev")
3. **Pencere Boyutu**: 5 (standart)
4. **Analiz Yap**: Butona tıklayın
5. **Sonuçları Görün**: Sol bağlam + [kelime] + sağ bağlam

### Senaryo 3: Frekans Analizi
1. **Analiz Türü**: "frequency" seçin
2. **Analiz Yap**: Butona tıklayın
3. **Sonuçları İnceleyin**: En sık kullanılan kelimeler listesi

### Senaryo 4: Collocation Analizi
1. **Analiz Türü**: "collocation" seçin
2. **Hedef Kelime**: Analiz edilecek kelime (örn: "okul")
3. **Pencere Boyutu**: 3-5 arası önerilir
4. **Analiz Yap**: PMI skorları ile collocation listesi

### Senaryo 5: Word Sketch
1. **Analiz Türü**: "word_sketch" seçin
2. **Lemma**: Analiz edilecek lemma (örn: "ev")
3. **Analiz Yap**: Dependency relations gösterilir

### Senaryo 6: Corpus Düzenleme (YENİ!)
1. **Corpus Düzenleme Sekmesine Geçin**: Üst sekmeden "Corpus Düzenleme"yi seçin
2. **Dosya Açın**: 
   - "Dosya Aç" butonuna tıklayın
   - Düzenlemek istediğiniz .txt dosyasını seçin
   - Metin düzenleyicide içeriği göreceksiniz
3. **Metni Düzenleyin**:
   - Metni istediğiniz gibi değiştirin
   - Türkçe karakter desteği tam
   - Kaydırma çubuğu ile uzun metinler
4. **Değişiklikleri Kaydedin**:
   - "Kaydet" butonuna tıklayın
   - Dosya diske kaydedilir
5. **Veritabanını Güncelleyin**:
   - "Veritabanını Güncelle" butonuna tıklayın
   - Metin NLP işlenir ve veritabanına eklenir
   - Durum çubuğundan ilerlemeyi takip edin
6. **Devam Edin**: Düzenlenen metin artık analiz edilebilir

### Senaryo 7: Analiz Sonuçlarını Dışa Aktarma (YENİ!)
1. **Analiz Yapın**: İstediğiniz analizi çalıştırın (KWIC, Frekans, vb.)
2. **Sonuçlar Sekmesine Geçin**: "Sonuçlar" sekmesine gidin
3. **Dışa Aktar Butonuna Tıklayın**: "Sonuçları Kaydet" butonuna tıklayın
4. **Format Seçin**: 
   - **TXT**: Basit metin olarak kaydet
   - **JSON**: Yapısal veri olarak kaydet (düzenleme için ideal)
   - **XML**: Web standardı formatında kaydet
   - **Veritabanı**: SQLite tablosu olarak kaydet
5. **Dosya Yolunu Seçin**: Kaydedilecek konumu belirtin
6. **Sonucu Kontrol Edin**: Dosyanın doğru kaydedildiğini kontrol edin

### Senaryo 8: Kaydedilen Dosyaları Düzenleme (YENİ!)
1. **Dosya Düzenleme Sekmesine Geçin**: "Dosya Düzenleme" sekmesine gidin
2. **Dosya Türü Seçin**:
   - **JSON Aç**: Önceki JSON export dosyalarını düzenleme
   - **XML Aç**: XML formatındaki dosyaları düzenleme
   - **TXT Aç**: Metin dosyalarını düzenleme
3. **Düzenleme Yapın**: İçeriği istediğiniz gibi değiştirin
4. **Doğrula**: JSON/XML için format doğruluğunu kontrol edin
5. **Kaydet**: Değişiklikleri diske kaydedin

### Senaryo 9: Veritabanı Dışa Aktarma
1. **Analiz Yapın**: Herhangi bir analiz türü seçin
2. **Dışa Aktar**: "Veritabanı" formatını seçin
3. **Veritabanı Dosyası Seçin**: Yeni veya mevcut .db dosyasını belirtin
4. **Tablo İnceleyin**: SQLite browser ile tabloyu görüntüleyin
5. **SQL Sorguları**: Veriler üzerinde SQL sorguları çalıştırın

### Senaryo 10: Yeni Corpus Oluşturma

## 🔧 İleri Düzey Kullanım

### Backend Seçimi
- **simple**: En hızlı, en güvenilir (önerilen)
- **spaCy**: En doğru sonuçlar (Python 3.13 gerekli)
- **custom_bert**: Kendi modeliniz için

### Performans Optimizasyonu
- **Büyük Dosyalar**: Batch processing otomatik
- **Bellek Kullanımı**: 1000 token/batch
- **Çoklu İş Parçacığı**: GUI donmaz
- **Hata Toleransı**: Kesintisiz işlem

### Sonuçları Kaydetme
1. Analizi tamamlayın
2. "Sonuçları Kaydet" butonuna tıklayın
3. Dosya adını ve konumunu seçin
4. TXT formatında kaydedilir

## ⚠️ Hata Durumları ve Çözümler

### Sık Karşılaşılan Hatalar

#### 1. "Veritabanı bulunamadı"
**Çözüm**: 
- Önce "Veritabanı Oluştur" butonuna tıklayın
- Geçerli bir dosya yolu seçin

#### 2. "Metin klasörü seçilmedi"
**Çözüm**:
- "Gözat" butonu ile klasör seçin
- Klasörde .txt dosyaları olduğundan emin olun

#### 3. "Analiz yapılamadı"
**Çözüm**:
- Corpus'un önce içeri aktarıldığından emin olun
- Backend olarak `simple` seçin

#### 4. "Hata oluştu" mesajları
**Çözüm**:
- Terminal/komut penceresindeki hata mesajlarını kontrol edin
- Gerekirse `simple` backend kullanın

### Hata Mesajları
- **Bilgilendirici**: Ne yapılması gerektiği açık
- **Ayrıntılı**: Teknik detaylar verilir
- **Çözüm Önerileri**: Ne yapılacağı belirtilir

## 📱 Kullanıcı Deneyimi

### Tasarım Özellikleri
- **Modern Görünüm**: Clean, minimal arayüz
- **Responsive**: Pencere boyutuna uyum
- **Accessible**: Kolay navigasyon
- **Intuitive**: Sezgisel kullanım

### Etkileşim Özellikleri
- **Hover Efektleri**: Butonlar canlı
- **Status Feedback**: Gerçek zamanlı bilgi
- **Progress Indication**: İşlem ilerlemesi
- **Error Handling**: Kullanıcı dostu hatalar

### Klavye Kısayolları
- **Tab**: Alanlar arası geçiş
- **Enter**: Seçili butonu çalıştır
- **Escape**: Açık diyalogları kapat

## 🎯 En İyi Uygulamalar

### Başlangıç İçin
1. **Demo Verilerle Başlayın**: `sample_turkish_corpus` klasörünü kullanın
2. **Simple Backend**: İlk denemelerde `simple` seçin
3. **Küçük Dosyalar**: Test için küçük metinlerle başlayın

### Verimli Kullanım
1. **Organize Edin**: Metin dosyalarınızı klasörleyin
2. **Anlamlı İsimler**: Veritabanı dosyalarına açıklayıcı isimler verin
3. **Düzenli Kayıt**: Sonuçları düzenli olarak kaydedin

### Sorun Giderme
1. **Terminal Kontrol**: Hata mesajları için komut penceresini izleyin
2. **Basit Backend**: Sorun yaşarsanız `simple` kullanın
3. **Temiz Başlangıç**: Yeni veritabanı oluşturun

## 🚀 GUI Başlatma Seçenekleri

### Seçenek 1: Standart Başlatma
```bash
py run_gui.py
```

### Seçenek 2: Python ile
```bash
python run_gui.py
```

### Seçenek 3: Doğrudan GUI
```bash
python gui/corpus_gui.py
```

## 💡 İpuçları ve Püf Noktaları

1. **İlk Kullanım**: `demo_fixed.py` çalıştırarak sistemi test edin
2. **Büyük Korpuslar**: İşlem uzun sürebilir, sabırlı olun
3. **Sonuçları Kaydet**: Analiz sonuçlarını mutlaka kaydedin
4. **Farklı Backend'ler**: Sonuçları karşılaştırmak için farklı backend'ler deneyin
5. **Düzenli Backup**: Veritabanı dosyalarınızı yedekleyin

**GUI ile Corpus Data Manipulator'ın tüm gücünü kolayca kullanabilirsiniz!**