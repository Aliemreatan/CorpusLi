# Türkçe POS Tagger Karşılaştırma Raporu

*Rapor Tarihi: 2026-01-06 21:40:42*

## 1. Hız Performansı (2000 karakterlik metin üzerinde)
| Model | Süre (saniye) | Durum |
|-------|---------------|-------|
| Project_Simple | 0.0003 | ✅ Aktif |
| Project_CustomBERT | 0.0807 | ✅ Aktif |
| Extra_Stanza | 0.2008 | ✅ Aktif |
| Extra_Zeyrek | 0.0988 | ✅ Aktif |

## 2. Model Detayları
- **Project_Simple:** Regex ve kural tabanlı basit yaklaşım.
- **Project_SpaCy:** SpaCy `tr_core_news_sm` modeli.
- **Project_CustomBERT:** Projedeki `LiProject/Bert-turkish-pos-trained`.
- **Extra_OzcanBert:** HuggingFace `ozcangundes/bert-base-turkish-cased-pos`.
- **Extra_Stanza:** Stanford NLP `stanza` kütüphanesi (Türkçe modeli).
- **Extra_Zeyrek:** Zemberek'in Python portu (Morfolojik Analiz).

## 3. Detaylı Cümle Analizleri
Aşağıda her bir örnek cümlenin farklı modeller tarafından nasıl etiketlendiği gösterilmiştir:

### Cümle 1: "Çayın kenarında oturup sıcak bir çay içtik."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | çayın/NOUN | kenarında/NOUN | oturup/NOUN | sıcak/NOUN | bir/NUM | çay/NOUN | içtik/NOUN |
| **Project_CustomBERT** | Çayın/AD-NOUN | kenarında/AD-NOUN | oturup/FİİL-VERB | sıcak/SIFAT-ADJECTIVE | bir/BELİRLEYİCİ-DET | çay/AD-NOUN | içtik/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Çayın/NOUN | kenarında/ADJ | oturup/VERB | sıcak/ADJ | bir/DET | çay/NOUN | içtik/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Çayın', lemma='Çay', pos='Noun', morphemes=['Noun', 'A3sg', 'Gen'], formatted='[Çay:Noun,Prop] çay:Noun+A3sg+ın:Gen')/ERROR | Parse(word='kenarında', lemma='kenar', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Loc'], formatted='[kenar:Noun] kenar:Noun+A3sg+ın:P2sg+da:Loc')/ERROR | Parse(word='oturup', lemma='oturmak', pos='Adv', morphemes=['Verb', 'AfterDoingSo', 'Adv'], formatted='[oturmak:Verb] otur:Verb|up:AfterDoingSo→Adv')/ERROR | Parse(word='sıcak', lemma='sıcak', pos='Adj', morphemes=['Adj'], formatted='[sıcak:Adj] sıcak:Adj')/ERROR | Parse(word='bir', lemma='bir', pos='Adj', morphemes=['Adj'], formatted='[bir:Adj] bir:Adj')/ERROR | Parse(word='çay', lemma='Çay', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[Çay:Noun,Prop] çay:Noun+A3sg')/ERROR | Parse(word='içtik', lemma='içmek', pos='Verb', morphemes=['Verb', 'Past', 'A1pl'], formatted='[içmek:Verb] iç:Verb+ti:Past+k:A1pl')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 2: "Yüz kere söyledim, şu yastığın kılıfını yüz."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Yüz/NUM | kere/NOUN | söyledim/NOUN | şu/PRON | yastığın/NOUN | kılıfını/NOUN | yüz/NUM |
| **Project_CustomBERT** | Yüz/SIFAT-ADJECTIVE | kere/AD-NOUN | söyledim/FİİL-VERB | ,/NOKTALAMA-PUNCTUATION | şu/BELİRLEYİCİ-DET | yastığın/AD-NOUN | kılıfını/AD-NOUN | yüz/AD-NOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Yüz/NUM | kere/NOUN | söyledim/VERB | ,/PUNCT | şu/DET | yastığın/NOUN | kılıfını/NOUN | yüz/AUX | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Yüz', lemma='yüz', pos='Num', morphemes=['Num'], formatted='[yüz:Num,Card] yüz:Num')/ERROR | Parse(word='kere', lemma='ker', pos='Noun', morphemes=['Noun', 'A3sg', 'Dat'], formatted='[ker:Noun] ker:Noun+A3sg+e:Dat')/ERROR | Parse(word='söyledim', lemma='söylemek', pos='Verb', morphemes=['Verb', 'Past', 'A1sg'], formatted='[söylemek:Verb] söyle:Verb+di:Past+m:A1sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='şu', lemma='şu', pos='Adj', morphemes=['Adj'], formatted='[şu:Adj] şu:Adj')/ERROR | Parse(word='yastığın', lemma='yasmak', pos='Adj', morphemes=['Verb', 'PastPart', 'Adj', 'P2sg'], formatted='[yasmak:Verb] yas:Verb|tığ:PastPart→Adj+ın:P2sg')/ERROR | Parse(word='kılıfını', lemma='kılıf', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Acc'], formatted='[kılıf:Noun] kılıf:Noun+A3sg+ın:P2sg+ı:Acc')/ERROR | Parse(word='yüz', lemma='yüz', pos='Num', morphemes=['Num'], formatted='[yüz:Num,Card] yüz:Num')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 3: "Bu yaz, bana sık sık mektup yaz."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Bu/PRON | yaz/NOUN | bana/NOUN | sık/NOUN | sık/NOUN | mektup/NOUN | yaz/NOUN |
| **Project_CustomBERT** | Bu/BELİRLEYİCİ-DET | yaz/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | bana/ADIL-PRONOUN | sık/BELİRTEÇ-ADVERB | sık/BELİRTEÇ-ADVERB | mektup/AD-NOUN | yaz/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Bu/DET | yaz/NOUN | ,/PUNCT | bana/PRON | sık/ADV | sık/ADJ | mektup/NOUN | yaz/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Bu', lemma='bu', pos='Det', morphemes=['Det'], formatted='[bu:Det] bu:Det')/ERROR | Parse(word='yaz', lemma='yazmak', pos='Verb', morphemes=['Verb', 'Imp', 'A2sg'], formatted='[yazmak:Verb] yaz:Verb+Imp+A2sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='bana', lemma='banmak', pos='Verb', morphemes=['Verb', 'Opt', 'A3sg'], formatted='[banmak:Verb] ban:Verb+a:Opt+A3sg')/ERROR | Parse(word='sık', lemma='sık', pos='Adj', morphemes=['Adj'], formatted='[sık:Adj] sık:Adj')/ERROR | Parse(word='sık', lemma='sık', pos='Adj', morphemes=['Adj'], formatted='[sık:Adj] sık:Adj')/ERROR | Parse(word='mektup', lemma='mektup', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[mektup:Noun] mektup:Noun+A3sg')/ERROR | Parse(word='yaz', lemma='yazmak', pos='Verb', morphemes=['Verb', 'Imp', 'A2sg'], formatted='[yazmak:Verb] yaz:Verb+Imp+A2sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 4: "Ocak ayında yeni bir ocak satın aldık."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Ocak/NOUN | ayında/NOUN | yeni/NOUN | bir/NUM | ocak/NOUN | satın/NOUN | aldık/NOUN |
| **Project_CustomBERT** | Ocak/AD-NOUN | ayında/AD-NOUN | yeni/SIFAT-ADJECTIVE | bir/BELİRLEYİCİ-DET | ocak/AD-NOUN | satın/AD-NOUN | aldık/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Ocak/NOUN | ayında/NOUN | yeni/ADJ | bir/DET | ocak/NOUN | satın/ADV | aldık/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Ocak', lemma='ocak', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[ocak:Noun] ocak:Noun+A3sg')/ERROR | Parse(word='ayında', lemma='ay', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Loc'], formatted='[ay:Noun] ay:Noun+A3sg+ın:P2sg+da:Loc')/ERROR | Parse(word='yeni', lemma='yeni', pos='Adj', morphemes=['Adj'], formatted='[yeni:Adj] yeni:Adj')/ERROR | Parse(word='bir', lemma='bir', pos='Adj', morphemes=['Adj'], formatted='[bir:Adj] bir:Adj')/ERROR | Parse(word='ocak', lemma='ocak', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[ocak:Noun] ocak:Noun+A3sg')/ERROR | Parse(word='satın', lemma='satmak', pos='Verb', morphemes=['Verb', 'Imp', 'A2pl'], formatted='[satmak:Verb] sat:Verb+Imp+ın:A2pl')/ERROR | Parse(word='aldık', lemma='almak', pos='Verb', morphemes=['Verb', 'Past', 'A1pl'], formatted='[almak:Verb] al:Verb+dı:Past+k:A1pl')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 5: "Kır saçlı adam, odunları dizinde kır."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Kır/NOUN | saçlı/NOUN | adam/NOUN | odunları/NOUN | dizinde/NOUN | kır/NOUN |
| **Project_CustomBERT** | Kır/SIFAT-ADJECTIVE | saçlı/SIFAT-ADJECTIVE | adam/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | odunları/AD-NOUN | dizinde/AD-NOUN | kır/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Kır/NOUN | saçlı/ADJ | adam/NOUN | ,/PUNCT | odunları/NOUN | dizinde/NOUN | kır/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Kır', lemma='kır', pos='Adj', morphemes=['Adj'], formatted='[kır:Adj] kır:Adj')/ERROR | Parse(word='saçlı', lemma='saç', pos='Adj', morphemes=['Noun', 'A3sg', 'With', 'Adj'], formatted='[saç:Noun] saç:Noun+A3sg|lı:With→Adj')/ERROR | Parse(word='adam', lemma='ada', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg'], formatted='[ada:Noun] ada:Noun+A3sg+m:P1sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='odunları', lemma='odun', pos='Noun', morphemes=['Noun', 'A3pl', 'Acc'], formatted='[odun:Noun] odun:Noun+lar:A3pl+ı:Acc')/ERROR | Parse(word='dizinde', lemma='diz', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Loc'], formatted='[diz:Noun] diz:Noun+A3sg+in:P2sg+de:Loc')/ERROR | Parse(word='kır', lemma='kır', pos='Adj', morphemes=['Adj'], formatted='[kır:Adj] kır:Adj')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 6: "Atı alan Üsküdar'ı geçti, sen o taşı at."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Atı/VERB | alan/NOUN | üsküdar/NOUN | ı/NOUN | geçti/VERB | sen/PRON | o/PRON | taşı/NOUN | at/NOUN |
| **Project_CustomBERT** | Atı/AD-NOUN | alan/FİİL-VERB | Üsküdar'ı/AD-NOUN | geçti/FİİL-VERB | ,/NOKTALAMA-PUNCTUATION | sen/ADIL-PRONOUN | o/BELİRLEYİCİ-DET | taşı/AD-NOUN | at/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Atı/NOUN | alan/VERB | Üsküdar'ı/PROPN | geçti/VERB | ,/PUNCT | sen/PRON | o/DET | taşı/NOUN | at/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Atı', lemma='at', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[at:Noun] at:Noun+A3sg+ı:Acc')/ERROR | Parse(word='alan', lemma='ala', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg'], formatted='[ala:Noun] ala:Noun+A3sg+n:P2sg')/ERROR | Parse(word='Üsküdarı', lemma='Üsküdar', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[Üsküdar:Noun,Prop] üsküdar:Noun+A3sg+ı:Acc')/ERROR | Parse(word='geçti', lemma='geçmek', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[geçmek:Verb] geç:Verb+ti:Past+A3sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='sen', lemma='se', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg'], formatted='[se:Noun] se:Noun+A3sg+n:P2sg')/ERROR | Parse(word='o', lemma='o', pos='Det', morphemes=['Det'], formatted='[o:Det] o:Det')/ERROR | Parse(word='taşı', lemma='taşımak', pos='Verb', morphemes=['Verb', 'Imp', 'A2sg'], formatted='[taşımak:Verb] taşı:Verb+Imp+A2sg')/ERROR | Parse(word='at', lemma='atmak', pos='Verb', morphemes=['Verb', 'Imp', 'A2sg'], formatted='[atmak:Verb] at:Verb+Imp+A2sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 7: "Ben bu benleri yüzümden aldırmak istiyorum."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Ben/PRON | bu/PRON | benleri/NOUN | yüzümden/NOUN | aldırmak/VERB | istiyorum/NOUN |
| **Project_CustomBERT** | Ben/ADIL-PRONOUN | bu/BELİRLEYİCİ-DET | benleri/AD-NOUN | yüzümden/AD-NOUN | aldırmak/FİİL-VERB | istiyorum/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Ben/PRON | bu/DET | benleri/PRON | yüzümden/NOUN | aldırmak/VERB | istiyorum/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Ben', lemma='ben', pos='Pron', morphemes=['Pron', 'A1sg'], formatted='[ben:Pron,Pers] ben:Pron+A1sg')/ERROR | Parse(word='bu', lemma='bu', pos='Det', morphemes=['Det'], formatted='[bu:Det] bu:Det')/ERROR | Parse(word='benleri', lemma='ben', pos='Noun', morphemes=['Noun', 'A3sg', 'P3pl'], formatted='[ben:Noun] ben:Noun+A3sg+leri:P3pl')/ERROR | Parse(word='yüzümden', lemma='yüz', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg', 'Abl'], formatted='[yüz:Noun] yüz:Noun+A3sg+üm:P1sg+den:Abl')/ERROR | Parse(word='aldırmak', lemma='aldırmak', pos='Noun', morphemes=['Verb', 'Inf1', 'Noun', 'A3sg'], formatted='[aldırmak:Verb] aldır:Verb|mak:Inf1→Noun+A3sg')/ERROR | Parse(word='istiyorum', lemma='istemek', pos='Verb', morphemes=['Verb', 'Prog1', 'A1sg'], formatted='[istemek:Verb] ist:Verb+iyor:Prog1+um:A1sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 8: "Kaz gelecek yerden tavuk esirgenmez, toprağı kaz."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Kaz/NOUN | gelecek/VERB | yerden/NOUN | tavuk/NOUN | esirgenmez/NOUN | toprağı/NOUN | kaz/NOUN |
| **Project_CustomBERT** | Kaz/AD-NOUN | gelecek/SIFAT-ADJECTIVE | yerden/AD-NOUN | tavuk/AD-NOUN | esirgenmez/FİİL-VERB | ,/NOKTALAMA-PUNCTUATION | toprağı/AD-NOUN | kaz/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Kaz/NOUN | gelecek/VERB | yerden/NOUN | tavuk/NOUN | esirgenmez/VERB | ,/PUNCT | toprağı/NOUN | kaz/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Kaz', lemma='kaz', pos='Adj', morphemes=['Adj'], formatted='[kaz:Adj] kaz:Adj')/ERROR | Parse(word='gelecek', lemma='gelecek', pos='Adj', morphemes=['Adj'], formatted='[gelecek:Adj] gelecek:Adj')/ERROR | Parse(word='yerden', lemma='yer', pos='Noun', morphemes=['Noun', 'A3sg', 'Abl'], formatted='[yer:Noun] yer:Noun+A3sg+den:Abl')/ERROR | Parse(word='tavuk', lemma='tavuk', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[tavuk:Noun] tavuk:Noun+A3sg')/ERROR | Parse(word='esirgenmez', lemma='esirgemek', pos='Verb', morphemes=['Verb', 'Pass', 'Verb', 'Neg', 'Aor', 'A3sg'], formatted='[esirgemek:Verb] esirge:Verb|n:Pass→Verb+me:Neg+z:Aor+A3sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='toprağı', lemma='toprak', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[toprak:Noun] toprağ:Noun+A3sg+ı:Acc')/ERROR | Parse(word='kaz', lemma='kaz', pos='Adj', morphemes=['Adj'], formatted='[kaz:Adj] kaz:Adj')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 9: "Dolu yağarken bardak tamamen dolu muydu?"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Dolu/NOUN | yağarken/NOUN | bardak/NOUN | tamamen/NOUN | dolu/NOUN | muydu/VERB |
| **Project_CustomBERT** | Dolu/BELİRTEÇ-ADVERB | yağarken/FİİL-VERB | bardak/AD-NOUN | tamamen/BELİRTEÇ-ADVERB | dolu/FİİL-VERB | muydu/FİİL-VERB | ?/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Dolu/ADJ | yağarken/VERB | bardak/NOUN | tamamen/ADV | dolu/ADJ | muydu/AUX | ?/PUNCT |
| **Extra_Zeyrek** | Parse(word='Dolu', lemma='dolu', pos='Adj', morphemes=['Adj'], formatted='[dolu:Adj] dolu:Adj')/ERROR | Parse(word='yağarken', lemma='yağmak', pos='Adv', morphemes=['Verb', 'Aor', 'While', 'Adv'], formatted='[yağmak:Verb] yağ:Verb+ar:Aor|ken:While→Adv')/ERROR | Parse(word='bardak', lemma='bardak', pos='Adj', morphemes=['Adj'], formatted='[bardak:Adj] bardak:Adj')/ERROR | Parse(word='tamamen', lemma='tamamen', pos='Adv', morphemes=['Adv'], formatted='[tamamen:Adv] tamamen:Adv')/ERROR | Parse(word='dolu', lemma='dolu', pos='Adj', morphemes=['Adj'], formatted='[dolu:Adj] dolu:Adj')/ERROR | Parse(word='muydu', lemma='mu', pos='Ques', morphemes=['Ques', 'Past', 'A3sg'], formatted='[mu:Ques] mu:Ques+ydu:Past+A3sg')/ERROR | Parse(word='?', lemma='?', pos='Punc', morphemes=['Punc'], formatted='[?:Punc] ?:Punc')/ERROR |

