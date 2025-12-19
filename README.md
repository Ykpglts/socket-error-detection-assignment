# Data Transmission with Error Detection Methods

## Proje Amacı
Bilgisayar ağlarında veri iletimi sırasında oluşan hataları tespit etmek için kullanılan yöntemleri (Parity, 2D Parity, CRC, Hamming, Checksum) socket programlama ile pratik olarak göstermek.

## Sistem Bileşenleri
- **client1_sender.py**: Gönderici – Metin alır, kontrol bilgisi üretir ve paketi sunucuya gönderir.
- **server.py**: Ara düğüm + Veri bozucu – Paketi alır, rastgele hata enjekte eder (bit flip, karakter değiştirme/silme/ekleme vb.) ve alıcıya iletir.
- **client2_receiver.py**: Alıcı – Paketi alır, kontrol bilgisini yeniden hesaplar ve hatayı tespit eder.

**Paket Formatı:** `VERİ|YÖNTEM|KONTROL_BİLGİSİ`  
Örnek: `HELLO|CRC16|87AF`

## Desteklenen Yöntemler
1. Parity Bit (Even/Odd)
2. 2D Parity
3. CRC-16
4. Hamming Code
5. Internet Checksum

## Çalıştırma Sırası
1. `python client2_receiver.py` (alıcı)
2. `python server.py` (sunucu)
3. `python client1_sender.py` (gönderici → metin ve yöntem seç)

## Örnek
Gönderici: `HELLO WORLD|CRC16|5546`  
Server bozar → `HELLO WORLOD|CRC16|5546`  
Alıcı: **HATA TESPİT EDİLDİ!**

**Not:** Demo için kısa İngilizce metin kullanın. Server %70 olasılıkla veri bozar.

Hazırlayan: [Yakup Gültaş]  
Tarih: 19 Aralık 2025

Başarılar! 🚀