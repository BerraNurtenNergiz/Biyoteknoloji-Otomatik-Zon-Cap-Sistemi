# Biyoteknoloji-Otomatik-Zon-Cap-Sistemi
Bu proje, biyoteknolojik analizlerde kullanılan antibiyogram disklerinin inhibisyon zon çaplarını, manuel ölçüm hatalarını minimize ederek dijital olarak hesaplayan bir analiz protokolüdür. Gıda atıklarından (limon, portakal, mandalina) sentezlenen nanopartiküllerin antimikrobiyal etkinliğini değerlendirmek amacıyla geliştirilmiştir.
## Projenin Amacı
Geleneksel manuel ölçüm yöntemlerindeki subjektif hata payını ortadan kaldırmak, laboratuvar verimliliğini artırmak ve klinik standartlarda tekrarlanabilir, objektif veriler elde etmektir.
## Temel Özellikler
**Otomatik Tespit:** Petri kabını ve üzerindeki antibiyogram disklerini görüntü üzerinden otomatik algılama.  
**Hassas Ölçüm:** Radyal yoğunluk profili analizi ile inhibisyon zon sınırlarını milimetrik doğrulukla hesaplama.  
**Esnek Analiz:** Dairesel olmayan, eliptik formdaki zonları dahi başarıyla tespit etme.  
**Hata Ayıklama:** Zon oluşumu görülmeyen diskleri otomatik olarak sınıflandırma.  
## Kullanılan Teknolojiler
**Python** (Projenin ana programlama dili)  
**OpenCV** (Petri kabı ve disklerin tespiti, kenar belirleme ve görselleştirme)  
**NumPy** (Görüntü verilerini matrisler halinde işleme ve sayısal hesaplamalar)  
**Pillow** (Görüntü dosyalarının açılması ve temel düzenleme işlemleri)  
**Scikit-image & Scipy** (İnhibisyon zonlarının radyal yoğunluk profili analizi ve hassas ölçümler)  
**Pandas** (Analiz verilerinin tablo haline getirilmesi ve yönetimi)  
**Matplotlib** (Analiz sonuçlarının grafiksel olarak gösterimi)  