---

### Cümle 10: "Kara görününce gemidekiler kara kara düşünmeye başladı."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Kara/NOUN | görününce/NOUN | gemidekiler/NOUN | kara/NOUN | kara/NOUN | düşünmeye/NOUN | başladı/VERB |
| **Project_CustomBERT** | Kara/AD-NOUN | görününce/FİİL-VERB | gemidekiler/AD-NOUN | kara/BELİRTEÇ-ADVERB | kara/BELİRTEÇ-ADVERB | düşünmeye/FİİL-VERB | başladı/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Kara/ADJ | görününce/VERB | gemideki/VERB | ler/ADP | kara/ADJ | kara/ADJ | düşünmeye/VERB | başladı/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Kara', lemma='kara', pos='Adj', morphemes=['Adj'], formatted='[kara:Adj] kara:Adj')/ERROR | Parse(word='görününce', lemma='görünmek', pos='Adv', morphemes=['Verb', 'When', 'Adv'], formatted='[görünmek:Verb] görün:Verb|ünce:When→Adv')/ERROR | Parse(word='gemidekiler', lemma='gemi', pos='Verb', morphemes=['Noun', 'A3sg', 'Loc', 'Rel', 'Adj', 'Zero', 'Verb', 'Pres', 'A3pl'], formatted='[gemi:Noun] gemi:Noun+A3sg+de:Loc|ki:Rel→Adj|Zero→Verb+Pres+ler:A3pl')/ERROR | Parse(word='kara', lemma='kara', pos='Adj', morphemes=['Adj'], formatted='[kara:Adj] kara:Adj')/ERROR | Parse(word='kara', lemma='kara', pos='Adj', morphemes=['Adj'], formatted='[kara:Adj] kara:Adj')/ERROR | Parse(word='düşünmeye', lemma='düşünmek', pos='Verb', morphemes=['Verb', 'Neg', 'Opt', 'A3sg'], formatted='[düşünmek:Verb] düşün:Verb+me:Neg+ye:Opt+A3sg')/ERROR | Parse(word='başladı', lemma='başlamak', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[başlamak:Verb] başla:Verb+dı:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 11: "Kara kızın kısa kayışını kasışına kızmayışına şaşmamışsın da, kuru kazın kızıp kayısı kazışına şaşmış kalmışsın."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Kara/NOUN | kızın/NOUN | kısa/NOUN | kayışını/NOUN | kasışına/NOUN | kızmayışına/NOUN | şaşmamışsın/NOUN | da/NOUN | kuru/NOUN | kazın/NOUN | kızıp/NOUN | kayısı/NOUN | kazışına/NOUN | şaşmış/VERB | kalmışsın/NOUN |
| **Project_CustomBERT** | Kara/SIFAT-ADJECTIVE | kızın/AD-NOUN | kısa/SIFAT-ADJECTIVE | kayışını/AD-NOUN | kasışına/FİİL-VERB | kızmayışına/FİİL-VERB | şaşmamışsın/FİİL-VERB | da/BAĞLAÇ-CONJ | ,/NOKTALAMA-PUNCTUATION | kuru/SIFAT-ADJECTIVE | kazın/AD-NOUN | kızıp/FİİL-VERB | kayısı/AD-NOUN | kazışına/AD-NOUN | şaşmış/FİİL-VERB | kalmışsın/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Kara/ADJ | kızın/ADJ | kısa/ADJ | kayışını/NOUN | kasışına/NOUN | kızmayışına/VERB | şaşmamışsın/VERB | da/CCONJ | ,/PUNCT | kuru/ADJ | kazın/NOUN | kızıp/VERB | kayısı/NOUN | kazışına/NOUN | şaşmış/VERB | kalmışsın/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Kara', lemma='kara', pos='Adj', morphemes=['Adj'], formatted='[kara:Adj] kara:Adj')/ERROR | Parse(word='kızın', lemma='kızmak', pos='Verb', morphemes=['Verb', 'Imp', 'A2pl'], formatted='[kızmak:Verb] kız:Verb+Imp+ın:A2pl')/ERROR | Parse(word='kısa', lemma='kısa', pos='Adv', morphemes=['Adv'], formatted='[kısa:Adv] kısa:Adv')/ERROR | Parse(word='kayışını', lemma='kayış', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Acc'], formatted='[kayış:Noun] kayış:Noun+A3sg+ın:P2sg+ı:Acc')/ERROR | Parse(word='kasışına', lemma='kasmak', pos='Noun', morphemes=['Verb', 'Inf3', 'Noun', 'A3sg', 'P2sg', 'Dat'], formatted='[kasmak:Verb] kas:Verb|ış:Inf3→Noun+A3sg+ın:P2sg+a:Dat')/ERROR | Parse(word='kızmayışına', lemma='kızmak', pos='Noun', morphemes=['Verb', 'Neg', 'Inf3', 'Noun', 'A3sg', 'P2sg', 'Dat'], formatted='[kızmak:Verb] kız:Verb+ma:Neg|yış:Inf3→Noun+A3sg+ın:P2sg+a:Dat')/ERROR | Parse(word='şaşmamışsın', lemma='şaşmak', pos='Verb', morphemes=['Verb', 'Neg', 'Narr', 'A2sg'], formatted='[şaşmak:Verb] şaş:Verb+ma:Neg+mış:Narr+sın:A2sg')/ERROR | Parse(word='da', lemma='da', pos='Conj', morphemes=['Conj'], formatted='[da:Conj] da:Conj')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='kuru', lemma='kuru', pos='Adj', morphemes=['Adj'], formatted='[kuru:Adj] kuru:Adj')/ERROR | Parse(word='kazın', lemma='kazmak', pos='Verb', morphemes=['Verb', 'Imp', 'A2pl'], formatted='[kazmak:Verb] kaz:Verb+Imp+ın:A2pl')/ERROR | Parse(word='kızıp', lemma='kızmak', pos='Adv', morphemes=['Verb', 'AfterDoingSo', 'Adv'], formatted='[kızmak:Verb] kız:Verb|ıp:AfterDoingSo→Adv')/ERROR | Parse(word='kayısı', lemma='Kayı', pos='Noun', morphemes=['Noun', 'A3sg', 'P3sg'], formatted='[Kayı:Noun,Prop] kayı:Noun+A3sg+sı:P3sg')/ERROR | Parse(word='kazışına', lemma='kazmak', pos='Noun', morphemes=['Verb', 'Inf3', 'Noun', 'A3sg', 'P2sg', 'Dat'], formatted='[kazmak:Verb] kaz:Verb|ış:Inf3→Noun+A3sg+ın:P2sg+a:Dat')/ERROR | Parse(word='şaşmış', lemma='şaşmak', pos='Adj', morphemes=['Verb', 'NarrPart', 'Adj'], formatted='[şaşmak:Verb] şaş:Verb|mış:NarrPart→Adj')/ERROR | Parse(word='kalmışsın', lemma='kalmak', pos='Verb', morphemes=['Verb', 'Narr', 'A2sg'], formatted='[kalmak:Verb] kal:Verb+mış:Narr+sın:A2sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 12: "Hızlı araba yolda hızlı gidiyordu."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Hızlı/NOUN | araba/NOUN | yolda/NOUN | hızlı/NOUN | gidiyordu/VERB |
| **Project_CustomBERT** | Hızlı/SIFAT-ADJECTIVE | araba/AD-NOUN | yolda/AD-NOUN | hızlı/BELİRTEÇ-ADVERB | gidiyordu/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Hızlı/ADJ | araba/NOUN | yolda/NOUN | hızlı/ADJ | gidiyordu/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Hızlı', lemma='hızlı', pos='Adj', morphemes=['Adj'], formatted='[hızlı:Adj] hızlı:Adj')/ERROR | Parse(word='araba', lemma='araba', pos='Adj', morphemes=['Adj'], formatted='[araba:Adj] araba:Adj')/ERROR | Parse(word='yolda', lemma='yol', pos='Noun', morphemes=['Noun', 'A3sg', 'Loc'], formatted='[yol:Noun] yol:Noun+A3sg+da:Loc')/ERROR | Parse(word='hızlı', lemma='hızlı', pos='Adj', morphemes=['Adj'], formatted='[hızlı:Adj] hızlı:Adj')/ERROR | Parse(word='gidiyordu', lemma='gitmek', pos='Verb', morphemes=['Verb', 'Prog1', 'Past', 'A3sg'], formatted='[gitmek:Verb] gid:Verb+iyor:Prog1+du:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 13: "Güzel konuşan insan güzel düşünür."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Güzel/NOUN | konuşan/NOUN | insan/NOUN | güzel/NOUN | düşünür/NOUN |
| **Project_CustomBERT** | Güzel/BELİRTEÇ-ADVERB | konuşan/SIFAT-ADJECTIVE | insan/AD-NOUN | güzel/BELİRTEÇ-ADVERB | düşünür/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Güzel/ADJ | konuşan/VERB | insan/NOUN | güzel/ADJ | düşünür/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Güzel', lemma='güzel', pos='Adj', morphemes=['Adj'], formatted='[güzel:Adj] güzel:Adj')/ERROR | Parse(word='konuşan', lemma='konuşmak', pos='Adj', morphemes=['Verb', 'PresPart', 'Adj'], formatted='[konuşmak:Verb] konuş:Verb|an:PresPart→Adj')/ERROR | Parse(word='insan', lemma='insan', pos='Adj', morphemes=['Adj'], formatted='[insan:Adj] insan:Adj')/ERROR | Parse(word='güzel', lemma='güzel', pos='Adj', morphemes=['Adj'], formatted='[güzel:Adj] güzel:Adj')/ERROR | Parse(word='düşünür', lemma='düşünmek', pos='Verb', morphemes=['Verb', 'Aor', 'A3sg'], formatted='[düşünmek:Verb] düşün:Verb+ür:Aor+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 14: "Doğru insanla doğru zamanda karşılaşmak zordur."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Doğru/NOUN | insanla/NOUN | doğru/NOUN | zamanda/NOUN | karşılaşmak/VERB | zordur/NOUN |
| **Project_CustomBERT** | Doğru/SIFAT-ADJECTIVE | insanla/AD-NOUN | doğru/SIFAT-ADJECTIVE | zamanda/AD-NOUN | karşılaşmak/FİİL-VERB | zordur/SIFAT-ADJECTIVE | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Doğru/ADJ | insanla/NOUN | doğru/ADJ | zamanda/NOUN | karşılaşmak/VERB | zor/ADJ | dur/AUX | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Doğru', lemma='doğru', pos='Adj', morphemes=['Adj'], formatted='[doğru:Adj] doğru:Adj')/ERROR | Parse(word='insanla', lemma='İnsa', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Ins'], formatted='[İnsa:Noun,Prop] insa:Noun+A3sg+n:P2sg+la:Ins')/ERROR | Parse(word='doğru', lemma='doğru', pos='Adj', morphemes=['Adj'], formatted='[doğru:Adj] doğru:Adj')/ERROR | Parse(word='zamanda', lemma='zaman', pos='Noun', morphemes=['Noun', 'A3sg', 'Loc'], formatted='[zaman:Noun,Time] zaman:Noun+A3sg+da:Loc')/ERROR | Parse(word='karşılaşmak', lemma='karşı', pos='Noun', morphemes=['Adj', 'Become', 'Verb', 'Inf1', 'Noun', 'A3sg'], formatted='[karşı:Adj] karşı:Adj|laş:Become→Verb|mak:Inf1→Noun+A3sg')/ERROR | Parse(word='zordur', lemma='zor', pos='Verb', morphemes=['Adj', 'Zero', 'Verb', 'Pres', 'A3sg', 'Cop'], formatted='[zor:Adj] zor:Adj|Zero→Verb+Pres+A3sg+dur:Cop')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 15: "Tahtayı doğru kessen iyi olurdu."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Tahtayı/NOUN | doğru/NOUN | kessen/NOUN | iyi/NOUN | olurdu/VERB |
| **Project_CustomBERT** | Tahtayı/AD-NOUN | doğru/BELİRTEÇ-ADVERB | kessen/FİİL-VERB | iyi/SIFAT-ADJECTIVE | olurdu/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Tahtayı/NOUN | doğru/ADJ | kessen/VERB | iyi/ADJ | olurdu/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Tahtayı', lemma='tahta', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[tahta:Noun] tahta:Noun+A3sg+yı:Acc')/ERROR | Parse(word='doğru', lemma='doğru', pos='Adj', morphemes=['Adj'], formatted='[doğru:Adj] doğru:Adj')/ERROR | Parse(word='kessen', lemma='kesmek', pos='Verb', morphemes=['Verb', 'Desr', 'A2sg'], formatted='[kesmek:Verb] kes:Verb+se:Desr+n:A2sg')/ERROR | Parse(word='iyi', lemma='iyi', pos='Adv', morphemes=['Adv'], formatted='[iyi:Adv] iyi:Adv')/ERROR | Parse(word='olurdu', lemma='olmak', pos='Verb', morphemes=['Verb', 'Aor', 'Past', 'A3sg'], formatted='[olmak:Verb] ol:Verb+ur:Aor+du:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 16: "Yalnız adam, evde yalnız yaşıyordu."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Yalnız/NOUN | adam/NOUN | evde/NOUN | yalnız/NOUN | yaşıyordu/VERB |
| **Project_CustomBERT** | Yalnız/SIFAT-ADJECTIVE | adam/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | evde/AD-NOUN | yalnız/BELİRTEÇ-ADVERB | yaşıyordu/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Yalnız/ADV | adam/NOUN | ,/PUNCT | evde/NOUN | yalnız/ADV | yaşıyordu/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Yalnız', lemma='yalnız', pos='Adv', morphemes=['Adv'], formatted='[yalnız:Adv] yalnız:Adv')/ERROR | Parse(word='adam', lemma='ada', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg'], formatted='[ada:Noun] ada:Noun+A3sg+m:P1sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='evde', lemma='ev', pos='Noun', morphemes=['Noun', 'A3sg', 'Loc'], formatted='[ev:Noun] ev:Noun+A3sg+de:Loc')/ERROR | Parse(word='yalnız', lemma='yalnız', pos='Adv', morphemes=['Adv'], formatted='[yalnız:Adv] yalnız:Adv')/ERROR | Parse(word='yaşıyordu', lemma='yaşamak', pos='Verb', morphemes=['Verb', 'Prog1', 'Past', 'A3sg'], formatted='[yaşamak:Verb] yaş:Verb+ıyor:Prog1+du:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 17: "Genç, yaşlılara yer verdi."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Genç/NOUN | yaşlılara/NOUN | yer/NOUN | verdi/VERB |
| **Project_CustomBERT** | Genç/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | yaşlılara/AD-NOUN | yer/AD-NOUN | verdi/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Genç/ADJ | ,/PUNCT | yaşlılara/ADJ | yer/NOUN | verdi/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Genç', lemma='genç', pos='Adj', morphemes=['Adj'], formatted='[genç:Adj] genç:Adj')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='yaşlılara', lemma='yaş', pos='Noun', morphemes=['Noun', 'A3sg', 'With', 'Adj', 'Zero', 'Noun', 'A3pl', 'Dat'], formatted='[yaş:Noun] yaş:Noun+A3sg|lı:With→Adj|Zero→Noun+lar:A3pl+a:Dat')/ERROR | Parse(word='yer', lemma='yemek', pos='Verb', morphemes=['Verb', 'Aor', 'A3sg'], formatted='[yemek:Verb] ye:Verb+r:Aor+A3sg')/ERROR | Parse(word='verdi', lemma='vermek', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[vermek:Verb] ver:Verb+di:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 18: "Hasta çocuk hasta yatağında yatıyor."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Hasta/NOUN | çocuk/NOUN | hasta/NOUN | yatağında/NOUN | yatıyor/VERB |
| **Project_CustomBERT** | Hasta/SIFAT-ADJECTIVE | çocuk/AD-NOUN | hasta/SIFAT-ADJECTIVE | yatağında/AD-NOUN | yatıyor/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Hasta/NOUN | çocuk/NOUN | hasta/ADJ | yatağında/NOUN | yatıyor/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Hasta', lemma='hasta', pos='Adj', morphemes=['Adj'], formatted='[hasta:Adj] hasta:Adj')/ERROR | Parse(word='çocuk', lemma='çocuk', pos='Adj', morphemes=['Adj'], formatted='[çocuk:Adj] çocuk:Adj')/ERROR | Parse(word='hasta', lemma='hasta', pos='Adj', morphemes=['Adj'], formatted='[hasta:Adj] hasta:Adj')/ERROR | Parse(word='yatağında', lemma='yatak', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Loc'], formatted='[yatak:Noun] yatağ:Noun+A3sg+ın:P2sg+da:Loc')/ERROR | Parse(word='yatıyor', lemma='yatmak', pos='Verb', morphemes=['Verb', 'Prog1', 'A3sg'], formatted='[yatmak:Verb] yat:Verb+ıyor:Prog1+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 19: "Gidiyorum gündüz gece, bilmiyorum ne haldeyim."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Gidiyorum/NOUN | gündüz/NOUN | gece/NOUN | bilmiyorum/NOUN | ne/NOUN | haldeyim/NOUN |
| **Project_CustomBERT** | Gidiyorum/FİİL-VERB | gündüz/BELİRTEÇ-ADVERB | gece/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | bilmiyorum/FİİL-VERB | ne/SORU-QUESTION | haldeyim/AD-NOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Gidiyorum/VERB | gündüz/NOUN | gece/NOUN | ,/PUNCT | bilmiyorum/VERB | ne/PRON | halde/NOUN | yim/AUX | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Gidiyorum', lemma='gitmek', pos='Verb', morphemes=['Verb', 'Prog1', 'A1sg'], formatted='[gitmek:Verb] gid:Verb+iyor:Prog1+um:A1sg')/ERROR | Parse(word='gündüz', lemma='gündüz', pos='Adv', morphemes=['Adv'], formatted='[gündüz:Adv] gündüz:Adv')/ERROR | Parse(word='gece', lemma='gece', pos='Adv', morphemes=['Adv'], formatted='[gece:Adv] gece:Adv')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='bilmiyorum', lemma='bilmek', pos='Verb', morphemes=['Verb', 'Neg', 'Prog1', 'A1sg'], formatted='[bilmek:Verb] bil:Verb+m:Neg+iyor:Prog1+um:A1sg')/ERROR | Parse(word='ne', lemma='ne', pos='Interj', morphemes=['Interj'], formatted='[ne:Interj] ne:Interj')/ERROR | Parse(word='haldeyim', lemma='hâl', pos='Verb', morphemes=['Noun', 'A3sg', 'Loc', 'Zero', 'Verb', 'Pres', 'A1sg'], formatted='[hâl:Noun] hal:Noun+A3sg+de:Loc|Zero→Verb+Pres+yim:A1sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 20: "Sakla samanı, gelir zamanı."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Sakla/NOUN | samanı/NOUN | gelir/NOUN | zamanı/NOUN |
| **Project_CustomBERT** | Sakla/FİİL-VERB | samanı/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | gelir/FİİL-VERB | zamanı/AD-NOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Sakla/NOUN | samanı/NOUN | ,/PUNCT | gelir/NOUN | zamanı/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Sakla', lemma='saklamak', pos='Verb', morphemes=['Verb', 'Imp', 'A2sg'], formatted='[saklamak:Verb] sakla:Verb+Imp+A2sg')/ERROR | Parse(word='samanı', lemma='saman', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[saman:Noun] saman:Noun+A3sg+ı:Acc')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='gelir', lemma='gelir', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[gelir:Noun] gelir:Noun+A3sg')/ERROR | Parse(word='zamanı', lemma='zaman', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[zaman:Noun,Time] zaman:Noun+A3sg+ı:Acc')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 21: "Ağır ağır çıkacaksın bu merdivenlerden."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Ağır/NOUN | ağır/NOUN | çıkacaksın/NOUN | bu/PRON | merdivenlerden/NOUN |
| **Project_CustomBERT** | Ağır/BELİRTEÇ-ADVERB | ağır/BELİRTEÇ-ADVERB | çıkacaksın/FİİL-VERB | bu/BELİRLEYİCİ-DET | merdivenlerden/AD-NOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Ağır/ADJ | ağır/ADJ | çıkacaksın/VERB | bu/DET | merdivenlerden/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Ağır', lemma='ağır', pos='Adv', morphemes=['Adv'], formatted='[ağır:Adv] ağır:Adv')/ERROR | Parse(word='ağır', lemma='ağır', pos='Adv', morphemes=['Adv'], formatted='[ağır:Adv] ağır:Adv')/ERROR | Parse(word='çıkacaksın', lemma='çıkmak', pos='Verb', morphemes=['Verb', 'Fut', 'A2sg'], formatted='[çıkmak:Verb] çık:Verb+acak:Fut+sın:A2sg')/ERROR | Parse(word='bu', lemma='bu', pos='Det', morphemes=['Det'], formatted='[bu:Det] bu:Det')/ERROR | Parse(word='merdivenlerden', lemma='merdiven', pos='Noun', morphemes=['Noun', 'A3pl', 'Abl'], formatted='[merdiven:Noun] merdiven:Noun+ler:A3pl+den:Abl')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 22: "Görmedim ömrümde böyle bir rezalet."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Görmedim/NOUN | ömrümde/NOUN | böyle/NOUN | bir/NUM | rezalet/NOUN |
| **Project_CustomBERT** | Görmedim/FİİL-VERB | ömrümde/AD-NOUN | böyle/BELİRLEYİCİ-DET | bir/BELİRLEYİCİ-DET | rezalet/AD-NOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Görmedim/VERB | ömrümde/NOUN | böyle/ADJ | bir/DET | rezalet/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Görmedim', lemma='görmek', pos='Verb', morphemes=['Verb', 'Neg', 'Past', 'A1sg'], formatted='[görmek:Verb] gör:Verb+me:Neg+di:Past+m:A1sg')/ERROR | Parse(word='ömrümde', lemma='ömür', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg', 'Loc'], formatted='[ömür:Noun] ömr:Noun+A3sg+üm:P1sg+de:Loc')/ERROR | Parse(word='böyle', lemma='böyle', pos='Adj', morphemes=['Adj'], formatted='[böyle:Adj] böyle:Adj')/ERROR | Parse(word='bir', lemma='bir', pos='Adj', morphemes=['Adj'], formatted='[bir:Adj] bir:Adj')/ERROR | Parse(word='rezalet', lemma='rezalet', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[rezalet:Noun] rezalet:Noun+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 23: "Severim fırtınalı havalarda denizi izlemeyi."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Severim/NOUN | fırtınalı/NOUN | havalarda/NOUN | denizi/NOUN | izlemeyi/NOUN |
| **Project_CustomBERT** | Severim/FİİL-VERB | fırtınalı/SIFAT-ADJECTIVE | havalarda/AD-NOUN | denizi/AD-NOUN | izlemeyi/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Severim/VERB | fırtınalı/ADJ | havalarda/NOUN | denizi/NOUN | izlemeyi/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Severim', lemma='sevmek', pos='Verb', morphemes=['Verb', 'Aor', 'A1sg'], formatted='[sevmek:Verb] sev:Verb+er:Aor+im:A1sg')/ERROR | Parse(word='fırtınalı', lemma='fırtına', pos='Adj', morphemes=['Noun', 'A3sg', 'With', 'Adj'], formatted='[fırtına:Noun] fırtına:Noun+A3sg|lı:With→Adj')/ERROR | Parse(word='havalarda', lemma='hava', pos='Noun', morphemes=['Noun', 'A3pl', 'Loc'], formatted='[hava:Noun] hava:Noun+lar:A3pl+da:Loc')/ERROR | Parse(word='denizi', lemma='de', pos='Noun', morphemes=['Noun', 'A3sg', 'P2pl', 'Acc'], formatted='[de:Noun] de:Noun+A3sg+niz:P2pl+i:Acc')/ERROR | Parse(word='izlemeyi', lemma='izlemek', pos='Noun', morphemes=['Verb', 'Inf2', 'Noun', 'A3sg', 'Acc'], formatted='[izlemek:Verb] izle:Verb|me:Inf2→Noun+A3sg+yi:Acc')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 24: "Anlatamıyorum derdimi kimselere."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Anlatamıyorum/NOUN | derdimi/NOUN | kimselere/NOUN |
| **Project_CustomBERT** | Anlatamıyorum/FİİL-VERB | derdimi/AD-NOUN | kimselere/ADIL-PRONOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Anlatamıyorum/VERB | derdimi/NOUN | kimselere/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Anlatamıyorum', lemma='anlatmak', pos='Verb', morphemes=['Verb', 'Unable', 'Prog1', 'A1sg'], formatted='[anlatmak:Verb] anlat:Verb+am:Unable+ıyor:Prog1+um:A1sg')/ERROR | Parse(word='derdimi', lemma='dert', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg', 'Acc'], formatted='[dert:Noun] derd:Noun+A3sg+im:P1sg+i:Acc')/ERROR | Parse(word='kimselere', lemma='kimse', pos='Pron', morphemes=['Pron', 'A3pl', 'Dat'], formatted='[kimse:Pron,Quant] kimse:Pron+ler:A3pl+e:Dat')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 25: "Çekoslovakyalılaştıramadıklarımızdan mısınız?"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | çekoslovakyalılaştıramadıklarımızdan/NOUN | mısınız/NOUN |
| **Project_CustomBERT** | Çekoslovakyalılaştıramadıklarımızdan/AD-NOUN | mısınız/SORU-QUESTION | ?/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Çekoslovakyalılaştıramadıklarımızdan/NOUN | mısınız/AUX | ?/PUNCT |
| **Extra_Zeyrek** | Parse(word='Çekoslovakyalılaştıramadıklarımızdan', lemma='Çekoslovakyalı', pos='Noun', morphemes=['Noun', 'A3sg', 'Become', 'Verb', 'Caus', 'Verb', 'Unable', 'PastPart', 'Noun', 'A3pl', 'P1pl', 'Abl'], formatted='[Çekoslovakyalı:Noun,Prop] çekoslovakyalı:Noun+A3sg|laş:Become→Verb|tır:Caus→Verb+ama:Unable|dık:PastPart→Noun+lar:A3pl+ımız:P1pl+dan:Abl')/ERROR | Parse(word='mısınız', lemma='mı', pos='Ques', morphemes=['Ques', 'Pres', 'A2pl'], formatted='[mı:Ques] mı:Ques+Pres+sınız:A2pl')/ERROR | Parse(word='?', lemma='?', pos='Punc', morphemes=['Punc'], formatted='[?:Punc] ?:Punc')/ERROR |

