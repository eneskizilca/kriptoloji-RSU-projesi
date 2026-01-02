# RSÜ (Rastgele Sayı Üreteci) Projesi

# 1. Algoritma Mantığı:

Bu projede Hybrid LCG-Xor yöntemi kullanılmıştır. Standart Linear Congruential Generator (LCG) algoritmasının ürettiği değerler, bit seviyesinde karıştırma yapan Xorshift işleminden geçirilmiştir.
Neden? LCG tek başına hızlıdır ancak alt bitlerinde örüntü oluşturabilir. Xorshift bu bitleri karıştırarak 0 ve 1 dağılımının (Bernoulli dağılımı) %50-%50'ye yaklaşmasını sağlar.

Formül: X 
n+1
​	
 =(a⋅X 
n
​	
 +c)(modm) ardından Bitwise XOR ve Shift işlemleri.

 2. Sözde Kod (Pseudo-Code):

BAŞLA
  GİRDİ: Seed (Tohum) Değeri
  EĞER Seed YOKSA -> Şimdiki Zamanı Seed Yap
  
  FONKSİYON Next_Int():
    State = (State * 1664525 + 1013904223) MOD 2^32
    Temp = State
    Temp = Temp XOR (Temp << 13)
    Temp = Temp XOR (Temp >> 17)
    Temp = Temp XOR (Temp << 5)
    DÖNDÜR Temp
  
  TEST İÇİN:
    10.000 bitlik veri üret
    Ki-Kare Testi Uygula (Frekans dengesi)
    Mislin (Runs) Testi Uygula (Seri bağımsızlığı)
BİTİR

# 3. Akış Şeması

<img width="329" height="859" alt="Ekran Resmi 2026-01-02 15 12 29" src="https://github.com/user-attachments/assets/b5b8753a-1ede-453f-8668-51a5b6c8c6f3" />

