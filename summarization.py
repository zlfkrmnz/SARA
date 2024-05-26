from summarize import Summarizer
import openpyxl


def get_text_summary(path):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    _summaries = []
    for row in ws.iter_rows():
        for cell in row:
            _summaries.append(cell.value)
    return _summaries


def summarize(_text):
    summ = Summarizer("turkish-english-summarizer")
    print(f"Text: {_text}\nSummary: {summ.summarize(_text)}")


if "__main__" == __name__:
    summaries = get_text_summary("data/tr_summaries.xlsx")
    summarize("""Giriş
Türk kamuoyunda ilkokul öğrencilerinin başarısı birincil olarak sınıf
öğretmenlerinin niteliklerine bağlanmakta (Bümen ve Ercan Özaydın,
2013) ve sınıf öğretmenleri çocukların geleceğini biçimlendirmede etkisi
uzun yıllar sürecek izler bırakmaktadır. Erol ve Başaran (2020),
çocukların ilkokul döneminde aileden sonra en çok birlikte zaman
geçirdikleri kişinin sınıf öğretmeni olduğunu belirtirken, Altuner ve
Başaran (2017) da ilkokul öğrencilerinin sınıf öğretmenlerini anne-
babası gibi gördüklerini, onu her açıdan örnek aldıklarını, ona
güvenerek duygusal açıdan güçlü bir şekilde bağlandıklarını
vurgulamıştır. Bununla birlikte sınıf öğretmenleri hem farklı yaş
grubundaki öğrencilere hem de birden fazla derse yönelik hizmet
verdiği için, iş yükü ve sorumluluğu ağır bir görev yapmaktadır. Bu
nedenle, sınıf öğretmenlerinin belli sınıf düzeylerinde ya da derslerde
uzmanlaşmasının daha işlevsel olup olmadığı uzun zamandır tartışılan
bir konu olmuştur.
Türkiye’de uzun yıllardır öğrencilerin ilkokulda aynı öğretmenle
öğrenime devam etmesi geleneği sürmekte, ancak bazı özel okullar
tüm sınıflarda farklı sınıf öğretmenlerinin derse girmesi; bazı özel
okullar ilk iki sınıfta aynı, son iki sınıfta farklı bir sınıf öğretmeninin;
bazıları ise ilk üç sınıfta aynı, son sınıfta farklı bir sınıf öğretmeninin
görev yapması şeklinde uygulamalar yapmaktadır. Ayrıca bazı özel
okullarda belli sınıf düzeylerinde (ör. Dördüncü sınıfta) ve belli bir derste
(ör. Matematik, fen bilimleri ya da Türkçe vb.) uzmanlaşan sınıf
öğretmenleri de bulunmaktadır. Sözü edilen farklı modellerin son
yıllarda özel okul sayısındaki hızlı artış ve rekabet nedeniyle
gerçekleştiği (Cesur, 2019), ancak devlet okullarında geleneksel modelin
sürdüğü söylenebilir.
Dünyada sınıf öğretmenliğinde farklı uzmanlaşma modellerinin
uygulandığı ve bu modellerin çeşitli şekillerde adlandırıldığı
görülmektedir. Kanada ve ABD’de geleneksel hale gelen “her yıl
öğretmen değişmesi” ya da “bir yıllık öğretmen” modeli (Tourigny ve
diğerleri, 2019) ya da “döngüsel” model (looping) bunlardandır. Çin,
Danimarka, Finlandiya, Hırvatistan, Hollanda, İsrail, İsveç, İtalya,
Jamaika, Japonya, Küba ve Rusya’daki ilkokullarda da uygulanan
döngüsel model (Girgin, 2021; Marušić ve diğerleri, 2020; Tourigny ve
diğerleri, 2019; Wang ve diğerleri, 2017), Türkiye’deki devlet okullarında
dört yıllık döngüsel şeklinde uygulanarak geleneksel model haline
gelmiştir. Bu modelde öğretmen bir grup öğrenciyle en az iki öğretim
yılı ders yürütmekte, döngü tamamlandığında ise yeni bir sınıfla aynı
döngüye devam etmektedir (Cistone ve Shneyderman, 2004).
Döngülerin kaç yıl süreceği ülkeden ülkeye göre değişmekle birlikte,
genellikle iki ya da üç yıl sürmektedir (Tourigny ve diğerlerleri, 2019).
Böylece modelin iki yıllık döngüsel, üç yıllık döngüsel, dört yıllık
döngüsel ve beş yıllık döngüsel şeklinde alt türleri bulunmakta,
Türkiye’deki devlet okullarında dört yıllık döngüsel şeklinde
uygulanmaktadır.
Bunun yanı sıra ders/ konu alanlarını temele alan bütünsel (generalist,
self-contained) ya da branşlaşmış (departmentalized) modeller de
bulunmaktadır. Bütünsel modelde, sınıf öğretmenlerinin programda
bulunan tüm temel derslerde (dil, matematik, fen bilimleri ve sosyal
bilimler) eşit derecede yetkin olduğu varsayılarak, tüm temel akademik
konuları (dersleri) öğretmesi esas alınır (Brobst ve diğerleri, 2017).
Yabancı dil, beden eğitimi, müzik, görsel sanatlar, dini bilgiler, drama vb.
dersler ise farklı öğretmenler tarafından yürütülür. Bütünsel modelde
öğretmen; çocuğun zihinsel, duygusal ve fiziksel gelişiminin tüm
aşamalarını destekleyecek şekilde, “bütün yönleriyle” ilgilenir.
Öğretmen tüm temel dersleri verdiği için hem anlamlı ve bağlantılı
öğrenmeyi mümkün kılan sürekliliği elde etmekte; hem de özerkliği
arttığından daha esnek davranarak, dersler/konular arası bütünleşmeyi
sağlama imkânı bulmaktadır (Parker ve diğerleri, 2017). Öte yandan
branşlaşmış modelde, temel konuları öğretme sorumluluğunun iki
veya daha fazla öğretmen tarafından üstlenilmesi (Ray, 2017),
öğretmenlerin bir dersi birden fazla sınıfa öğretmesi (Slavin, 1987) ve
belli bir konu alanında uzmanlaşması söz konusudur (Chan ve Jarman,
2004). ABD’deki hesap verilebilirlik talepleri (özellikle İngilizce ve
matematik derslerinde öğrenci başarısının artırılması yönündeki
baskılar), dördüncü ve beşinci sınıflarda branşlaşmış modelin son
yıllarda hızla artmasına neden olmuştur (Baroody, 2017).
Görüldüğü gibi, sınıf öğretmenliğinde uzmanlaşma modelleri temelde
öğrenci gruplarına ya da öğretilecek derslere göre çeşitlendirilmiştir.
Öğrenci grupları temele alındığında “her yıl öğretmen değişmesi” ya da
döngüsel modeller, öğretilecek dersler temele alındığında ise bütünsel
ya da branşlaşmış modeller ortaya çıkmaktadır. Şekil 1’de uzmanlaşma
modellerinin sınıflaması sunulmaktadır.""")