---

### Cümle 26: "Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine/NOUN |
| **Project_CustomBERT** | Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine/SIFAT-ADJECTIVE | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Muvaffakiyetsizleştiricileştiriveremeyebileceklerimizdenmişsinizcesine', lemma='Unk', pos='Unk', morphemes='Unk', formatted='Unk')/ERROR |

---

### Cümle 27: "Evdeki hesap çarşıya uymaz."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Evdeki/NOUN | hesap/NOUN | çarşıya/NOUN | uymaz/NOUN |
| **Project_CustomBERT** | Evdeki/AD-NOUN | hesap/AD-NOUN | çarşıya/AD-NOUN | uymaz/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Evde/NOUN | ki/ADP | hesap/NOUN | çarşıya/NOUN | uymaz/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Evdeki', lemma='ev', pos='Adj', morphemes=['Noun', 'A3sg', 'Loc', 'Rel', 'Adj'], formatted='[ev:Noun] ev:Noun+A3sg+de:Loc|ki:Rel→Adj')/ERROR | Parse(word='hesap', lemma='hesap', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[hesap:Noun] hesap:Noun+A3sg')/ERROR | Parse(word='çarşıya', lemma='çarşı', pos='Noun', morphemes=['Noun', 'A3sg', 'Dat'], formatted='[çarşı:Noun] çarşı:Noun+A3sg+ya:Dat')/ERROR | Parse(word='uymaz', lemma='uymaz', pos='Adj', morphemes=['Adj'], formatted='[uymaz:Adj] uymaz:Adj')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 28: "Gözlükçüden aldığım gözlüğü gözlüğümün kabına koydum."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Gözlükçüden/NOUN | aldığım/NOUN | gözlüğü/NOUN | gözlüğümün/NOUN | kabına/NOUN | koydum/NOUN |
| **Project_CustomBERT** | Gözlükçüden/AD-NOUN | aldığım/SIFAT-ADJECTIVE | gözlüğü/AD-NOUN | gözlüğümün/AD-NOUN | kabına/AD-NOUN | koydum/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Gözlükçüden/NOUN | aldığım/VERB | gözlüğü/NOUN | gözlüğümün/NOUN | kabına/NOUN | koydum/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Gözlükçüden', lemma='gözlük', pos='Noun', morphemes=['Noun', 'A3sg', 'Agt', 'Noun', 'A3sg', 'Abl'], formatted='[gözlük:Noun] gözlük:Noun+A3sg|çü:Agt→Noun+A3sg+den:Abl')/ERROR | Parse(word='aldığım', lemma='almak', pos='Adj', morphemes=['Verb', 'PastPart', 'Adj', 'P1sg'], formatted='[almak:Verb] al:Verb|dığ:PastPart→Adj+ım:P1sg')/ERROR | Parse(word='gözlüğü', lemma='gözlük', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[gözlük:Noun] gözlüğ:Noun+A3sg+ü:Acc')/ERROR | Parse(word='gözlüğümün', lemma='gözlük', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg', 'Gen'], formatted='[gözlük:Noun] gözlüğ:Noun+A3sg+üm:P1sg+ün:Gen')/ERROR | Parse(word='kabına', lemma='kâp', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Dat'], formatted='[kâp:Noun] kab:Noun+A3sg+ın:P2sg+a:Dat')/ERROR | Parse(word='koydum', lemma='koymak', pos='Verb', morphemes=['Verb', 'Past', 'A1sg'], formatted='[koymak:Verb] koy:Verb+du:Past+m:A1sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 29: "Kitaplıktaki kitapları kitapçığa kaydettim."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Kitaplıktaki/NOUN | kitapları/NOUN | kitapçığa/NOUN | kaydettim/NOUN |
| **Project_CustomBERT** | Kitaplıktaki/AD-NOUN | kitapları/AD-NOUN | kitapçığa/AD-NOUN | kaydettim/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Kitaplıkta/NOUN | ki/ADP | kitapları/NOUN | kitapçığa/NOUN | kaydettim/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Kitaplıktaki', lemma='Kitap', pos='Adj', morphemes=['Noun', 'A3sg', 'Ness', 'Noun', 'A3sg', 'Loc', 'Rel', 'Adj'], formatted='[Kitap:Noun,Prop] kitap:Noun+A3sg|lık:Ness→Noun+A3sg+ta:Loc|ki:Rel→Adj')/ERROR | Parse(word='kitapları', lemma='Kitap', pos='Noun', morphemes=['Noun', 'A3sg', 'P3pl'], formatted='[Kitap:Noun,Prop] kitap:Noun+A3sg+ları:P3pl')/ERROR | Parse(word='kitapçığa', lemma='Kitap', pos='Noun', morphemes=['Noun', 'A3sg', 'Dim', 'Noun', 'A3sg', 'Dat'], formatted='[Kitap:Noun,Prop] kitap:Noun+A3sg|çığ:Dim→Noun+A3sg+a:Dat')/ERROR | Parse(word='kaydettim', lemma='kaydetmek', pos='Verb', morphemes=['Verb', 'Past', 'A1sg'], formatted='[kaydetmek:Verb] kaydet:Verb+ti:Past+m:A1sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 30: "Sen de mi Brütüs?"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Sen/PRON | de/NOUN | mi/NOUN | Brütüs/NOUN |
| **Project_CustomBERT** | Sen/ADIL-PRONOUN | de/BAĞLAÇ-CONJ | mi/SORU-QUESTION | Brütüs/AD-NOUN | ?/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Sen/PRON | de/CCONJ | mi/AUX | Brütüs/NOUN | ?/PUNCT |
| **Extra_Zeyrek** | Parse(word='Sen', lemma='se', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg'], formatted='[se:Noun] se:Noun+A3sg+n:P2sg')/ERROR | Parse(word='de', lemma='de', pos='Conj', morphemes=['Conj'], formatted='[de:Conj] de:Conj')/ERROR | Parse(word='mi', lemma='mi', pos='Ques', morphemes=['Ques', 'Pres', 'A3sg'], formatted='[mi:Ques] mi:Ques+Pres+A3sg')/ERROR | Parse(word='Brütüs', lemma='Brütüs', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[Brütüs:Noun,Prop] brütüs:Noun+A3sg')/ERROR | Parse(word='?', lemma='?', pos='Punc', morphemes=['Punc'], formatted='[?:Punc] ?:Punc')/ERROR |

---

### Cümle 31: "Ah, elim yandı!"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Ah/NOUN | elim/NOUN | yandı/VERB |
| **Project_CustomBERT** | Ah/BELİRTEÇ-ADVERB | ,/NOKTALAMA-PUNCTUATION | elim/AD-NOUN | yandı/FİİL-VERB | !/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Ah/INTJ | ,/PUNCT | elim/NOUN | yandı/VERB | !/PUNCT |
| **Extra_Zeyrek** | Parse(word='Ah', lemma='ah', pos='Interj', morphemes=['Interj'], formatted='[ah:Interj] ah:Interj')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='elim', lemma='elim', pos='Adj', morphemes=['Adj'], formatted='[elim:Adj] elim:Adj')/ERROR | Parse(word='yandı', lemma='yanmak', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[yanmak:Verb] yan:Verb+dı:Past+A3sg')/ERROR | Parse(word='!', lemma='!', pos='Punc', morphemes=['Punc'], formatted='[!:Punc] !:Punc')/ERROR |

---

### Cümle 32: "Eyvah, otobüsü kaçırdım!"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Eyvah/NOUN | otobüsü/NOUN | kaçırdım/NOUN |
| **Project_CustomBERT** | Eyvah/BELİRTEÇ-ADVERB | ,/NOKTALAMA-PUNCTUATION | otobüsü/AD-NOUN | kaçırdım/FİİL-VERB | !/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Eyvah/PROPN | ,/PUNCT | otobüsü/NOUN | kaçırdım/VERB | !/PUNCT |
| **Extra_Zeyrek** | Parse(word='Eyvah', lemma='eyvah', pos='Interj', morphemes=['Interj'], formatted='[eyvah:Interj] eyvah:Interj')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='otobüsü', lemma='otobüs', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[otobüs:Noun] otobüs:Noun+A3sg+ü:Acc')/ERROR | Parse(word='kaçırdım', lemma='kaçırmak', pos='Verb', morphemes=['Verb', 'Past', 'A1sg'], formatted='[kaçırmak:Verb] kaçır:Verb+dı:Past+m:A1sg')/ERROR | Parse(word='!', lemma='!', pos='Punc', morphemes=['Punc'], formatted='[!:Punc] !:Punc')/ERROR |

---

### Cümle 33: "Bunu sana kim söyledi, Ali mi Veli mi?"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Bunu/NOUN | sana/NOUN | kim/NOUN | söyledi/VERB | Ali/NOUN | mi/NOUN | Veli/NOUN | mi/NOUN |
| **Project_CustomBERT** | Bunu/ADIL-PRONOUN | sana/ADIL-PRONOUN | kim/SORU-QUESTION | söyledi/FİİL-VERB | ,/NOKTALAMA-PUNCTUATION | Ali/AD-NOUN | mi/SORU-QUESTION | Veli/AD-NOUN | mi/SORU-QUESTION | ?/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Bunu/PRON | sana/PRON | kim/PRON | söyledi/VERB | ,/PUNCT | Ali/PROPN | mi/AUX | Veli/PROPN | mi/AUX | ?/PUNCT |
| **Extra_Zeyrek** | Parse(word='Bunu', lemma='bu', pos='Pron', morphemes=['Pron', 'A3sg', 'Acc'], formatted='[bu:Pron,Demons] bu:Pron+A3sg+nu:Acc')/ERROR | Parse(word='sana', lemma='sanmak', pos='Verb', morphemes=['Verb', 'Opt', 'A3sg'], formatted='[sanmak:Verb] san:Verb+a:Opt+A3sg')/ERROR | Parse(word='kim', lemma='kim', pos='Conj', morphemes=['Conj'], formatted='[kim:Conj] kim:Conj')/ERROR | Parse(word='söyledi', lemma='söylemek', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[söylemek:Verb] söyle:Verb+di:Past+A3sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='Ali', lemma='ali', pos='Adj', morphemes=['Adj'], formatted='[ali:Adj] ali:Adj')/ERROR | Parse(word='mi', lemma='mi', pos='Ques', morphemes=['Ques', 'Pres', 'A3sg'], formatted='[mi:Ques] mi:Ques+Pres+A3sg')/ERROR | Parse(word='Veli', lemma='veli', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[veli:Noun] veli:Noun+A3sg')/ERROR | Parse(word='mi', lemma='mi', pos='Ques', morphemes=['Ques', 'Pres', 'A3sg'], formatted='[mi:Ques] mi:Ques+Pres+A3sg')/ERROR | Parse(word='?', lemma='?', pos='Punc', morphemes=['Punc'], formatted='[?:Punc] ?:Punc')/ERROR |

---

### Cümle 34: "Neden benimle gelmedin, korktun mu?"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Neden/NOUN | benimle/NOUN | gelmedin/NOUN | korktun/NOUN | mu/NOUN |
| **Project_CustomBERT** | Neden/SORU-QUESTION | benimle/ADIL-PRONOUN | gelmedin/FİİL-VERB | ,/NOKTALAMA-PUNCTUATION | korktun/FİİL-VERB | mu/SORU-QUESTION | ?/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Neden/PRON | benimle/PRON | gelmedin/VERB | ,/PUNCT | korktun/VERB | mu/AUX | ?/PUNCT |
| **Extra_Zeyrek** | Parse(word='Neden', lemma='neden', pos='Adv', morphemes=['Adv'], formatted='[neden:Adv] neden:Adv')/ERROR | Parse(word='benimle', lemma='ben', pos='Pron', morphemes=['Pron', 'A1sg', 'Ins'], formatted='[ben:Pron,Pers] ben:Pron+A1sg+imle:Ins')/ERROR | Parse(word='gelmedin', lemma='gelmek', pos='Verb', morphemes=['Verb', 'Neg', 'Past', 'A2sg'], formatted='[gelmek:Verb] gel:Verb+me:Neg+di:Past+n:A2sg')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='korktun', lemma='korkmak', pos='Verb', morphemes=['Verb', 'Past', 'A2sg'], formatted='[korkmak:Verb] kork:Verb+tu:Past+n:A2sg')/ERROR | Parse(word='mu', lemma='mu', pos='Ques', morphemes=['Ques', 'Pres', 'A3sg'], formatted='[mu:Ques] mu:Ques+Pres+A3sg')/ERROR | Parse(word='?', lemma='?', pos='Punc', morphemes=['Punc'], formatted='[?:Punc] ?:Punc')/ERROR |

---

### Cümle 35: "Türkiye'nin başkenti Ankara'dır ve Anıtkabir oradadır."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Türkiye/NOUN | nin/NOUN | başkenti/VERB | Ankara/NOUN | dır/NOUN | ve/CCONJ | Anıtkabir/NOUN | oradadır/NOUN |
| **Project_CustomBERT** | Türkiye'nin/AD-NOUN | başkenti/AD-NOUN | Ankara'dır/AD-NOUN | ve/BAĞLAÇ-CONJ | Anıtkabir/AD-NOUN | oradadır/ADIL-PRONOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Türkiye'nin/PROPN | başkenti/NOUN | Ankara/PROPN | 'dır/AUX | ve/CCONJ | Anıtkabir/NOUN | orada/NOUN | dır/AUX | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Türkiyenin', lemma='Türkiye', pos='Noun', morphemes=['Noun', 'A3sg', 'Gen'], formatted='[Türkiye:Noun,Prop] türkiye:Noun+A3sg+nin:Gen')/ERROR | Parse(word='başkenti', lemma='başkent', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[başkent:Noun] başkent:Noun+A3sg+i:Acc')/ERROR | Parse(word='Ankaradır', lemma='Ankara', pos='Verb', morphemes=['Noun', 'A3sg', 'Zero', 'Verb', 'Pres', 'A3sg', 'Cop'], formatted='[Ankara:Noun,Prop] ankara:Noun+A3sg|Zero→Verb+Pres+A3sg+dır:Cop')/ERROR | Parse(word='ve', lemma='ve', pos='Conj', morphemes=['Conj'], formatted='[ve:Conj] ve:Conj')/ERROR | Parse(word='Anıtkabir', lemma='Anıtkabir', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[Anıtkabir:Noun,Prop] anıtkabir:Noun+A3sg')/ERROR | Parse(word='oradadır', lemma='ora', pos='Verb', morphemes=['Noun', 'A3sg', 'Loc', 'Zero', 'Verb', 'Pres', 'A3sg', 'Cop'], formatted='[ora:Noun] ora:Noun+A3sg+da:Loc|Zero→Verb+Pres+A3sg+dır:Cop')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 36: "TBMM'nin açılış tarihi 23 Nisan 1920'dir."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | TBMM/NOUN | nin/NOUN | açılış/NOUN | tarihi/NOUN | 23/NOUN | Nisan/NOUN | 1920/NOUN | dir/NOUN |
| **Project_CustomBERT** | TBMM'nin/AD-NOUN | açılış/AD-NOUN | tarihi/AD-NOUN | 23/AD-NOUN | Nisan/AD-NOUN | 1920'dir/AD-NOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | TBMM'nin/NOUN | açılış/NOUN | tarihi/NOUN | 23/NUM | Nisan/NOUN | 1920/NUM | 'dir/AUX | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='TBMMnin', lemma='Tbmm', pos='Noun', morphemes=['Noun', 'A3sg', 'Gen'], formatted='[Tbmm:Noun,Abbrv] tbmm:Noun+A3sg+nin:Gen')/ERROR | Parse(word='açılış', lemma='açmak', pos='Noun', morphemes=['Verb', 'Pass', 'Verb', 'Inf3', 'Noun', 'A3sg'], formatted='[açmak:Verb] aç:Verb|ıl:Pass→Verb|ış:Inf3→Noun+A3sg')/ERROR | Parse(word='tarihi', lemma='tarihî', pos='Adj', morphemes=['Adj'], formatted='[tarihî:Adj] tarihi:Adj')/ERROR | Parse(word='23', lemma='Unk', pos='Unk', morphemes='Unk', formatted='Unk')/ERROR |

