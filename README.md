# Segmentation-With-Mask-RCNN
**Projenin Amacı:** <br>
Mask R-CNN ile Beyin Tümörünün Segmentasyonu <br>

**Segmentasyon Nedir?** <br>
Segmentasyon, bir diğer adıyla bölümleme ya da bölütleme; bir görüntüyü farklı özelliklerin tutulduğu anlamlı bölgelere ayırmaktır. Yani, her piksel için etiketler çıkartılır ve bu etiketlere dair tahminler yapılarak birtakım çıkarımlarda bulunulur. Medikal görüntülerde de tanı ve tedavinin ilk ve oldukça kritik bir bileşenidir ve homojen alanları ayırmak için yaygın olarak kullanılmaktadır . BT veya MR görüntülerinde; organların veya lezyonların piksellerini tanımlayan tıbbi görüntü segmentasyonu, bu organların ve lezyonların şekilleri ve hacimleri hakkında kritik bilgiler sunmak konusunda oldukça önemli yere sahiptirler. Daha önceleri bu görevler çeşitli filtreler ve çeşitli matematiksel formüllerin uygulanması ile gerçekleştirilirken son yıllarda derin öğrenmeye dayalı teknikler büyük ilgi görerek bu alanda sıklıkla kullanılmaya başlanmıştır [[1](https://www.makesense.ai/)]. <br>

**Segmentasyon Türleri:**
- Semantic
- Instance <br>

<img
  src="https://www.jeremyjordan.me/content/images/2018/05/Screen-Shot-2018-05-30-at-11.35.12-AM-1.png"
  alt="Alt text"
  title="Optional title"> <br>
  
  
  **Mask R-CNN:** 
  - Instance Segmentasyon türü
  - ResNet tabanlı CNN modelleri içerir
  
 **Mask R-CNN Çalışma Aşamaları:**
 - İlk aşamada görüntü taranır ve önerileri üretilir
 - İkinci aşamada ise önerilen nesnelerin sınıfıları belirlenir sonrasında sınırlayıcı kutular(bounding box) ve maskeler oluşturulur.
 
 <img
  src="https://miro.medium.com/max/1154/0*_p3LGIufAVslUhEw"
  width="500" height="400"> <br>

**Mask R-CNN Kaynak Kod:** <br>
Proje kapmasımda kullanılan kod kaynaklarına [buradan](https://pysource.com/2021/08/10/train-mask-r-cnn-for-image-segmentation-online-free-gpu/) erişim sağlayabilirisniz. 


**Veri Etiketleme:** <br>
Proje kapsamında 310 görüntünün etiketlenmesi [Make Sense](https://www.makesense.ai/) ile gerçekeliştirlmiştir. 

 <img src="https://github.com/lil9991/Segmentation-With-Mask-RCNN/blob/main/img/labell.png"
  width="400" height="400"> 
 <img src="https://github.com/lil9991/Segmentation-With-Mask-RCNN/blob/main/img/label.png"
  width="400" height="400"> <br>
 
 
 **Sonuçlar:** <br>
Mask R-CNN ile beyin tümörünün tespiti ve segmentasyonu 
 
 <img src="https://github.com/lil9991/Segmentation-With-Mask-RCNN/blob/main/img/output.png"
 width="400" height="400"> 
 <img src="https://github.com/lil9991/Segmentation-With-Mask-RCNN/blob/main/img/output2.png"
 width="400" height="400"> <br>
 
   


