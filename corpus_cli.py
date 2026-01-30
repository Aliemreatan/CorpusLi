import argparse
import json
import sys
import os
from typing import List, Dict, Any

# Proje dizinini path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query.corpus_query import CorpusQuery

class CorpusCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Corpus Manipulator CLI - Veri Yönetim Aracı",
            formatter_class=argparse.RawTextHelpFormatter
        )
        self.setup_commands()

    def setup_commands(self):
        subparsers = self.parser.add_subparsers(dest='command', help='Komutlar')

        # Export Komutu
        export_parser = subparsers.add_parser('export', help='Veriyi dışa aktarır')
        export_parser.add_argument('output', help='Çıktı dosyasının yolu (örn: data.json)')
        export_parser.add_argument('--format', choices=['json', 'jsonl'], default='json', 
                                   help='Çıktı formatı: json (liste) veya jsonl (satır satır). Varsayılan: json')
        export_parser.add_argument('--db', default='corpus.db', help='Veritabanı dosyası')

    def run(self):
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return

        if args.command == 'export':
            self.export_data(args.db, args.output, args.format)

    def export_data(self, db_path, output_path, output_format):
        print(f"Veritabanına bağlanılıyor: {db_path}...")
        try:
            cq = CorpusQuery(db_path)
        except Exception as e:
            print(f"Hata: Veritabanı açılamadı. {e}")
            return

        print("Veri çekiliyor ve işleniyor...")
        
        # Generator'ı başlat
        token_stream = cq.get_all_tokens_for_export()
        
        current_sentence = None
        sentence_count = 0
        
        try:
            # Dosyayı yazma modunda aç
            with open(output_path, 'w', encoding='utf-8') as f:
                
                # Eğer JSON ise liste başını yaz
                if output_format == 'json':
                    f.write('[\n')
                
                first_item = True
                
                for row, is_new_sentence in token_stream:
                    # row indexleri: 
                    # 0:sent_id, 1:token_number, 2:form, 3:lemma, 4:upos, 5:xpos, 
                    # 6:morph, 7:dep_head, 8:dep_rel, 9:sent_text, 10:doc_name
                    
                    if is_new_sentence:
                        # Önceki cümleyi kaydet (eğer varsa)
                        if current_sentence:
                            self._write_sentence(f, current_sentence, output_format, first_item)
                            first_item = False
                            sentence_count += 1
                            
                            if sentence_count % 1000 == 0:
                                print(f"\rİşlenen cümle sayısı: {sentence_count}", end="")

                        # Yeni cümleyi başlat
                        current_sentence = {
                            "sent_id": row[0],
                            "doc_name": row[10],
                            "text": row[9],
                            "tokens": []
                        }
                    
                    # Token verisini ekle
                    token = {
                        "id": row[1],
                        "form": row[2],
                        "lemma": row[3],
                        "upos": row[4],
                        "xpos": row[5],
                        "head": row[7],
                        "dep_rel": row[8]
                    }
                    current_sentence["tokens"].append(token)
                
                # Son cümleyi kaydet
                if current_sentence:
                    self._write_sentence(f, current_sentence, output_format, first_item)
                    sentence_count += 1
                
                # Eğer JSON ise liste sonunu yaz
                if output_format == 'json':
                    f.write('\n]')
                    
            print(f"\n\nBaşarılı! Toplam {sentence_count} cümle dışa aktarıldı.")
            print(f"Dosya: {output_path}")
            
        except Exception as e:
            print(f"\nBir hata oluştu: {e}")
        finally:
            cq.close()

    def _write_sentence(self, file_obj, sentence_data, fmt, is_first):
        if fmt == 'json':
            if not is_first:
                file_obj.write(',\n')
            json.dump(sentence_data, file_obj, ensure_ascii=False)
        else: # jsonl
            file_obj.write(json.dumps(sentence_data, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    cli = CorpusCLI()
    cli.run()