---

### Cümle 37: "Ayşe'nin kedisi Minnoş, Van Gölü'ne düştü."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Ayşe/NOUN | nin/NOUN | kedisi/NOUN | Minnoş/NOUN | Van/NOUN | Gölü/NOUN | ne/NOUN | düştü/VERB |
| **Project_CustomBERT** | Ayşe'nin/AD-NOUN | kedisi/AD-NOUN | Minnoş/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | Van/AD-NOUN | Gölü'ne/AD-NOUN | düştü/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Ayşe'nin/PROPN | kedisi/NOUN | Minnoş/PROPN | ,/PUNCT | Van/PROPN | Gölü'ne/NOUN | düştü/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Ayşenin', lemma='Ayşe', pos='Noun', morphemes=['Noun', 'A3sg', 'Gen'], formatted='[Ayşe:Noun,Prop] ayşe:Noun+A3sg+nin:Gen')/ERROR | Parse(word='kedisi', lemma='kedi', pos='Noun', morphemes=['Noun', 'A3sg', 'P3sg'], formatted='[kedi:Noun] kedi:Noun+A3sg+si:P3sg')/ERROR | Parse(word='Minnoş', lemma='minnoş', pos='Interj', morphemes=['Interj'], formatted='[minnoş:Interj] minnoş:Interj')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='Van', lemma='Van', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[Van:Noun,Prop] van:Noun+A3sg')/ERROR | Parse(word='Gölüne', lemma='göl', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Dat'], formatted='[göl:Noun] göl:Noun+A3sg+ün:P2sg+e:Dat')/ERROR | Parse(word='düştü', lemma='düşmek', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[düşmek:Verb] düş:Verb+tü:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 38: "İngilizce'yi ve Almanca'yı aynı anda öğreniyor."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | ingilizce/NOUN | yi/NOUN | ve/CCONJ | Almanca/NOUN | yı/NOUN | aynı/NOUN | anda/NOUN | öğreniyor/VERB |
| **Project_CustomBERT** | İngilizce'yi/AD-NOUN | ve/BAĞLAÇ-CONJ | Almanca'yı/AD-NOUN | aynı/SIFAT-ADJECTIVE | anda/AD-NOUN | öğreniyor/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | İngilizce'yi/ADJ | ve/CCONJ | Almanca'yı/ADJ | aynı/ADJ | anda/NOUN | öğreniyor/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='İngilizceyi', lemma='İngilizce', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[İngilizce:Noun,Prop] ingilizce:Noun+A3sg+yi:Acc')/ERROR | Parse(word='ve', lemma='ve', pos='Conj', morphemes=['Conj'], formatted='[ve:Conj] ve:Conj')/ERROR | Parse(word='Almancayı', lemma='Almanca', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[Almanca:Noun,Prop] almanca:Noun+A3sg+yı:Acc')/ERROR | Parse(word='aynı', lemma='aynı', pos='Adj', morphemes=['Adj'], formatted='[aynı:Adj] aynı:Adj')/ERROR | Parse(word='anda', lemma='an', pos='Noun', morphemes=['Noun', 'A3sg', 'Loc'], formatted='[an:Noun,Time] an:Noun+A3sg+da:Loc')/ERROR | Parse(word='öğreniyor', lemma='öğrenmek', pos='Verb', morphemes=['Verb', 'Prog1', 'A3sg'], formatted='[öğrenmek:Verb] öğren:Verb+iyor:Prog1+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 39: "Dr. Ahmet Bey, Prof. Dr. Mehmet ile görüştü."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Dr/NOUN | Ahmet/NOUN | Bey/NOUN | Prof/NOUN | Dr/NOUN | Mehmet/NOUN | ile/CCONJ | görüştü/VERB |
| **Project_CustomBERT** | Dr/AD-NOUN | ./NOKTALAMA-PUNCTUATION | Ahmet/AD-NOUN | Bey/AD-NOUN | ,/NOKTALAMA-PUNCTUATION | Prof/AD-NOUN | ./NOKTALAMA-PUNCTUATION | Dr/AD-NOUN | ./AD-NOUN | Mehmet/AD-NOUN | ile/İLGEÇ-PREPOS | görüştü/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Dr/PROPN | ./PUNCT | Ahmet/PROPN | Bey/NOUN | ,/PUNCT | Prof/PROPN | ./PUNCT | Dr./NOUN | Mehmet/PROPN | ile/CCONJ | görüştü/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Dr.', lemma='Unk', pos='Unk', morphemes='Unk', formatted='Unk')/ERROR |

---

### Cümle 40: "O, bu akşam bize gelecek."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | O/PRON | bu/PRON | akşam/NOUN | bize/NOUN | gelecek/VERB |
| **Project_CustomBERT** | O/ADIL-PRONOUN | ,/NOKTALAMA-PUNCTUATION | bu/BELİRLEYİCİ-DET | akşam/AD-NOUN | bize/ADIL-PRONOUN | gelecek/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | O/PRON | ,/PUNCT | bu/DET | akşam/NOUN | bize/PRON | gelecek/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='O', lemma='o', pos='Det', morphemes=['Det'], formatted='[o:Det] o:Det')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='bu', lemma='bu', pos='Det', morphemes=['Det'], formatted='[bu:Det] bu:Det')/ERROR | Parse(word='akşam', lemma='akşam', pos='Noun', morphemes=['Noun', 'A3sg'], formatted='[akşam:Noun,Time] akşam:Noun+A3sg')/ERROR | Parse(word='bize', lemma='biz', pos='Noun', morphemes=['Noun', 'A3sg', 'Dat'], formatted='[biz:Noun] biz:Noun+A3sg+e:Dat')/ERROR | Parse(word='gelecek', lemma='gelecek', pos='Adj', morphemes=['Adj'], formatted='[gelecek:Adj] gelecek:Adj')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 41: "O kitabı bana ver."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | O/PRON | kitabı/NOUN | bana/NOUN | ver/NOUN |
| **Project_CustomBERT** | O/ADIL-PRONOUN | kitabı/AD-NOUN | bana/ADIL-PRONOUN | ver/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | O/DET | kitabı/NOUN | bana/PRON | ver/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='O', lemma='o', pos='Det', morphemes=['Det'], formatted='[o:Det] o:Det')/ERROR | Parse(word='kitabı', lemma='Kitab', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[Kitab:Noun,Prop] kitab:Noun+A3sg+ı:Acc')/ERROR | Parse(word='bana', lemma='banmak', pos='Verb', morphemes=['Verb', 'Opt', 'A3sg'], formatted='[banmak:Verb] ban:Verb+a:Opt+A3sg')/ERROR | Parse(word='ver', lemma='vermek', pos='Verb', morphemes=['Verb', 'Imp', 'A2sg'], formatted='[vermek:Verb] ver:Verb+Imp+A2sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 42: "Bu, çok zor bir soru."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Bu/PRON | çok/NOUN | zor/NOUN | bir/NUM | soru/NOUN |
| **Project_CustomBERT** | Bu/BELİRLEYİCİ-DET | ,/NOKTALAMA-PUNCTUATION | çok/BELİRTEÇ-ADVERB | zor/SIFAT-ADJECTIVE | bir/BELİRLEYİCİ-DET | soru/AD-NOUN | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Bu/PRON | ,/PUNCT | çok/ADV | zor/ADJ | bir/DET | soru/NOUN | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Bu', lemma='bu', pos='Det', morphemes=['Det'], formatted='[bu:Det] bu:Det')/ERROR | Parse(word=',', lemma=',', pos='Punc', morphemes=['Punc'], formatted='[,:Punc] ,:Punc')/ERROR | Parse(word='çok', lemma='çok', pos='Adv', morphemes=['Adv'], formatted='[çok:Adv] çok:Adv')/ERROR | Parse(word='zor', lemma='zor', pos='Adv', morphemes=['Adv'], formatted='[zor:Adv] zor:Adv')/ERROR | Parse(word='bir', lemma='bir', pos='Adj', morphemes=['Adj'], formatted='[bir:Adj] bir:Adj')/ERROR | Parse(word='soru', lemma='sorumak', pos='Verb', morphemes=['Verb', 'Imp', 'A2sg'], formatted='[sorumak:Verb] soru:Verb+Imp+A2sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 43: "Bu soruyu çözmek zor."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Bu/PRON | soruyu/NOUN | çözmek/VERB | zor/NOUN |
| **Project_CustomBERT** | Bu/BELİRLEYİCİ-DET | soruyu/AD-NOUN | çözmek/FİİL-VERB | zor/SIFAT-ADJECTIVE | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Bu/DET | soruyu/NOUN | çözmek/VERB | zor/ADJ | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Bu', lemma='bu', pos='Det', morphemes=['Det'], formatted='[bu:Det] bu:Det')/ERROR | Parse(word='soruyu', lemma='soru', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[soru:Noun] soru:Noun+A3sg+yu:Acc')/ERROR | Parse(word='çözmek', lemma='çözmek', pos='Noun', morphemes=['Verb', 'Inf1', 'Noun', 'A3sg'], formatted='[çözmek:Verb] çöz:Verb|mek:Inf1→Noun+A3sg')/ERROR | Parse(word='zor', lemma='zor', pos='Adv', morphemes=['Adv'], formatted='[zor:Adv] zor:Adv')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 44: "Şu ağacı görüyor musun?"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | şu/PRON | ağacı/NOUN | görüyor/VERB | musun/NOUN |
| **Project_CustomBERT** | Şu/BELİRLEYİCİ-DET | ağacı/AD-NOUN | görüyor/FİİL-VERB | musun/SORU-QUESTION | ?/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Şu/DET | ağacı/NOUN | görüyor/VERB | musun/AUX | ?/PUNCT |
| **Extra_Zeyrek** | Parse(word='Şu', lemma='şu', pos='Adj', morphemes=['Adj'], formatted='[şu:Adj] şu:Adj')/ERROR | Parse(word='ağacı', lemma='ağaç', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[ağaç:Noun] ağac:Noun+A3sg+ı:Acc')/ERROR | Parse(word='görüyor', lemma='görmek', pos='Verb', morphemes=['Verb', 'Prog1', 'A3sg'], formatted='[görmek:Verb] gör:Verb+üyor:Prog1+A3sg')/ERROR | Parse(word='musun', lemma='mu', pos='Ques', morphemes=['Ques', 'Pres', 'A2sg'], formatted='[mu:Ques] mu:Ques+Pres+sun:A2sg')/ERROR | Parse(word='?', lemma='?', pos='Punc', morphemes=['Punc'], formatted='[?:Punc] ?:Punc')/ERROR |

---

### Cümle 45: "Şunu bana uzatır mısın?"
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | şunu/NOUN | bana/NOUN | uzatır/NOUN | mısın/NOUN |
| **Project_CustomBERT** | Şunu/ADIL-PRONOUN | bana/ADIL-PRONOUN | uzatır/FİİL-VERB | mısın/SORU-QUESTION | ?/NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Şunu/PRON | bana/PRON | uzatır/VERB | mısın/AUX | ?/PUNCT |
| **Extra_Zeyrek** | Parse(word='Şunu', lemma='şu', pos='Pron', morphemes=['Pron', 'A3sg', 'Acc'], formatted='[şu:Pron,Demons] şu:Pron+A3sg+nu:Acc')/ERROR | Parse(word='bana', lemma='banmak', pos='Verb', morphemes=['Verb', 'Opt', 'A3sg'], formatted='[banmak:Verb] ban:Verb+a:Opt+A3sg')/ERROR | Parse(word='uzatır', lemma='uzatmak', pos='Verb', morphemes=['Verb', 'Aor', 'A3sg'], formatted='[uzatmak:Verb] uzat:Verb+ır:Aor+A3sg')/ERROR | Parse(word='mısın', lemma='mı', pos='Ques', morphemes=['Ques', 'Pres', 'A2sg'], formatted='[mı:Ques] mı:Ques+Pres+sın:A2sg')/ERROR | Parse(word='?', lemma='?', pos='Punc', morphemes=['Punc'], formatted='[?:Punc] ?:Punc')/ERROR |

---

### Cümle 46: "Koşmak sağlığa yararlıdır."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Koşmak/VERB | sağlığa/NOUN | yararlıdır/NOUN |
| **Project_CustomBERT** | Koşmak/FİİL-VERB | sağlığa/AD-NOUN | yararlıdır/SIFAT-ADJECTIVE | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Koşmak/VERB | sağlığa/NOUN | yararlı/ADJ | dır/AUX | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Koşmak', lemma='koşmak', pos='Noun', morphemes=['Verb', 'Inf1', 'Noun', 'A3sg'], formatted='[koşmak:Verb] koş:Verb|mak:Inf1→Noun+A3sg')/ERROR | Parse(word='sağlığa', lemma='sağlık', pos='Noun', morphemes=['Noun', 'A3sg', 'Dat'], formatted='[sağlık:Noun] sağlığ:Noun+A3sg+a:Dat')/ERROR | Parse(word='yararlıdır', lemma='yarar', pos='Verb', morphemes=['Noun', 'A3sg', 'With', 'Adj', 'Zero', 'Verb', 'Pres', 'A3sg', 'Cop'], formatted='[yarar:Noun] yarar:Noun+A3sg|lı:With→Adj|Zero→Verb+Pres+A3sg+dır:Cop')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 47: "Gelen gideni aratır."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Gelen/NOUN | gideni/NOUN | aratır/NOUN |
| **Project_CustomBERT** | Gelen/AD-NOUN | gideni/AD-NOUN | aratır/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Gelen/VERB | gideni/ADJ | aratır/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Gelen', lemma='gelen', pos='Adj', morphemes=['Adj'], formatted='[gelen:Adj] gelen:Adj')/ERROR | Parse(word='gideni', lemma='Gide', pos='Noun', morphemes=['Noun', 'A3sg', 'P2sg', 'Acc'], formatted='[Gide:Noun,Prop] gide:Noun+A3sg+n:P2sg+i:Acc')/ERROR | Parse(word='aratır', lemma='aramak', pos='Verb', morphemes=['Verb', 'Caus', 'Verb', 'Aor', 'A3sg'], formatted='[aramak:Verb] ara:Verb|t:Caus→Verb+ır:Aor+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 48: "Gülerek yanıma geldi."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Gülerek/NOUN | yanıma/NOUN | geldi/VERB |
| **Project_CustomBERT** | Gülerek/BELİRTEÇ-ADVERB | yanıma/AD-NOUN | geldi/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Gülerek/VERB | yanıma/ADJ | geldi/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Gülerek', lemma='gülmek', pos='Adv', morphemes=['Verb', 'ByDoingSo', 'Adv'], formatted='[gülmek:Verb] gül:Verb|erek:ByDoingSo→Adv')/ERROR | Parse(word='yanıma', lemma='yan', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg', 'Dat'], formatted='[yan:Noun] yan:Noun+A3sg+ım:P1sg+a:Dat')/ERROR | Parse(word='geldi', lemma='gelmek', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[gelmek:Verb] gel:Verb+di:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 49: "Okumuş adamın hali başka olur."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Okumuş/VERB | adamın/NOUN | hali/NOUN | başka/NOUN | olur/NOUN |
| **Project_CustomBERT** | Okumuş/SIFAT-ADJECTIVE | adamın/AD-NOUN | hali/AD-NOUN | başka/BELİRTEÇ-ADVERB | olur/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Okumuş/VERB | adamın/NOUN | hali/NOUN | başka/ADJ | olur/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Okumuş', lemma='okumak', pos='Adj', morphemes=['Verb', 'NarrPart', 'Adj'], formatted='[okumak:Verb] oku:Verb|muş:NarrPart→Adj')/ERROR | Parse(word='adamın', lemma='ada', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg', 'Gen'], formatted='[ada:Noun] ada:Noun+A3sg+m:P1sg+ın:Gen')/ERROR | Parse(word='hali', lemma='hâl', pos='Noun', morphemes=['Noun', 'A3sg', 'Acc'], formatted='[hâl:Noun] hal:Noun+A3sg+i:Acc')/ERROR | Parse(word='başka', lemma='başka', pos='Postp', morphemes=['Postp'], formatted='[başka:Postp,PCAbl] başka:Postp')/ERROR | Parse(word='olur', lemma='olur', pos='Adj', morphemes=['Adj'], formatted='[olur:Adj] olur:Adj')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

