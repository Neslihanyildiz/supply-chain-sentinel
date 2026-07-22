# Supply Chain Sentinel

Typosquatting girişimlerini, bilinen zafiyetleri tespit eden ve endüstri
standardı SBOM üreten hafif bir bağımlılık güvenlik tarayıcısı — CI/CD
güvenlik kapısı ve gerçek, tekrarlanabilir bir saldırı simülasyonuyla
kanıtlanmış.

## Problem

Yazılım tedarik zinciri saldırıları, uygulama güvenliğinde en hızlı büyüyen
tehditlerden biri. Saldırganlar, popüler kütüphanelere çok yakın isimlerle
zararlı paketler yayınlıyor (`requests` yerine `reqeusts` gibi) veya
otomatik build sistemlerini kandırıp zararlı kod çekmelerini sağlayan
dependency confusion tekniklerini kullanıyor. Tek bir `pip install` veya
`npm install` komutu, bir geliştiricinin bilgisayarında rastgele kod
çalıştırmaya yetiyor — çoğu zaman hiçbir onay istemeden çalışan bir
`postinstall` scripti aracılığıyla.

Bu araç, bir projenin bağımlılık dosyasını tarayıp şüpheli paketleri
**kurulmadan önce** işaretliyor, ve bir CI/CD pipeline'ına otomatik bir
güvenlik kapısı olarak entegre edilebiliyor.

## Mimari
requirements.txt
↓
Dependency Parser
↓
Metadata Collector (PyPI API)
↓
Typosquat Analyzer ──→ "'requests'e çok yakın olduğu için şüpheli"
↓
Vulnerability Analyzer (OSV.dev) ──→ "N bilinen CVE bulundu"
↓
Risk Scorer ──→ LOW / MEDIUM / HIGH / CRITICAL
↓
Recommendation Engine ──→ "X.X.X sürümüne yükselt"
↓
SBOM Generator (CycloneDX)
↓
GitHub Action güvenlik kapısı (HIGH/CRITICAL'de build'i durdurur)

Pipeline tamamen deterministik ve açıklanabilir — her karar belirli bir
sinyale (edit distance, CVE sayısı, yayın metadata'sı) kadar izlenebilir,
kara kutu (black-box) bir bileşen yok.

## Özellikler

- **Typosquat tespiti**: popüler PyPI ve npm paketlerinden oluşan seçilmiş
  bir listeye karşı Levenshtein edit-distance karşılaştırması
- **Zafiyet taraması**: OSV.dev'in genel zafiyet veritabanına gerçek
  zamanlı sorgular, versiyon-duyarlı (en güncel sürüm değil, gerçekte
  belirtilen sürüm kontrol edilir)
- **Risk skorlama**: typosquat şüphesi, zafiyet sayısı ve paket varlık
  kontrolünü birleştiren ağırlıklı 0-100 skor
- **SBOM üretimi**: geçerli bir CycloneDX 1.5 JSON malzeme listesi üretir
- **CI/CD entegrasyonu**: her push/PR'de çalışan, HIGH veya CRITICAL
  riskli bir bağımlılık bulunduğunda build'i durduran GitHub Action

## Değerlendirme

Elle etiketlenmiş 25 paket adından oluşan bir ground truth setine karşı
test edildi (13 meşru paket, 12 bilinen typosquatting deseni):

| Metrik    | Skor |
|-----------|------|
| Precision | 1.00 |
| Recall    | 0.92 |
| F1 Score  | 0.96 |

**Confusion matrix:** 12 doğru pozitif, 0 yanlış pozitif, 13 doğru
negatif, 1 yanlış negatif.

Kaçırılan tek vaka (`reqeust`, `requests`'ten edit distance 3) doğrudan,
ölçülmüş bir sonucu: `threshold=2` tasarım kararının bir etkisi — bkz.
[Bilinen Sınırlamalar](#bilinen-sınırlamalar).

## Canlı Saldırı Simülasyonu

Sadece sentetik test verisine güvenmek yerine, bu proje izole bir lokal
npm registry'sine (Verdaccio) karşı **tekrarlanabilir, gerçek bir saldırı
simülasyonu** içeriyor:

1. `express` paketini taklit eden gerçek bir typosquat paketi (`expresss`)
   yayınlandı — gerçek zararlı paketlerin kurulum sırasında sessizce kod
   çalıştırmak için kullandığı `postinstall` mekanizmasıyla
2. Bir kurbanın `npm install expresss` çalıştırması simüle edildi
3. Sessiz kod çalıştırma doğrulandı (kanıt dosyası otomatik oluştu,
   hiçbir kullanıcı onayı gerekmedi)
4. Supply Chain Sentinel bu paket adına karşı çalıştırıldı — **doğru
   şekilde işaretlendi** (`express`'ten edit distance: 1)

Tam log ve tekrarlama adımları: [`demo/SIMULATION_LOG.md`](demo/SIMULATION_LOG.md)

## Bilinen Sınırlamalar

Bunları şeffafça paylaşıyorum çünkü bir sistemin sınırlarını anlamak,
onu inşa etmek kadar önemli:

- **Typosquat eşiği sabit (`=2`)**: değerlendirme, bunun daha uzun edit
  distance'a sahip typo'ları (ör. `reqeust`, mesafe 3) kaçırdığını
  gösterdi. Uzunluğa göre normalize edilmiş veya dinamik bir eşik,
  bir miktar precision kaybıyla recall'ı artırabilir.
- **Referans paket listesi elle seçilmiş** (~50 paket), canlı PyPI/npm
  indirme istatistiklerinden çekilmiyor. Üretim versiyonu, "en çok
  indirilen N paket" API'sine senkronize olurdu.
- **Versiyon aralıkları çözümlenmiyor**: `~=4.2` olarak belirtilen bir
  bağımlılık, gerçek kurulu sürüm yerine `"4.2"` olarak kaydedilip
  taranıyor. Lockfile-duyarlı bir çözümleyici bunu düzeltirdi.
- **Davranışsal analiz yok**: araç isimleri, metadata'yı ve bilinen
  CVE'leri kontrol ediyor — sıfırıncı gün (zero-day) zararlı davranışı
  tespit etmek için paketleri sandbox'ta çalıştırmıyor. Bu, dinamik değil,
  statik/sinyal tabanlı bir yaklaşım.

## Nasıl Çalıştırılır

```bash
git clone https://github.com/Neslihanyildiz/supply-chain-sentinel.git
cd supply-chain-sentinel
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt

python main.py        # tüm pipeline'ı çalıştır
python evaluate.py    # değerlendirme setini çalıştır
```

## Teknoloji Yığını

Python · requests · python-Levenshtein · scikit-learn · cyclonedx-python-lib
· OSV.dev API · PyPI JSON API · Verdaccio (npm) · GitHub Actions