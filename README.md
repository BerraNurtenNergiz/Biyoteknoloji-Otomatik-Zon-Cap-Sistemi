# Biyoteknoloji-Otomatik-Zon-Cap-Sistemi
Bu proje, biyoteknolojik analizlerde kullanılan antibiyogram disklerinin inhibisyon zon çaplarını, manuel ölçüm hatalarını minimize ederek dijital olarak hesaplayan bir analiz protokolüdür. Gıda atıklarından (limon, portakal, mandalina) sentezlenen nanopartiküllerin antimikrobiyal etkinliğini değerlendirmek amacıyla geliştirilmiştir.
## Projenin Amacı
Geleneksel manuel ölçüm yöntemlerindeki subjektif hata payını ortadan kaldırmak, laboratuvar verimliliğini artırmak ve klinik standartlarda tekrarlanabilir, objektif veriler elde etmektir.
## Temel Özellikler
Otomatik Tespit: Petri kabını ve üzerindeki antibiyogram disklerini görüntü üzerinden otomatik algılama. <br /><br />
Hassas Ölçüm: Radyal yoğunluk profili analizi ile inhibisyon zon sınırlarını milimetrik doğrulukla hesaplama. <br /><br />
Esnek Analiz: Dairesel olmayan, eliptik formdaki zonları dahi başarıyla tespit etme. <br /><br />
Hata Ayıklama: Zon oluşumu görülmeyen diskleri otomatik olarak sınıflandırma. <br /><br />
## Kullanılan Teknolojiler
Python (Projenin ana programlama dili) <br /><br />
OpenCV (Petri kabı ve disklerin tespiti, kenar belirleme ve görselleştirme) <br /><br />
NumPy (Görüntü verilerini matrisler halinde işleme ve sayısal hesaplamalar) <br /><br />
Pillow (Görüntü dosyalarının açılması ve temel düzenleme işlemleri) <br /><br />
Scikit-image & Scipy (İnhibisyon zonlarının radyal yoğunluk profili analizi ve hassas ölçümler) <br /><br />
Pandas (Analiz verilerinin tablo haline getirilmesi ve yönetimi) <br /><br />
Matplotlib (Analiz sonuçlarının grafiksel olarak gösterimi)<br /><br />