### Cümle 50: "Dolmuş durağa yanaştı."
| Model | Etiketlenmiş Çıktı (Kelime/TAG) |
| :--- | :--- |
| **Project_Simple** | Dolmuş/VERB | durağa/NOUN | yanaştı/VERB |
| **Project_CustomBERT** | Dolmuş/AD-NOUN | durağa/AD-NOUN | yanaştı/FİİL-VERB | ./NOKTALAMA-PUNCTUATION |
| **Extra_Stanza** | Dolmuş/ADJ | durağa/NOUN | yanaştı/VERB | ./PUNCT |
| **Extra_Zeyrek** | Parse(word='Dolmuş', lemma='dolmuş', pos='Adj', morphemes=['Adj'], formatted='[dolmuş:Adj] dolmuş:Adj')/ERROR | Parse(word='durağa', lemma='durak', pos='Noun', morphemes=['Noun', 'A3sg', 'Dat'], formatted='[durak:Noun] durağ:Noun+A3sg+a:Dat')/ERROR | Parse(word='yanaştı', lemma='yanaşmak', pos='Verb', morphemes=['Verb', 'Past', 'A3sg'], formatted='[yanaşmak:Verb] yanaş:Verb+tı:Past+A3sg')/ERROR | Parse(word='.', lemma='.', pos='Punc', morphemes=['Punc'], formatted='[.:Punc] .:Punc')/ERROR |

---

