import json
import os

def convert_corpus_to_label_studio(input_path, output_path):
    """
    Corpus verisini (JSONL) Label Studio 'import' formatına dönüştürür.
    Token bazlı UPOS etiketlerini 'predictions' olarak ekler.
    """
    ls_tasks = []
    
    print(f"İşleniyor: {input_path}")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines):
            if not line.strip():
                continue
                
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"Hata: {line_num + 1}. satır geçerli bir JSON değil, atlanıyor.")
                continue

            text = data.get('text', '')
            tokens = data.get('tokens', [])
            
            # Label Studio için 'prediction' (tahmin/ön etiket) oluşturma
            results = []
            cursor = 0 # Metin içinde aramaya başlanacak konum
            
            for token in tokens:
                word = token.get('form')
                label = token.get('upos')
                
                if not word:
                    continue
                
                # Kelimeyi metin içinde bul
                # Cursor kullanarak aynı kelimenin tekrarında sıradakini bulmayı garanti ederiz
                start_index = text.find(word, cursor)
                
                if start_index != -1:
                    end_index = start_index + len(word)
                    
                    # Eğer etiket varsa sonuca ekle
                    if label:
                        results.append({
                            "from_name": "label",
                            "to_name": "text",
                            "type": "labels",
                            "value": {
                                "start": start_index,
                                "end": end_index,
                                "text": word,
                                "labels": [label] # Label Studio liste bekler
                            }
                        })
                    
                    # Cursor'ı kelimenin bitişine taşı
                    cursor = end_index
                else:
                    # Token metin içinde bulunamadıysa (nadiren olur, veri hatası)
                    # Sadece loglayıp devam ediyoruz, cursor'ı oynatmıyoruz
                    # print(f"Uyarı: '{word}' kelimesi metin içinde bulunamadı. (Satır {line_num+1})")
                    pass

            # Label Studio Task Objesi
            task = {
                "data": {
                    "text": text,
                    "doc_name": data.get('doc_name', ''),
                    "sent_id": data.get('sent_id')
                },
                # Tahminleri ekle (Modelin bulduğu etiketler olarak görünür)
                "predictions": [{
                    "model_version": "corpus_v1",
                    "score": 1.0, # Güven skoru
                    "result": results
                }]
            }
            ls_tasks.append(task)
            
        # Çıktıyı kaydet
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ls_tasks, f, ensure_ascii=False, indent=2)
            
        print(f"Başarılı! {len(ls_tasks)} veri dönüştürüldü.")
        print(f"Oluşturulan dosya: {output_path}")
        print("Bu dosyayı Label Studio'ya 'Import' edebilirsiniz.")

    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    input_file = os.path.join("label_studio_setup", "raw_data.jsonl")
    output_file = os.path.join("label_studio_setup", "ready_for_label_studio.json")
    
    # Dosya yollarını kontrol et
    if not os.path.exists(input_file):
        # Script eğer farklı yerden çalıştırılırsa diye kontrol
        input_file = "raw_data.jsonl"
        output_file = "ready_for_label_studio.json"
    
    if os.path.exists(input_file):
        convert_corpus_to_label_studio(input_file, output_file)
    else:
        print(f"Girdi dosyası bulunamadı: {input_file}")
