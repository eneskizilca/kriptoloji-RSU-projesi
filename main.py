# Algorithm name: Hybrid-LCG-Xor

import time
import math

class HybridRNG:
    def __init__(self, seed=None):
        if seed is None:
            # Seed verilmezse zamanı kullan (tamamen rastgelelik için)
            self.state = int(time.time() * 1000)
        else:
            self.state = seed
        
        # LCG Sabitleri (Yaygın kullanılan parametreler)
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        
    def next_int(self):
        # 1. Adım: Linear Congruential Generator (LCG)
        self.state = (self.a * self.state + self.c) % self.m
        
        # 2. Adım: Xorshift (Daha iyi dağılım ve 0-1 dengesi için)
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        return x & 0xFFFFFFFF # 32-bit integer döndür

    def generate_binary_string(self, length=1000):
        """Testler için 0 ve 1'lerden oluşan uzun bir string üretir"""
        binary_str = ""
        while len(binary_str) < length:
            num = self.next_int()
            # Sayıyı binary formatına çevir (0b öneki olmadan)
            binary_str += bin(num)[2:].zfill(32)
        return binary_str[:length]

# --- İSTATİSTİKSEL TESTLER ---

def ki_kare_testi(binary_data):
    """
    Chi-Square (Ki-Kare) Testi:
    0 ve 1'lerin dağılımının beklenen değerden (yarı yarıya) ne kadar saptığını ölçer.
    """
    count_0 = binary_data.count('0')
    count_1 = binary_data.count('1')
    total = len(binary_data)
    expected = total / 2
    
    # Ki-kare formülü: sum((Gözlenen - Beklenen)^2 / Beklenen)
    chi_square = ((count_0 - expected)**2 / expected) + ((count_1 - expected)**2 / expected)
    
    print(f"\n--- Ki-Kare (Chi-Square) Testi ---")
    print(f"0 Sayısı: {count_0}, 1 Sayısı: {count_1}")
    print(f"Hesaplanan Değer: {chi_square:.4f}")
    if chi_square < 3.841: # %95 güven aralığı için kritik değer (1 serbestlik derecesi)
        print("SONUÇ: BAŞARILI (Dağılım Rastgele)")
    else:
        print("SONUÇ: BAŞARISIZ (Dağılım Dengeli Değil)")
    return chi_square

def mislin_testi(binary_data):
    """
    Runs Test (Mislin Testi):
    Ardışık gelen aynı değerlerin (serilerin) sayısını analiz eder.
    Örn: 0011100 -> Seriler: 00, 111, 00 (3 seri var)
    """
    runs = 1 # İlk seri
    for i in range(len(binary_data) - 1):
        if binary_data[i] != binary_data[i+1]:
            runs += 1
            
    n1 = binary_data.count('0')
    n2 = binary_data.count('1')
    n = len(binary_data)
    
    # Beklenen seri sayısı
    expected_runs = ((2 * n1 * n2) / n) + 1
    # Varyans
    variance = (2 * n1 * n2 * (2 * n1 * n2 - n)) / ((n**2) * (n - 1))
    # Z Skoru
    z_score = (runs - expected_runs) / math.sqrt(variance)
    
    print(f"\n--- Mislin (Runs) Testi ---")
    print(f"Gözlenen Seri Sayısı: {runs}")
    print(f"Beklenen Seri Sayısı: {expected_runs:.2f}")
    print(f"Z Skoru: {z_score:.4f}")
    
    if -1.96 < z_score < 1.96: # %95 güven aralığı
        print("SONUÇ: BAŞARILI (Seriler Rastgele)")
    else:
        print("SONUÇ: BAŞARISIZ (Serilerde Örüntü Var)")

# --- ANA ÇALIŞTIRMA ---
if __name__ == "__main__":
    # 1. Seed belirle (Fotoğraftaki G(seed) kısmı)
    seed_input = input("Bir seed (başlangıç değeri) girin (Boş bırakırsanız zamanı kullanır): ")
    seed = int(seed_input) if seed_input.strip() else None
    
    rng = HybridRNG(seed)
    
    print("\n--- Örnek Çıktılar (Integer) ---")
    for _ in range(5):
        print(rng.next_int())
        
    print("\n--- Test Verisi Üretiliyor (10.000 bit) ---")
    test_data = rng.generate_binary_string(10000)
    print(f"İlk 50 bit: {test_data[:50]}...")
    
    # Testleri Çalıştır
    ki_kare_testi(test_data)
    mislin_testi(test_data)