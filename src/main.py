import pygame
import sys
import math
import random 
from PIL import Image 
# 1. AYARLAR VE KURULUM
pygame.init()
# GIF Dosyalarını Dönüştürmek Için Fonksiyon
def load_animated_gif(gif_path):  
    # GIF'i Pillow ile aç
    gif = Image.open(gif_path)  
    frames = []  
    durations = []  
 
    # GIF'ten kareleri ve süreleri çıkar  
    for frame_index in range(gif.n_frames):  
        gif.seek(frame_index)  
        frame_rgba = gif.convert("RGBA")  
        frame_data = frame_rgba.tobytes()  
        frame_surface = pygame.image.fromstring(  
            frame_data, frame_rgba.size, frame_rgba.mode  
        ).convert_alpha()  
        frames.append(frame_surface)  
        durations.append(gif.info.get("duration", 100))  # Varsayılan 100 milisaniye  
 
    return frames, durations  
 
# Tam Ekran
ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
GENISLIK = info.current_w
YUKSEKLIK = info.current_h

pygame.display.set_caption("Ultimate Fighter (Menü)")


# Animasyon Sabitleri
idle_anim, idle_durations = load_animated_gif("../assets/stickmanidlesmall.gif")
r_idle_anim, r_idle_durations = load_animated_gif("../assets/stickmanidlersmall.gif")
walk_anim, walk_durations = load_animated_gif("../assets/stickmannewsmall.gif")
r_walk_anim, r_walk_durations = load_animated_gif("../assets/stickmannewrsmall.gif")
fist_anim, fist_durations = load_animated_gif("../assets/stickmanfistsmall.gif")
r_fist_anim, r_fist_durations = load_animated_gif("../assets/stickmanfistrsmall.gif")
kick_anim, kick_durations = load_animated_gif("../assets/stickmankicksmall.gif")
r_kick_anim, r_kick_durations = load_animated_gif("../assets/stickmankickrsmall.gif")


ridle_anim, ridle_durations = load_animated_gif("../assets/redmanidlesmall.gif")
r_ridle_anim, r_ridle_durations = load_animated_gif("../assets/redmanidlersmall.gif")
rwalk_anim, rwalk_durations = load_animated_gif("../assets/redmannewsmall.gif")
r_rwalk_anim, r_rwalk_durations = load_animated_gif("../assets/redmannewrsmall.gif")
rfist_anim, rfist_durations = load_animated_gif("../assets/redmanfistsmall.gif")
r_rfist_anim, r_rfist_durations = load_animated_gif("../assets/redmanfistrsmall.gif")
rkick_anim, rkick_durations = load_animated_gif("../assets/redmankicksmall.gif")
r_rkick_anim, r_rkick_durations = load_animated_gif("../assets/redmankickrsmall.gif")
mevcut_animasyon = idle_anim
p2mevcut_animasyon = ridle_anim
current_frame = 0 
p2current_frame = 0 
frame_start_time = pygame.time.get_ticks()  
p2frame_start_time = pygame.time.get_ticks()



# --- OYUN DURUMU ---
oyun_durumu = "MENU" 
bot_zorluk = None 
kazanan_metni = "" 

# --- FONT VE RENKLER ---
FONT_BUYUK = pygame.font.SysFont('Arial', 80)
FONT_KUCUK = pygame.font.SysFont('Arial', 40)
FONT_DEV = pygame.font.SysFont('Arial', 150, bold=True) 

# Renkler
BEYAZ = (255, 255, 255)
SIYAH = (0, 0, 0)
SARI = (255, 255, 0) 
YESIL = (0, 200, 0)
MAVI = (0, 0, 200)
GOKYUZU = (135, 206, 235)
ZEMIN_RENGI = (34, 139, 34)
OYUNCU_RENK = (220, 20, 60) 
BOT_RENK = (75, 0, 130)     
YUMRUK_RENGI = (255, 215, 0) 
TEKME_RENGI = (255, 165, 0) 
ENGELLEME_RENK = (100, 100, 255) 
MERMI_RENK_P = (0, 255, 255) # P1 Mermi Rengi
MERMI_RENK_B = (255, 0, 255) # P2/Bot Mermi Rengi
STUN_PARLAMA_RENGI = (128, 0, 128) # Mor parlama
DASH_RENK = (255, 140, 0) # Turuncu
CAN_DOLU_P = (255, 0, 0)
CAN_DOLU_B = (180, 0, 180)

# --- YENİ SABİTLER ---
YETENEK_STUN_SURESI = 3000 # 3 saniye stun süresi (milisaniye)

#-----KONTROL TUŞLARI----
p1_dash = pygame.K_f
p1_ziplama = pygame.K_w
p1_yumruk = pygame.K_s
p1_tekme = pygame.K_e
p1_skill = pygame.K_q
p1_sag = pygame.K_d
p1_sol = pygame.K_a
p2_dash = pygame.K_k
p2_ziplama = pygame.K_UP
p2_yumruk = pygame.K_DOWN
p2_tekme = pygame.K_RCTRL
p2_skill = pygame.K_j
p2_sag = pygame.K_RIGHT
p2_sol = pygame.K_LEFT

# Buton Kontrolü İçin Değişkenler
kontrole_tiklandi = False
tiklanan_kontrol = -1

# DASH SABİTLERİ
DASH_MESAFESI = 250
DASH_SURESI = 15 # Kare (frame) sayısı
DASH_BEKLEME_SURESI = 3000 # 3 saniye bekleme süresi (milisaniye)
DASH_HASARI = 7

# FPS
saat = pygame.time.Clock()
FPS = 60

# --- FİZİK SABİTLERİ ---
zemin_yuksekligi = 150
zemin_y = YUKSEKLIK - zemin_yuksekligi
yer_cekimi = 0.8
p_ziplama = -22
p_hizlanma = 1.8           
p_max_hiz = 10             
p_yer_surtunmesi = 0.80    
p_hava_surtunmesi = 0.99   
mer_hiz = 30 
bot_hizlanma = p_hizlanma * 1.3 # Bot daha hızlı hareket edebilir

# --- OYUNCU VE BOT TEMEL DEĞİŞKENLERİ ---
p_w, p_h = 70, 110
b_w, b_h = 70, 110
p_max_can, b_max_can = 100, 100 

# Yumruk/Tekme
yumruk_suresi = 14
yumruk_bekleme_suresi = 2000 
yumruk_hasari = 5
tekme_suresi = 24
tekme_bekleme_suresi = 3000 
tekme_hasari = 9
tekme_menzili_w, tekme_menzili_h = 30, 15 

# Yetenek
yet_bekleme_suresi = 10000 # 10 saniye bekleme süresi
yet_hasari = 1             

# --- GLOBAL DURUM DEĞİŞKENLERİ ---
# P1
p_x, p_y, p_y_hiz, p_x_hiz, p_yon, p_can, p_yumruk_aktif, p_yumruk_sayaci, p_son_vurus_zamani, p_tekme_aktif, p_tekme_sayaci, p_son_tekme_zamani = 0, 0, 0, 0, 1, 100, False, 0, 0, False, 0, 0
p_mer_aktif, p_mer_x, p_mer_y, p_mer_hiz, p_son_yet_zamani = False, 0, 0, 0, 0
p_stun_bitis_zamani = 0
p_cekme_hakki_bitis_zamani = 0
p_dash_aktif = False
p_dash_sayaci = 0
p_son_dash_zamani = 0
p_dash_hasar_verdi = False 
# Double jump için yeni değişkenler
p_ziplama_sayisi = 0
p_ziplama_yapabilir = True

# P2/BOT
b_x, b_y, b_y_hiz, b_x_hiz, b_yon, b_can, b_yumruk_aktif, b_yumruk_sayaci, b_son_vurus_zamani, b_tekme_aktif, b_tekme_sayaci, b_son_tekme_zamani = 0, 0, 0, 0, -1, 100, False, 0, 0, False, 0, 0
b_mer_aktif, b_mer_x, b_mer_y, b_mer_hiz, b_son_yet_zamani = False, 0, 0, 0, 0
b_stun_bitis_zamani = 0 
b_cekme_hakki_bitis_zamani = 0
b_dash_aktif = False
b_dash_sayaci = 0
b_son_dash_zamani = 0
b_dash_hasar_verdi = False 
# Bot için double jump değişkenleri
b_ziplama_sayisi = 0
b_ziplama_yapabilir = True

# ULTRA ZOR AI DEĞİŞKENLERİ
ai_bekleme_sayaci = 0 
b_engelleme_aktif = False 
b_engelleme_sayaci = 0
ai_karar_sayaci = 0
ai_mod = "AGRESIF"
ai_hedef_mesafe = 150
ai_saldiri_tahmini = [0, 0]  # [x_tahmini, y_tahmini]
ai_oyuncu_hareket_gecmisi = []  # Oyuncu hareketlerini kaydet
ai_kombosu = []  # Kombo hareketleri
ai_son_saldiri_zamani = 0
ai_basit_mod = False  # Düşük can durumunda basit ama etkili taktikler

# --- UI HESAPLAMALARI ---
ORTA_BOSLUK = 50
KENAR_BOSLUKLARI = 20
bar_genislik = (GENISLIK - ORTA_BOSLUK - (2 * KENAR_BOSLUKLARI)) // 2
bar_yukseklik = 70
UI_Y_KONUMU = 50 

p_bar_x, p_bar_y = KENAR_BOSLUKLARI, UI_Y_KONUMU
b_bar_x, b_bar_y = p_bar_x + bar_genislik + ORTA_BOSLUK, UI_Y_KONUMU

# --- MENÜ VE DÜĞMELER ---
button_w, button_h = 300, 70
center_x = GENISLIK // 2
center_y = YUKSEKLIK // 2
tek_oyuncu_rect = pygame.Rect(center_x - button_w // 2, center_y - 100, button_w, button_h)
iki_oyuncu_rect = pygame.Rect(center_x - button_w // 2, center_y + 20, button_w, button_h)
kontroller_rect = pygame.Rect(center_x - button_w // 2, center_y + 100, button_w, button_h)
geri_gel_rect = pygame.Rect(center_x - button_w // 2, center_y + 260, button_w, button_h)
p1_yumruk_kontrol = pygame.Rect(center_x - button_w // 2 + 200, center_y - 300, button_w * 1.2, button_h * 0.7)
p1_tekme_kontrol = pygame.Rect(center_x - button_w // 2 + 200, center_y - 220, button_w * 1.2, button_h * 0.7)
p1_dash_kontrol = pygame.Rect(center_x - button_w // 2 + 200, center_y - 140, button_w * 1.2, button_h * 0.7)
p1_skill_kontrol = pygame.Rect(center_x - button_w // 2 + 200, center_y - 60, button_w * 1.2, button_h * 0.7)
p1_ziplama_kontrol = pygame.Rect(center_x - button_w // 2 + 200, center_y + 20, button_w * 1.2, button_h * 0.7)
p1_sag_kontrol = pygame.Rect(center_x - button_w // 2 + 200, center_y + 100, button_w * 1.2, button_h * 0.7)
p1_sol_kontrol = pygame.Rect(center_x - button_w // 2 + 200, center_y + 180, button_w * 1.2, button_h * 0.7)
p2_yumruk_kontrol = pygame.Rect(center_x - button_w // 2 - 200, center_y - 300, button_w * 1.2, button_h * 0.7)
p2_tekme_kontrol = pygame.Rect(center_x - button_w // 2 - 200, center_y - 220, button_w * 1.2, button_h * 0.7)
p2_dash_kontrol = pygame.Rect(center_x - button_w // 2 - 200, center_y - 140, button_w * 1.2, button_h * 0.7)
p2_skill_kontrol = pygame.Rect(center_x - button_w // 2 - 200, center_y - 60, button_w * 1.2, button_h * 0.7)
p2_ziplama_kontrol = pygame.Rect(center_x - button_w // 2 - 200, center_y + 20, button_w * 1.2, button_h * 0.7)
p2_sag_kontrol = pygame.Rect(center_x - button_w // 2 - 200, center_y + 100, button_w * 1.2, button_h * 0.7)
p2_sol_kontrol = pygame.Rect(center_x - button_w // 2 - 200, center_y + 180, button_w * 1.2, button_h * 0.7)
kolay_rect = pygame.Rect(center_x - button_w // 2, center_y - 200, button_w, button_h)
zor_rect = pygame.Rect(center_x - button_w // 2, center_y + 20, button_w, button_h)
cok_zor_rect = pygame.Rect(center_x - button_w // 2, center_y + 140, button_w, button_h)
tekrar_oyna_rect = pygame.Rect(center_x - button_w // 2, center_y + 260, button_w, button_h)

# --- YARDIMCI FONKSİYONLAR ---
def draw_button(ekran, rect, renk, metin, font, text_color):
    pygame.draw.rect(ekran, renk, rect)
    text_surface = font.render(metin, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    ekran.blit(text_surface, text_rect)

def reset_game_state():
    """Tüm karakter değişkenlerini başlangıç değerlerine sıfırlar."""
    global p_x, p_y, p_y_hiz, p_x_hiz, p_yon, p_can, p_yumruk_aktif, p_yumruk_sayaci, p_son_vurus_zamani, p_tekme_aktif, p_tekme_sayaci, p_son_tekme_zamani, p_mer_aktif, p_mer_x, p_mer_y, p_mer_hiz, p_son_yet_zamani, p_stun_bitis_zamani, p_cekme_hakki_bitis_zamani, p_dash_aktif, p_dash_sayaci, p_son_dash_zamani, p_dash_hasar_verdi, p_ziplama_sayisi, p_ziplama_yapabilir
    global b_x, b_y, b_y_hiz, b_x_hiz, b_yon, b_can, b_yumruk_aktif, b_yumruk_sayaci, b_son_vurus_zamani, b_tekme_aktif, b_tekme_sayaci, b_son_tekme_zamani, b_mer_aktif, b_mer_x, b_mer_y, b_mer_hiz, b_son_yet_zamani, b_stun_bitis_zamani, b_cekme_hakki_bitis_zamani, b_dash_aktif, b_dash_sayaci, b_son_dash_zamani, b_dash_hasar_verdi, b_ziplama_sayisi, b_ziplama_yapabilir
    global ai_bekleme_sayaci, b_engelleme_aktif, b_engelleme_sayaci, oyun_durumu, kazanan_metni, ai_karar_sayaci, ai_mod, ai_hedef_mesafe, ai_saldiri_tahmini, ai_oyuncu_hareket_gecmisi, ai_kombosu, ai_son_saldiri_zamani, ai_basit_mod

    p_x, p_y = 100, zemin_y - p_h
    p_y_hiz, p_x_hiz = 0, 0
    p_yon = 1
    p_can = p_max_can 
    p_yumruk_aktif, p_yumruk_sayaci, p_son_vurus_zamani = False, 0, 0
    p_tekme_aktif, p_tekme_sayaci, p_son_tekme_zamani = False, 0, 0
    p_mer_aktif, p_mer_x, p_mer_y, p_mer_hiz, p_son_yet_zamani = False, 0, 0, 0, 0
    p_stun_bitis_zamani = 0
    p_cekme_hakki_bitis_zamani = 0
    p_dash_aktif, p_dash_sayaci, p_son_dash_zamani, p_dash_hasar_verdi = False, 0, 0, False
    p_ziplama_sayisi = 0
    p_ziplama_yapabilir = True

    b_x, b_y = GENISLIK - 280, zemin_y - b_h
    b_y_hiz, b_x_hiz = 0, 0
    b_yon = -1
    b_can = b_max_can 
    b_yumruk_aktif, b_yumruk_sayaci, b_son_vurus_zamani = False, 0, 0
    b_tekme_aktif, b_tekme_sayaci, b_son_tekme_zamani = False, 0, 0
    b_mer_aktif, b_mer_x, b_mer_y, b_mer_hiz, b_son_yet_zamani = False, 0, 0, 0, 0
    b_stun_bitis_zamani = 0
    b_cekme_hakki_bitis_zamani = 0
    b_dash_aktif, b_dash_sayaci, b_son_dash_zamani, b_dash_hasar_verdi = False, 0, 0, False
    b_ziplama_sayisi = 0
    b_ziplama_yapabilir = True

    ai_bekleme_sayaci = 0
    b_engelleme_aktif = False
    b_engelleme_sayaci = 0
    ai_karar_sayaci = 0
    ai_mod = "AGRESIF"
    ai_hedef_mesafe = 150
    ai_saldiri_tahmini = [0, 0]
    ai_oyuncu_hareket_gecmisi = []
    ai_kombosu = []
    ai_son_saldiri_zamani = 0
    ai_basit_mod = False
    kazanan_metni = ""

def bot_can_ziplayabilir():
    """Botun zıplama koşulunu kontrol eder (Sadece yerde olmayı kontrol eder)."""
    return b_y + b_h >= zemin_y - 1

def p1_hasar_alabilir():
    """P1'in hasar alıp alamayacağını kontrol eder (Dash sırasında hasar almaz)."""
    return not p_dash_aktif and not p_stun_bitis_zamani > pygame.time.get_ticks()

def p2_hasar_alabilir():
    """P2/Bot'un hasar alıp alamayacağını kontrol eder (Dash sırasında hasar almaz)."""
    return not b_dash_aktif and not b_stun_bitis_zamani > pygame.time.get_ticks()

def draw_cooldown_circle(ekran, center_x, center_y, radius, cooldown_ratio, tus_adi, kalan_sure, aktif_mi):
    """Yuvarlak cooldown göstergesi çizer"""
    
    # Arka plan daire (gri)
    pygame.draw.circle(ekran, (50, 50, 50), (center_x, center_y), radius)
    
    # Cooldown doluluk oranına göre renk
    if cooldown_ratio < 1.0:
        renk = (200, 50, 50)
    else:
        renk = (50, 200, 50) if aktif_mi else (100, 100, 100)
    
    if cooldown_ratio < 1.0:
        angle = 360 * cooldown_ratio
        pygame.draw.arc(ekran, renk, (center_x - radius, center_y - radius, radius * 2, radius * 2), 
                       -math.pi/2, -math.pi/2 + math.radians(angle), int(radius * 0.3))
    
    pygame.draw.circle(ekran, BEYAZ, (center_x, center_y), radius, 2)
    
    font = pygame.font.SysFont('Arial', 20)
    tus_text = font.render(tus_adi, True, BEYAZ)
    tus_rect = tus_text.get_rect(center=(center_x, center_y))
    ekran.blit(tus_text, tus_rect)
    
    if cooldown_ratio < 1.0 and kalan_sure > 0:
        time_font = pygame.font.SysFont('Arial', 16)
        time_text = time_font.render(f"{kalan_sure/1000:.1f}s", True, BEYAZ)
        time_rect = time_text.get_rect(center=(center_x, center_y + 25))
        ekran.blit(time_text, time_rect)

# ULTRA ZOR AI FONKSİYONLARI
def ai_oyuncu_hareketini_kaydet():
    """Oyuncunun hareketlerini kaydederek pattern öğrenir"""
    if len(ai_oyuncu_hareket_gecmisi) > 50:  # Son 50 hareketi sakla
        ai_oyuncu_hareket_gecmisi.pop(0)
    
    hareket = {
        'x': p_x,
        'y': p_y,
        'x_hiz': p_x_hiz,
        'y_hiz': p_y_hiz,
        'yon': p_yon,
        'zaman': mevcut_zaman
    }
    ai_oyuncu_hareket_gecmisi.append(hareket)

def ai_hareket_tahmini_yap():
    """Oyuncunun gelecekteki konumunu tahmin et"""
    if len(ai_oyuncu_hareket_gecmisi) < 5:
        return p_x + p_x_hiz * 8, p_y + p_y_hiz * 8
    
    # Son 5 frame'in ortalamasını al
    ortalama_x_hiz = sum([hareket['x_hiz'] for hareket in ai_oyuncu_hareket_gecmisi[-5:]]) / 5
    ortalama_y_hiz = sum([hareket['y_hiz'] for hareket in ai_oyuncu_hareket_gecmisi[-5:]]) / 5
    
    tahmini_x = p_x + ortalama_x_hiz * 12  # 12 frame ilerisi
    tahmini_y = p_y + ortalama_y_hiz * 12
    
    return tahmini_x, tahmini_y

def ai_kombo_olustur():
    """Rastgele kombolar oluştur"""
    kombolar = [
        ["YUMRUK", "TEKME", "YUMRUK"],
        ["TEKME", "DASH", "YUMRUK"],
        ["YUMRUK", "YUMRUK", "TEKME"],
        ["DASH", "YUMRUK", "TEKME"],
        ["YUMRUK", "TEKME", "MERMI"]
    ]
    return random.choice(kombolar)

def ai_mod_degistir():
    """Duruma göre AI modunu değiştir"""
    global ai_mod, ai_hedef_mesafe, ai_basit_mod
    
    if b_can > b_max_can * 0.7:  # %70 üstü
        ai_mod = "AGRESIF"
        ai_hedef_mesafe = 80
        ai_basit_mod = False
    elif b_can > b_max_can * 0.3:  # %30-%70 arası
        ai_mod = "TAKTIKLI"
        ai_hedef_mesafe = 150
        ai_basit_mod = False
    else:  # %30 altı
        ai_mod = "HAYATTA_KALMA"
        ai_hedef_mesafe = 250
        ai_basit_mod = True

def ai_mermi_hedefi_belirle():
    """İleri seviye mermi hedefleme"""
    tahmini_x, tahmini_y = ai_hareket_tahmini_yap()
    
    # Botun pozisyonundan tahmini hedefe vektör
    vektor_x = tahmini_x - (b_x + b_w/2)
    vektor_y = tahmini_y - (b_y + b_h/2)
    
    # Vektörü normalize et
    uzunluk = math.sqrt(vektor_x**2 + vektor_y**2)
    if uzunluk > 0:
        vektor_x /= uzunluk
        vektor_y /= uzunluk
    
    return vektor_x, vektor_y

def ai_saldiri_konumlandirma():
    """Akıllı saldırı konumlandırma"""
    tahmini_x, tahmini_y = ai_hareket_tahmini_yap()
    
    saldiri_menzili = 100
    mevcut_mesafe = abs(tahmini_x - b_x)
    
    if mevcut_mesafe > saldiri_menzili + 50:
        if tahmini_x > b_x:
            return 1  # Sağa git
        else:
            return -1  # Sola git
    elif mevcut_mesafe < saldiri_menzili - 30:
        if tahmini_x > b_x:
            return -1  # Sola git (uzaklaş)
        else:
            return 1   # Sağa git (uzaklaş)
    else:
        # Küçük hareketlerle pozisyon al
        if random.random() < 0.4:
            return 1 if random.random() < 0.5 else -1
        return 0

def ai_yetenek_karari():
    """Çok agresif yetenek kullanımı"""
    yatay_mesafe = abs(p_x - b_x)
    
    # Çekme hakkı varsa mutlaka kullan
    if p2_cekme_hakki_aktif and p1_stun_aktif:
        return "CEKME"
    
    # Mermi atışı - ÇOK YÜKSEK ŞANS
    if not b_mer_aktif and mevcut_zaman - b_son_yet_zamani > yet_bekleme_suresi:
        if ai_mod == "AGRESIF":
            if yatay_mesafe < 400 and random.random() < 0.7:  # %70 şans
                return "MERMI_ATES"
        elif ai_mod == "TAKTIKLI":
            if yatay_mesafe > 200 and yatay_mesafe < 500 and random.random() < 0.6:
                return "MERMI_ATES"
        else:  # HAYATTA_KALMA
            if yatay_mesafe < 200 and random.random() < 0.8:  # Yakındaysa yüksek şans
                return "MERMI_ATES"
    
    return "BEKLE"

def ai_dash_karari():
    """Sürekli dash kullanımı"""
    yatay_mesafe = abs(p_x - b_x)
    
    if mevcut_zaman - b_son_dash_zamani > DASH_BEKLEME_SURESI * 0.8:  # Daha sık dash
        if ai_mod == "AGRESIF":
            if (yatay_mesafe > 100 and yatay_mesafe < 350) or p1_stun_aktif:
                if random.random() < 0.6:  # %60 şans
                    return "SALDIRI"
        elif ai_mod == "TAKTIKLI":
            if yatay_mesafe > 200 or (p_mer_aktif and abs(p_mer_x - b_x) < 250):
                if random.random() < 0.5:
                    return "KACIS" if yatay_mesafe < 150 else "SALDIRI"
        else:  # HAYATTA_KALMA
            if yatay_mesafe < 150 or p_can > b_can:
                if random.random() < 0.7:
                    return "KACIS"
    
    return "BEKLE"

def ai_yakın_dovus_karari():
    """Çok agresif yakın dövüş"""
    yatay_mesafe = abs(p_x - b_x)
    saldiri_menzili = 110
    
    if yatay_mesafe < saldiri_menzili:
        if ai_mod == "AGRESIF":
            # SÜREKLİ SALDIRI
            if not b_yumruk_aktif and mevcut_zaman - b_son_vurus_zamani > yumruk_bekleme_suresi * 0.6:
                if random.random() < 0.8:  # %80 şans
                    return "YUMRUK"
            
            if not b_tekme_aktif and mevcut_zaman - b_son_tekme_zamani > tekme_bekleme_suresi * 0.8:
                if random.random() < 0.5:
                    return "TEKME"
                    
        elif ai_mod == "TAKTIKLI":
            if not b_yumruk_aktif and mevcut_zaman - b_son_vurus_zamani > yumruk_bekleme_suresi:
                if random.random() < 0.6:
                    return "YUMRUK"
            
            if not b_tekme_aktif and mevcut_zaman - b_son_tekme_zamani > tekme_bekleme_suresi:
                if random.random() < 0.4:
                    return "TEKME"
            
            # Akıllı engelleme
            if not b_engelleme_aktif and p_yumruk_aktif and random.random() < 0.4:
                return "ENGELLE"
                
        else:  # HAYATTA_KALMA
            if not b_engelleme_aktif and random.random() < 0.6:
                return "ENGELLE"
            elif not b_yumruk_aktif and mevcut_zaman - b_son_vurus_zamani > yumruk_bekleme_suresi:
                if random.random() < 0.3:
                    return "YUMRUK"
    
    return "BEKLE"

def ai_ziplama_karari():
    """Akıllı zıplama kararı"""
    if (b_y + b_h >= zemin_y - 1 or (b_ziplama_sayisi < 2 and b_ziplama_yapabilir)):
        if ai_mod == "AGRESIF":
            # Saldırı için zıpla
            if abs(p_x - b_x) < 150 and random.random() < 0.3:
                return True
            # Mermiden kaçmak için zıpla
            if p_mer_aktif and abs(p_mer_x - b_x) < 200 and random.random() < 0.7:
                return True
        elif ai_mod == "TAKTIKLI":
            if (p_mer_aktif and abs(p_mer_x - b_x) < 250) or (abs(p_x - b_x) < 100 and random.random() < 0.2):
                return True
        else:  # HAYATTA_KALMA
            if p_mer_aktif and abs(p_mer_x - b_x) < 300 and random.random() < 0.8:
                return True
    
    return False

# 2. OYUN DÖNGÜSÜ
calisiyor = True
while calisiyor:
    mevcut_zaman = pygame.time.get_ticks()
    
    # Stun Durumu Kontrolü
    p1_stun_aktif = mevcut_zaman < p_stun_bitis_zamani 
    p2_stun_aktif = mevcut_zaman < b_stun_bitis_zamani 
    
    # Çekme Hakkı Kontrolü
    p1_cekme_hakki_aktif = mevcut_zaman < p_cekme_hakki_bitis_zamani
    p2_cekme_hakki_aktif = mevcut_zaman < b_cekme_hakki_bitis_zamani
    
    # --- COOLDOWN HESAPLAMALARI ---
    
    # P1 Cooldown Hesaplamaları
    p_yumruk_cooldown_kaldi = max(0, yumruk_bekleme_suresi - (mevcut_zaman - p_son_vurus_zamani))
    p_yumruk_cooldown_orani = 1 - (p_yumruk_cooldown_kaldi / yumruk_bekleme_suresi)
    
    p_tekme_cooldown_kaldi = max(0, tekme_bekleme_suresi - (mevcut_zaman - p_son_tekme_zamani))
    p_tekme_cooldown_orani = 1 - (p_tekme_cooldown_kaldi / tekme_bekleme_suresi)
    
    p_yet_cooldown_kaldi = max(0, yet_bekleme_suresi - (mevcut_zaman - p_son_yet_zamani))
    p_yet_cooldown_orani = 1 - (p_yet_cooldown_kaldi / yet_bekleme_suresi)
    
    p_dash_cooldown_kaldi = max(0, DASH_BEKLEME_SURESI - (mevcut_zaman - p_son_dash_zamani))
    p_dash_cooldown_orani = 1 - (p_dash_cooldown_kaldi / DASH_BEKLEME_SURESI)
    
    # P2 Cooldown Hesaplamaları
    b_yumruk_cooldown_kaldi = max(0, yumruk_bekleme_suresi - (mevcut_zaman - b_son_vurus_zamani))
    b_yumruk_cooldown_orani = 1 - (b_yumruk_cooldown_kaldi / yumruk_bekleme_suresi)
    
    b_tekme_cooldown_kaldi = max(0, tekme_bekleme_suresi - (mevcut_zaman - b_son_tekme_zamani))
    b_tekme_cooldown_orani = 1 - (b_tekme_cooldown_kaldi / tekme_bekleme_suresi)
    
    b_yet_cooldown_kaldi = max(0, yet_bekleme_suresi - (mevcut_zaman - b_son_yet_zamani))
    b_yet_cooldown_orani = 1 - (b_yet_cooldown_kaldi / yet_bekleme_suresi)
    
    b_dash_cooldown_kaldi = max(0, DASH_BEKLEME_SURESI - (mevcut_zaman - b_son_dash_zamani))
    b_dash_cooldown_orani = 1 - (b_dash_cooldown_kaldi / DASH_BEKLEME_SURESI)
    
    # --- GİRDİLER (Keydown) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            calisiyor = False
        if event.type == pygame.KEYDOWN:
            if tiklanan_kontrol == 1:
                p1_yumruk = event.key
            elif tiklanan_kontrol == 2:
                p1_tekme = event.key
            elif tiklanan_kontrol == 3:
                p1_dash = event.key
            elif tiklanan_kontrol == 4:
                p1_skill = event.key
            elif tiklanan_kontrol == 5:
                p1_ziplama = event.key
            elif tiklanan_kontrol == 6:
                p1_sag = event.key
            elif tiklanan_kontrol == 7:
                p1_sol = event.key
            elif tiklanan_kontrol == 8:
                p2_yumruk = event.key
            elif tiklanan_kontrol == 9:
                p2_tekme = event.key
            elif tiklanan_kontrol == 10:
                p2_dash = event.key
            elif tiklanan_kontrol == 11:
                p2_skill = event.key
            elif tiklanan_kontrol == 12:
                p2_ziplama = event.key
            elif tiklanan_kontrol == 13:
                p2_sag = event.key
            elif tiklanan_kontrol == 14:
                p2_sol = event.key
            kontrole_tiklandi = False
            tiklanan_kontrol = -1
        
        # MENÜ VE ZORLUK SEÇİMİ KONTROLÜ
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if oyun_durumu == "MENU":
                if tek_oyuncu_rect.collidepoint(mouse_pos):
                    oyun_durumu = "DIFFICULTY_SELECT" 
                    pygame.display.set_caption("Zorluk Seçimi")
                elif iki_oyuncu_rect.collidepoint(mouse_pos):
                    reset_game_state() 
                    oyun_durumu = "IKI_OYUNCULU"
                    pygame.display.set_caption("İki Oyunculu Mod (VS)")
                elif kontroller_rect.collidepoint(mouse_pos):
                    oyun_durumu = "CONTROLS"
                    pygame.display.set_caption("Kontroller")

            elif oyun_durumu == "DIFFICULTY_SELECT":
                if kolay_rect.collidepoint(mouse_pos):
                    bot_zorluk = "KOLAY"
                    reset_game_state() 
                    oyun_durumu = "TEK_OYUNCULU"
                    pygame.display.set_caption("Tek Oyunculu Mod (Kolay)")
                elif zor_rect.collidepoint(mouse_pos):
                    bot_zorluk = "ZOR"
                    reset_game_state() 
                    oyun_durumu = "TEK_OYUNCULU"
                    pygame.display.set_caption("Tek Oyunculu Mod (Zor)")
                elif cok_zor_rect.collidepoint(mouse_pos):
                    bot_zorluk = "COK_ZOR"
                    reset_game_state() 
                    oyun_durumu = "TEK_OYUNCULU"
                    pygame.display.set_caption("Tek Oyunculu Mod (ÇOK ZOR)")
                    
            elif oyun_durumu == "OYUN_BITTI":
                if tekrar_oyna_rect.collidepoint(mouse_pos):
                    reset_game_state()
                    oyun_durumu = "MENU"
                    pygame.display.set_caption("Ultimate Fighter (Menü)")
            elif oyun_durumu == "CONTROLS":
                if p1_yumruk_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 1
                elif p1_tekme_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 2
                elif p1_dash_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 3
                elif p1_skill_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 4
                elif p1_ziplama_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 5
                elif p1_sag_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 6
                elif p1_sol_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 7
                elif p2_yumruk_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 8
                elif p2_tekme_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 9
                elif p2_dash_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 10
                elif p2_skill_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 11
                elif p2_ziplama_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 12
                elif p2_sag_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 13
                elif p2_sol_kontrol.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    kontrole_tiklandi = True
                    tiklanan_kontrol = 14
                elif geri_gel_rect.collidepoint(mouse_pos) and kontrole_tiklandi == False:
                    oyun_durumu = "MENU"


        # OYUN İÇİ GİRDİLER
        if (oyun_durumu == "TEK_OYUNCULU" or oyun_durumu == "IKI_OYUNCULU") and event.type == pygame.KEYDOWN:
            
            # --- P1 KONTROLLERİ ---
            if event.key == p1_dash and not p_dash_aktif and not p_yumruk_aktif and not p_tekme_aktif and not p1_stun_aktif and mevcut_zaman - p_son_dash_zamani > DASH_BEKLEME_SURESI:
                p_dash_aktif = True
                p_dash_sayaci = DASH_SURESI
                p_son_dash_zamani = mevcut_zaman
                p_dash_hasar_verdi = False
                dash_hiz = DASH_MESAFESI / DASH_SURESI
                p_x_hiz = dash_hiz * p_yon
                
            if not p1_stun_aktif and not p_dash_aktif:
                if event.key == p1_ziplama and not p_yumruk_aktif and not p_tekme_aktif:
                    if (p_y + p_h >= zemin_y - 1) or (p_ziplama_sayisi < 2 and p_ziplama_yapabilir):
                        p_y_hiz = p_ziplama
                        p_ziplama_sayisi += 1
                
                if event.key == p1_yumruk and not p_tekme_aktif and mevcut_zaman - p_son_vurus_zamani > yumruk_bekleme_suresi:
                    p_son_vurus_zamani = mevcut_zaman
                    p_yumruk_aktif = True
                    p_yumruk_sayaci = yumruk_suresi
                    
                    yumruk_genislik, yumruk_yukseklik = 50, 40
                    p_yumruk_rect = pygame.Rect(p_x + p_w if p_yon == 1 else p_x - yumruk_genislik, p_y + 30, yumruk_genislik, yumruk_yukseklik)
                    target_rect = pygame.Rect(b_x, b_y, b_w, b_h)
                    
                    if p_yumruk_rect.colliderect(target_rect) and b_can > 0 and p2_hasar_alabilir():
                        if b_engelleme_aktif:
                            b_can -= yumruk_hasari * 0.1 
                        else:
                            b_can -= yumruk_hasari 
                        b_engelleme_aktif = False
                        b_engelleme_sayaci = 0

                if event.key == p1_tekme and not p_yumruk_aktif and mevcut_zaman - p_son_tekme_zamani > tekme_bekleme_suresi:
                    p_son_tekme_zamani = mevcut_zaman
                    p_tekme_aktif = True
                    p_tekme_sayaci = tekme_suresi

                    p_tekme_rect = pygame.Rect(
                        p_x + p_w if p_yon == 1 else p_x - tekme_menzili_w, 
                        p_y + p_h - tekme_menzili_h, 
                        tekme_menzili_w, tekme_menzili_h
                    )
                    target_rect = pygame.Rect(b_x, b_y, b_w, b_h)
                    
                    if p_tekme_rect.colliderect(target_rect) and b_can > 0 and p2_hasar_alabilir():
                        if b_engelleme_aktif:
                            b_can -= tekme_hasari * 0.1 
                        else:
                            b_can -= tekme_hasari 
                        b_engelleme_aktif = False
                        b_engelleme_sayaci = 0
            
            if event.key == p1_skill:
                if p1_cekme_hakki_aktif:
                    if p2_stun_aktif:
                        b_x = p_x - p_w if p_yon == 1 else p_x + p_w 
                        b_y = zemin_y - b_h 
                        b_yon = p_yon 
                        b_stun_bitis_zamani = 0 
                    p_cekme_hakki_bitis_zamani = 0 
                elif not p_mer_aktif and mevcut_zaman - p_son_yet_zamani > yet_bekleme_suresi:
                    p_mer_aktif = True
                    p_mer_hiz = mer_hiz * p_yon
                    p_mer_x = p_x + p_w / 2 
                    p_mer_y = p_y + p_h / 2
                    p_son_yet_zamani = mevcut_zaman

            # --- P2 KONTROLLERİ (2 Oyunculu Mod) ---
            if oyun_durumu == "IKI_OYUNCULU":
                if event.key == p2_dash and not b_dash_aktif and not b_yumruk_aktif and not b_tekme_aktif and not p2_stun_aktif and mevcut_zaman - b_son_dash_zamani > DASH_BEKLEME_SURESI:
                    b_dash_aktif = True
                    b_dash_sayaci = DASH_SURESI
                    b_son_dash_zamani = mevcut_zaman
                    b_dash_hasar_verdi = False
                    dash_hiz = DASH_MESAFESI / DASH_SURESI
                    b_x_hiz = dash_hiz * b_yon

                if not p2_stun_aktif and not b_dash_aktif:
                    if event.key == p2_ziplama and not b_yumruk_aktif and not b_tekme_aktif:
                        if (b_y + b_h >= zemin_y - 1) or (b_ziplama_sayisi < 2 and b_ziplama_yapabilir):
                            b_y_hiz = p_ziplama
                            b_ziplama_sayisi += 1
                    
                    if event.key == p2_yumruk and not b_tekme_aktif and mevcut_zaman - b_son_vurus_zamani > yumruk_bekleme_suresi:
                        b_son_vurus_zamani = mevcut_zaman
                        b_yumruk_aktif = True
                        b_yumruk_sayaci = yumruk_suresi
                        
                        yumruk_genislik, yumruk_yukseklik = 50, 40
                        b_yumruk_rect = pygame.Rect(b_x + b_w if b_yon == 1 else b_x - yumruk_genislik, b_y + 30, yumruk_genislik, yumruk_yukseklik)
                        p1_rect = pygame.Rect(p_x, p_y, p_w, p_h)
                        if b_yumruk_rect.colliderect(p1_rect) and p_can > 0 and p1_hasar_alabilir():
                            p_can -= yumruk_hasari 

                    if event.key == p2_tekme and not b_yumruk_aktif and mevcut_zaman - b_son_tekme_zamani > tekme_bekleme_suresi:
                        b_son_tekme_zamani = mevcut_zaman
                        b_tekme_aktif = True
                        b_tekme_sayaci = tekme_suresi
                        
                        b_tekme_rect = pygame.Rect(
                            b_x + b_w if b_yon == 1 else b_x - tekme_menzili_w, 
                            b_y + b_h - tekme_menzili_h, 
                            tekme_menzili_w, tekme_menzili_h
                        )
                        p1_rect = pygame.Rect(p_x, p_y, p_w, p_h)
                        if b_tekme_rect.colliderect(p1_rect) and p_can > 0 and p1_hasar_alabilir():
                            p_can -= tekme_hasari 
                    
                    if event.key == p2_skill:
                        if p2_cekme_hakki_aktif:
                            if p1_stun_aktif:
                                p_x = b_x - b_w if b_yon == 1 else b_x + b_w 
                                p_y = zemin_y - p_h
                                p_yon = b_yon 
                                p_stun_bitis_zamani = 0 
                            b_cekme_hakki_bitis_zamani = 0 
                        elif not b_mer_aktif and mevcut_zaman - b_son_yet_zamani > yet_bekleme_suresi:
                            b_mer_aktif = True
                            b_mer_hiz = mer_hiz * b_yon
                            b_mer_x = b_x + b_w / 2 
                            b_mer_y = b_y + b_h / 2
                            b_son_yet_zamani = mevcut_zaman
                        

    # --- OYUN DURUMUNA GÖRE ÇİZİM VE GÜNCELLEME ---

    if oyun_durumu == "MENU" or oyun_durumu == "DIFFICULTY_SELECT" or oyun_durumu == "OYUN_BITTI" or oyun_durumu == "CONTROLS":
        if oyun_durumu == "MENU":
            ekran.fill(SIYAH)
            title_text = FONT_BUYUK.render("ULTIMATE FIGHTER", True, BEYAZ)
            title_rect = title_text.get_rect(center=(center_x, center_y - 200))
            ekran.blit(title_text, title_rect)
            draw_button(ekran, tek_oyuncu_rect, YESIL, "1 OYUNCULU", FONT_KUCUK, SIYAH)
            draw_button(ekran, iki_oyuncu_rect, MAVI, "2 OYUNCULU", FONT_KUCUK, SIYAH)
            draw_button(ekran, kontroller_rect, ZEMIN_RENGI, "KONTROLLER", FONT_KUCUK, SIYAH)

        elif oyun_durumu == "DIFFICULTY_SELECT":
            ekran.fill(SIYAH)
            title_text = FONT_BUYUK.render("ZORLUK SEÇİMİ", True, SARI)
            title_rect = title_text.get_rect(center=(center_x, center_y - 200))
            ekran.blit(title_text, title_rect)
            draw_button(ekran, kolay_rect, YESIL, "KOLAY", FONT_KUCUK, SIYAH)
            draw_button(ekran, zor_rect, (255, 165, 0), "ZOR", FONT_KUCUK, SIYAH)
            draw_button(ekran, cok_zor_rect, CAN_DOLU_P, "ÇOK ZOR", FONT_KUCUK, BEYAZ)

        elif oyun_durumu == "OYUN_BITTI":
            ekran.fill(SIYAH)
            kazanan_text = FONT_DEV.render(kazanan_metni, True, (255, 0, 0)) 
            kazanan_rect = kazanan_text.get_rect(center=(center_x, center_y - 50))
            ekran.blit(kazanan_text, kazanan_rect)
            draw_button(ekran, tekrar_oyna_rect, YESIL, "MENÜYE DÖN", FONT_KUCUK, SIYAH)
            
        elif oyun_durumu == "CONTROLS":
            ekran.fill(SIYAH)
            p1_yumruk_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 1  else "P1 Yumruk : " + pygame.key.name(p1_yumruk)
            p1_tekme_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 2  else "P1 Tekme : " + pygame.key.name(p1_tekme)
            p1_dash_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 3  else "P1 Dash : " + pygame.key.name(p1_dash)
            p1_skill_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 4  else "P1 Skill : " + pygame.key.name(p1_skill)
            p1_ziplama_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 5  else "P1 Zıplama : " + pygame.key.name(p1_ziplama)
            p1_sag_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 6  else "P1 Sağ : " + pygame.key.name(p1_sag)
            p1_sol_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 7  else "P1 Sol : " + pygame.key.name(p1_sol)
            p2_yumruk_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 8  else "P2 Yumruk : " + pygame.key.name(p2_yumruk)
            p2_tekme_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 9  else "P2 Tekme : " + pygame.key.name(p2_tekme)
            p2_dash_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 10  else "P2 Dash : " + pygame.key.name(p2_dash)
            p2_skill_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 11  else "P2 Skill : " + pygame.key.name(p2_skill)
            p2_ziplama_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 12  else "P2 Zıplama : " + pygame.key.name(p2_ziplama)
            p2_sag_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 13  else "P2 Sağ : " + pygame.key.name(p2_sag)
            p2_sol_yazi = "<Bir Tuşa Bas>" if tiklanan_kontrol == 14  else "P2 Sol : " + pygame.key.name(p2_sol)
            draw_button(ekran, p1_yumruk_kontrol, BEYAZ, p1_yumruk_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p1_tekme_kontrol, BEYAZ, p1_tekme_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p1_dash_kontrol, BEYAZ, p1_dash_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p1_skill_kontrol, BEYAZ, p1_skill_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p1_ziplama_kontrol, BEYAZ, p1_ziplama_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p1_sag_kontrol, BEYAZ, p1_sag_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p1_sol_kontrol, BEYAZ, p1_sol_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p2_yumruk_kontrol, BEYAZ, p2_yumruk_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p2_tekme_kontrol, BEYAZ, p2_tekme_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p2_dash_kontrol, BEYAZ, p2_dash_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p2_skill_kontrol, BEYAZ, p2_skill_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p2_ziplama_kontrol, BEYAZ, p2_ziplama_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p2_sag_kontrol, BEYAZ, p2_sag_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, p2_sol_kontrol, BEYAZ, p2_sol_yazi, FONT_KUCUK, SIYAH)
            draw_button(ekran, geri_gel_rect, BEYAZ, "Geri Gel", FONT_KUCUK, SIYAH)
            

    elif oyun_durumu == "TEK_OYUNCULU" or oyun_durumu == "IKI_OYUNCULU":
        
        tuslar = pygame.key.get_pressed()
        
        # --- P1 FİZİK VE HAREKET HESAPLAMALARI ---
        if p_dash_aktif:
            p_dash_sayaci -= 1
            if p_dash_sayaci <= 0:
                p_dash_aktif = False
                p_x_hiz = 0 
            if p_y + p_h < zemin_y:
                p_y_hiz += yer_cekimi * 0.5 
        
        elif not p_yumruk_aktif and not p_tekme_aktif and not p1_stun_aktif: 
            if tuslar[p1_sol]: 
                p_x_hiz = -10
                p_yon = -1
            elif tuslar[p1_sag]: 
                p_x_hiz = 10
                p_yon = 1
            elif p_ziplama_sayisi == 0: 
                p_x_hiz = 0
        elif p_yumruk_aktif and p_ziplama_sayisi == 0 or p_tekme_aktif and p_ziplama_sayisi == 0:
            p_x_hiz = 0
        if p1_stun_aktif: 
            p_x_hiz = 0
            p_y_hiz += yer_cekimi * 0.5 
        elif not p_dash_aktif and p_ziplama_sayisi != 0: 
            surtunme = p_yer_surtunmesi if p_y + p_h >= zemin_y - 1 else p_hava_surtunmesi
            if abs(p_x_hiz) > p_max_hiz:
                p_x_hiz = p_max_hiz if p_x_hiz > 0 else -p_max_hiz
            p_y_hiz += yer_cekimi
            if abs(p_x_hiz) < 0.5: p_x_hiz = 0 
            
        p_x += p_x_hiz
        p_y += p_y_hiz
        
        if p_y + p_h > zemin_y: 
            p_y = zemin_y - p_h
            p_y_hiz = 0
            p_ziplama_sayisi = 0
            p_ziplama_yapabilir = True
        
        if p_x < 0: p_x, p_x_hiz = 0, 0
        if p_x > GENISLIK - p_w: p_x, p_x_hiz = GENISLIK - p_w, 0

        # P1 DASH HASAR KONTROLÜ
        p_rect = pygame.Rect(p_x, p_y, p_w, p_h)
        b_rect = pygame.Rect(b_x, b_y, b_w, b_h)
        if p_dash_aktif and not p_dash_hasar_verdi and p_rect.colliderect(b_rect) and b_can > 0:
            if p2_hasar_alabilir():
                b_can -= DASH_HASARI
                b_engelleme_aktif = False 
                p_dash_hasar_verdi = True
        
        # --- P2/BOT FİZİK VE HAREKET HESAPLAMALARI ---
        yatay_mesafe = p_x - b_x
        
        if b_dash_aktif:
            b_dash_sayaci -= 1
            if b_dash_sayaci <= 0:
                b_dash_aktif = False
                b_x_hiz = 0
            if b_y + b_h < zemin_y:
                b_y_hiz += yer_cekimi * 0.5 

        # --- P2/BOT HAREKET KONTROLLERİ ---
        if oyun_durumu == "IKI_OYUNCULU":
            if not b_yumruk_aktif and not b_tekme_aktif and not p2_stun_aktif and not b_dash_aktif:
                if tuslar[pygame.K_LEFT]:
                    b_x_hiz = -10
                    b_yon = -1
                elif tuslar[pygame.K_RIGHT]:
                    b_x_hiz = 10
                    b_yon = 1
                elif b_y_hiz == 0:
                    b_x_hiz = 0
                
                    
        elif oyun_durumu == "TEK_OYUNCULU":
            if bot_zorluk == "KOLAY":
                b_x_hiz *= p_yer_surtunmesi
                
            elif bot_zorluk == "ZOR":
                # ORTA ZORLUK AI
                b_yon = 1 if yatay_mesafe > 0 else -1
                if not p2_stun_aktif and not b_dash_aktif and not b_yumruk_aktif and not b_tekme_aktif:
                    if abs(yatay_mesafe) > 200:
                        if yatay_mesafe > 0:
                            b_x_hiz += bot_hizlanma
                        else:
                            b_x_hiz -= bot_hizlanma
                    elif abs(yatay_mesafe) < 80:
                        if yatay_mesafe > 0:
                            b_x_hiz -= bot_hizlanma
                        else:
                            b_x_hiz += bot_hizlanma
                
                if abs(yatay_mesafe) < 120 and random.random() < 0.1:
                    if not b_yumruk_aktif and mevcut_zaman - b_son_vurus_zamani > yumruk_bekleme_suresi:
                        b_son_vurus_zamani = mevcut_zaman
                        b_yumruk_aktif = True
                        b_yumruk_sayaci = yumruk_suresi
                
            elif bot_zorluk == "COK_ZOR":
                # ULTRA ZOR AI
                ai_oyuncu_hareketini_kaydet()
                ai_mod_degistir()
                
                b_yon = 1 if yatay_mesafe > 0 else -1
                ai_karar_sayaci += 1
                
                if ai_karar_sayaci >= 8:  # Çok hızlı karar verme
                    ai_karar_sayaci = 0
                    
                    # Çekme hakkı - ANINDA kullan
                    if p2_cekme_hakki_aktif and p1_stun_aktif:
                        p_x = b_x - b_w if b_yon == 1 else b_x + b_w 
                        p_y = zemin_y - p_h
                        p_yon = b_yon 
                        p_stun_bitis_zamani = 0 
                        b_cekme_hakki_bitis_zamani = 0
                    
                    # Dash - ÇOK AGRESİF
                    dash_karar = ai_dash_karari()
                    if dash_karar != "BEKLE" and not b_dash_aktif and not p2_stun_aktif:
                        b_dash_aktif = True
                        b_dash_sayaci = DASH_SURESI
                        b_son_dash_zamani = mevcut_zaman
                        b_dash_hasar_verdi = False
                        dash_hiz = DASH_MESAFESI / DASH_SURESI
                        if dash_karar == "KACIS":
                            b_x_hiz = dash_hiz * (-b_yon)
                        else:
                            b_x_hiz = dash_hiz * b_yon
                    
                    # Yetenek - SÜREKLİ KULLANIM
                    yetenek_karar = ai_yetenek_karari()
                    if yetenek_karar == "MERMI_ATES" and not b_mer_aktif and not p2_stun_aktif:
                        b_mer_aktif = True
                        vektor_x, vektor_y = ai_mermi_hedefi_belirle()
                        b_mer_hiz = mer_hiz * vektor_x
                        b_mer_x = b_x + b_w / 2 
                        b_mer_y = b_y + b_h / 2
                        b_son_yet_zamani = mevcut_zaman
                    
                    # Yakın dövüş - ÇOK AGRESİF
                    if not p2_stun_aktif and not b_dash_aktif:
                        dovus_karar = ai_yakın_dovus_karari()
                        if dovus_karar == "YUMRUK" and not b_yumruk_aktif:
                            b_son_vurus_zamani = mevcut_zaman
                            b_yumruk_aktif = True
                            b_yumruk_sayaci = yumruk_suresi
                        elif dovus_karar == "TEKME" and not b_tekme_aktif:
                            b_son_tekme_zamani = mevcut_zaman
                            b_tekme_aktif = True
                            b_tekme_sayaci = tekme_suresi
                        elif dovus_karar == "ENGELLE" and not b_engelleme_aktif:
                            b_engelleme_aktif = True
                            b_engelleme_sayaci = random.randint(20, 40)
                
                # Hareket - İLERİ SEVİYE KONUMLANMA
                if not p2_stun_aktif and not b_dash_aktif and not b_yumruk_aktif and not b_tekme_aktif:
                    konum_karar = ai_saldiri_konumlandirma()
                    mevcut_mesafe = abs(p_x - b_x)
                    
                    if ai_mod == "AGRESIF":
                        # SÜREKLİ BASKI
                        if konum_karar == 1:
                            b_x_hiz += bot_hizlanma * 1.5
                        elif konum_karar == -1:
                            b_x_hiz -= bot_hizlanma * 1.5
                        else:
                            if random.random() < 0.5:
                                b_x_hiz += bot_hizlanma * 0.8 * (1 if random.random() < 0.5 else -1)
                    
                    elif ai_mod == "TAKTIKLI":
                        # AKILLI POZİSYON
                        if mevcut_mesafe > ai_hedef_mesafe + 30:
                            if p_x > b_x:
                                b_x_hiz += bot_hizlanma * 1.2
                            else:
                                b_x_hiz -= bot_hizlanma * 1.2
                        elif mevcut_mesafe < ai_hedef_mesafe - 30:
                            if p_x > b_x:
                                b_x_hiz -= bot_hizlanma * 1.2
                            else:
                                b_x_hiz += bot_hizlanma * 1.2
                    
                    else:  # HAYATTA_KALMA
                        # SAVUNMA AĞIRLIKLI
                        if mevcut_mesafe < 180:
                            if p_x > b_x:
                                b_x_hiz -= bot_hizlanma * 1.3
                            else:
                                b_x_hiz += bot_hizlanma * 1.3
                
                # Zıplama - AKILLI KULLANIM
                if ai_ziplama_karari():
                    b_y_hiz = p_ziplama 
                    b_ziplama_sayisi += 1
                
                # Engelleme kontrolü
                if b_engelleme_aktif:
                    b_engelleme_sayaci -= 1
                    if b_engelleme_sayaci <= 0:
                        b_engelleme_aktif = False

        # --- ORTAK FİZİK VE GÜNCELLEME (P2/BOT) ---
        if p2_stun_aktif: 
            b_x_hiz = 0
            b_y_hiz += yer_cekimi * 0.5
        elif not b_dash_aktif: 
            surtunme = p_yer_surtunmesi if b_y + b_h >= zemin_y - 1 else p_hava_surtunmesi
            b_x_hiz *= surtunme 
            if abs(b_x_hiz) > p_max_hiz:
                b_x_hiz = p_max_hiz if b_x_hiz > 0 else -p_max_hiz
            b_y_hiz += yer_cekimi
            if abs(b_x_hiz) < 0.5: b_x_hiz = 0 
            
        b_x += b_x_hiz
        b_y += b_y_hiz
        
        if b_y + b_h > zemin_y: 
            b_y = zemin_y - b_h
            b_y_hiz = 0
            b_ziplama_sayisi = 0
            b_ziplama_yapabilir = True
        
        if b_x < 0: b_x, b_x_hiz = 0, 0
        if b_x > GENISLIK - b_w: b_x, b_x_hiz = GENISLIK - b_w, 0
        
        if b_dash_aktif and not b_dash_hasar_verdi and b_rect.colliderect(p_rect) and p_can > 0:
            if p1_hasar_alabilir():
                p_can -= DASH_HASARI
                b_dash_hasar_verdi = True
        
        # --- SALDIRI SAYACI VE TEMİZLEME ---
        if p_yumruk_aktif:
            p_yumruk_sayaci -= 1
            if p_yumruk_sayaci <= 0: p_yumruk_aktif = False
        
        if p_tekme_aktif:
            p_tekme_sayaci -= 1
            if p_tekme_sayaci <= 0: p_tekme_aktif = False
            
        if b_yumruk_aktif:
            b_yumruk_sayaci -= 1
            if b_yumruk_sayaci <= 0: b_yumruk_aktif = False
        
        if b_tekme_aktif:
            b_tekme_sayaci -= 1
            if b_tekme_sayaci <= 0: b_tekme_aktif = False

        # --- MERMİ FİZİĞİ VE ÇARPIŞMA ---
        if p_mer_aktif:
            p_mer_x += p_mer_hiz
            p_mer_rect = pygame.Rect(p_mer_x, p_mer_y, 10, 10)
            b_rect = pygame.Rect(b_x, b_y, b_w, b_h)
            
            if p_mer_rect.colliderect(b_rect) and b_can > 0 and p2_hasar_alabilir():
                p_mer_aktif = False
                if b_engelleme_aktif:
                    b_can -= yet_hasari * 0.1 
                else:
                    b_can -= yet_hasari
                    b_stun_bitis_zamani = mevcut_zaman + YETENEK_STUN_SURESI
                    p_cekme_hakki_bitis_zamani = mevcut_zaman + 2000
                b_engelleme_aktif = False
                b_engelleme_sayaci = 0

            if p_mer_x < 0 or p_mer_x > GENISLIK:
                p_mer_aktif = False

        if b_mer_aktif:
            b_mer_x += b_mer_hiz
            b_mer_rect = pygame.Rect(b_mer_x, b_mer_y, 10, 10)
            p_rect = pygame.Rect(p_x, p_y, p_w, p_h)
            
            if b_mer_rect.colliderect(p_rect) and p_can > 0 and p1_hasar_alabilir():
                b_mer_aktif = False
                p_can -= yet_hasari
                p_stun_bitis_zamani = mevcut_zaman + YETENEK_STUN_SURESI
                b_cekme_hakki_bitis_zamani = mevcut_zaman + 2000
            
            if b_mer_x < 0 or b_mer_x > GENISLIK:
                b_mer_aktif = False
        
        # --- ÇİZİM ---
        ekran.fill(GOKYUZU) 
        pygame.draw.rect(ekran, ZEMIN_RENGI, (0, zemin_y, GENISLIK, zemin_yuksekligi))
        
        # Can Barları
        pygame.draw.rect(ekran, SIYAH, (p_bar_x, p_bar_y, bar_genislik, bar_yukseklik))
        pygame.draw.rect(ekran, SIYAH, (b_bar_x, b_bar_y, bar_genislik, bar_yukseklik))
        
        p_can_genislik = int(bar_genislik * (p_can / p_max_can))
        p_can_rect = pygame.Rect(p_bar_x, p_bar_y, p_can_genislik, bar_yukseklik)
        pygame.draw.rect(ekran, CAN_DOLU_P, p_can_rect)

        b_can_genislik = int(bar_genislik * (b_can / b_max_can))
        b_can_rect = pygame.Rect(b_bar_x + bar_genislik - b_can_genislik, b_bar_y, b_can_genislik, bar_yukseklik)
        pygame.draw.rect(ekran, CAN_DOLU_B, b_can_rect)
        
        # Karakter Çizimi
        p_cizim_renk = OYUNCU_RENK
        b_cizim_renk = BOT_RENK
        
        if p_dash_aktif: p_cizim_renk = DASH_RENK
        if b_dash_aktif: b_cizim_renk = DASH_RENK
        
        
        #P1 için Animasyonlar
        if p_yumruk_aktif and mevcut_animasyon != fist_anim and mevcut_animasyon != r_fist_anim:
            current_frame = 0
            if p_yon == 1:
                mevcut_animasyon = fist_anim
            else:
                mevcut_animasyon = r_fist_anim
        elif p_tekme_aktif and mevcut_animasyon != kick_anim and mevcut_animasyon != r_kick_anim:
            current_frame = 0
            if p_yon == 1:
                mevcut_animasyon = kick_anim
            else:
                mevcut_animasyon = r_kick_anim
        elif p_x_hiz == 0 and p_y_hiz == 0 and p_yon == 1 and mevcut_animasyon != idle_anim and not p_yumruk_aktif and not p_tekme_aktif:
            current_frame = 0
            mevcut_animasyon = idle_anim
        elif p_x_hiz == 0 and p_y_hiz == 0 and p_yon == -1 and mevcut_animasyon != r_idle_anim and not p_yumruk_aktif and not p_tekme_aktif:
            current_frame = 0;
            mevcut_animasyon = r_idle_anim
        elif p_x_hiz > 0 and mevcut_animasyon != walk_anim and not p_yumruk_aktif and not p_tekme_aktif:
            current_frame = 0
            mevcut_animasyon = walk_anim
        elif p_x_hiz < 0 and mevcut_animasyon != r_walk_anim and not p_yumruk_aktif and not p_tekme_aktif:
            current_frame = 0
            mevcut_animasyon = r_walk_anim
        if mevcut_animasyon == idle_anim:
            if mevcut_zaman - frame_start_time > idle_durations[current_frame] and p_x_hiz == 0 and p_y_hiz == 0:  
                current_frame = (current_frame + 1) % len(idle_anim)  
                mevcut_animasyon = idle_anim
                frame_start_time = mevcut_zaman
        elif mevcut_animasyon == kick_anim:
            if mevcut_zaman - frame_start_time > kick_durations[current_frame]:  
                current_frame = (current_frame + 1) % len(kick_anim)  
                mevcut_animasyon = kick_anim
                frame_start_time = mevcut_zaman
        elif mevcut_animasyon == r_kick_anim:
            if mevcut_zaman - frame_start_time > r_kick_durations[current_frame]:  
                current_frame = (current_frame + 1) % len(r_kick_anim)  
                mevcut_animasyon = r_kick_anim
                frame_start_time = mevcut_zaman
        elif mevcut_animasyon == fist_anim:
            if mevcut_zaman - frame_start_time > fist_durations[current_frame]:  
                current_frame = (current_frame + 1) % len(fist_anim)  
                mevcut_animasyon = fist_anim
                frame_start_time = mevcut_zaman
        elif mevcut_animasyon == r_fist_anim:
            if mevcut_zaman - frame_start_time > r_fist_durations[current_frame]:  
                current_frame = (current_frame + 1) % len(r_fist_anim)  
                mevcut_animasyon = r_fist_anim
                frame_start_time = mevcut_zaman
        elif mevcut_animasyon == walk_anim:
            if mevcut_zaman - frame_start_time > walk_durations[current_frame]:  
                current_frame = (current_frame + 1) % len(walk_anim)  
                mevcut_animasyon = walk_anim
                frame_start_time = mevcut_zaman
        elif mevcut_animasyon == r_walk_anim:
            if mevcut_zaman - frame_start_time > r_walk_durations[current_frame]:  
                current_frame = (current_frame + 1) % len(r_walk_anim)  
                mevcut_animasyon = r_walk_anim
                frame_start_time = mevcut_zaman
        elif mevcut_animasyon == r_idle_anim:
            if mevcut_zaman - frame_start_time > r_idle_durations[current_frame]:  
                current_frame = (current_frame + 1) % len(r_idle_anim)  
                mevcut_animasyon = r_idle_anim
                frame_start_time = mevcut_zaman
        
        
        
        #Bot/P2 için Animasyonlar
        
        
        
        
        if b_yumruk_aktif and p2mevcut_animasyon != rfist_anim and p2mevcut_animasyon != r_rfist_anim:
            p2current_frame = 0
            if b_yon == 1:
                p2mevcut_animasyon = rfist_anim
            else:
                p2mevcut_animasyon = r_rfist_anim
        elif b_tekme_aktif and p2mevcut_animasyon != rkick_anim and p2mevcut_animasyon != r_rkick_anim:
            p2current_frame = 0
            if b_yon == 1:
                p2mevcut_animasyon = rkick_anim
            else:
                p2mevcut_animasyon = r_rkick_anim
        elif b_x_hiz == 0 and b_y_hiz == 0 and b_yon == 1 and p2mevcut_animasyon != ridle_anim and not b_yumruk_aktif and not b_tekme_aktif:
            p2current_frame = 0
            p2mevcut_animasyon = ridle_anim
        elif b_x_hiz == 0 and b_y_hiz == 0 and b_yon == -1 and p2mevcut_animasyon != r_ridle_anim and not b_yumruk_aktif and not b_tekme_aktif:
            p2current_frame = 0;
            p2mevcut_animasyon = r_ridle_anim
        elif b_x_hiz > 0 and p2mevcut_animasyon != rwalk_anim and not b_yumruk_aktif and not b_tekme_aktif:
            p2current_frame = 0
            p2mevcut_animasyon = rwalk_anim
        elif b_x_hiz < 0 and p2mevcut_animasyon != r_rwalk_anim and not b_yumruk_aktif and not b_tekme_aktif:
            p2current_frame = 0
            p2mevcut_animasyon = r_rwalk_anim
        if p2mevcut_animasyon == ridle_anim:
            if mevcut_zaman - p2frame_start_time > ridle_durations[p2current_frame] and b_x_hiz == 0 and b_y_hiz == 0:  
                p2current_frame = (p2current_frame + 1) % len(ridle_anim)  
                p2mevcut_animasyon = ridle_anim
                p2frame_start_time = mevcut_zaman
        elif p2mevcut_animasyon == rkick_anim:
            if mevcut_zaman - p2frame_start_time > rkick_durations[p2current_frame]:  
                p2current_frame = (p2current_frame + 1) % len(rkick_anim)  
                p2mevcut_animasyon = rkick_anim
                p2frame_start_time = mevcut_zaman
        elif p2mevcut_animasyon == r_rkick_anim:
            if mevcut_zaman - p2frame_start_time > r_rkick_durations[p2current_frame]:  
                p2current_frame = (p2current_frame + 1) % len(r_rkick_anim)  
                p2mevcut_animasyon = r_rkick_anim
                p2frame_start_time = mevcut_zaman
        elif p2mevcut_animasyon == rfist_anim:
            if mevcut_zaman - p2frame_start_time > rfist_durations[p2current_frame]:  
                p2current_frame = (p2current_frame + 1) % len(rfist_anim)  
                p2mevcut_animasyon = rfist_anim
                p2frame_start_time = mevcut_zaman
        elif p2mevcut_animasyon == r_rfist_anim:
            if mevcut_zaman - p2frame_start_time > r_rfist_durations[p2current_frame]:  
                p2current_frame = (p2current_frame + 1) % len(r_rfist_anim)  
                p2mevcut_animasyon = r_rfist_anim
                p2frame_start_time = mevcut_zaman
        elif p2mevcut_animasyon == rwalk_anim:
            if mevcut_zaman - p2frame_start_time > rwalk_durations[p2current_frame]:  
                p2current_frame = (p2current_frame + 1) % len(rwalk_anim)  
                p2mevcut_animasyon = rwalk_anim
                p2frame_start_time = mevcut_zaman
        elif p2mevcut_animasyon == r_rwalk_anim:
            if mevcut_zaman - p2frame_start_time > r_rwalk_durations[p2current_frame]:  
                p2current_frame = (p2current_frame + 1) % len(r_rwalk_anim)  
                p2mevcut_animasyon = r_rwalk_anim
                p2frame_start_time = mevcut_zaman
        elif p2mevcut_animasyon == r_ridle_anim:
            if mevcut_zaman - p2frame_start_time > r_ridle_durations[p2current_frame]:  
                p2current_frame = (p2current_frame + 1) % len(r_ridle_anim)  
                p2mevcut_animasyon = r_ridle_anim
                p2frame_start_time = mevcut_zaman
        ekran.blit(p2mevcut_animasyon[p2current_frame], (b_x - 30, b_y, b_w, b_h))
        ekran.blit(mevcut_animasyon[current_frame], (p_x - 30, p_y, p_w, p_h))
        
        if b_engelleme_aktif:
            pygame.draw.rect(ekran, ENGELLEME_RENK, (b_x, b_y, b_w, b_h), 4)

        if p1_stun_aktif:
             pygame.draw.rect(ekran, STUN_PARLAMA_RENGI, (p_x, p_y, p_w, p_h), 5)
        if p2_stun_aktif:
             pygame.draw.rect(ekran, STUN_PARLAMA_RENGI, (b_x, b_y, b_w, b_h), 5)
        
        # Hitboxları Hesapla
        if p_yumruk_aktif:
            yumruk_genislik, yumruk_yukseklik = 30, 20
            yumruk_x = p_x + p_w if p_yon == 1 else p_x - yumruk_genislik
            yumruk_rect = pygame.Rect(yumruk_x, p_y + 30, yumruk_genislik, yumruk_yukseklik)
            
        
        if p_tekme_aktif:
            tekme_x = p_x + p_w if p_yon == 1 else p_x - tekme_menzili_w
            tekme_rect = pygame.Rect(tekme_x, p_y + p_h - tekme_menzili_h - 25, tekme_menzili_w, tekme_menzili_h)
            
            
        if b_yumruk_aktif:
            yumruk_genislik, yumruk_yukseklik = 30, 20
            yumruk_x = b_x + b_w if b_yon == 1 else b_x - yumruk_genislik
            yumruk_rect = pygame.Rect(yumruk_x, b_y + 30, yumruk_genislik, yumruk_yukseklik)
            
        
        if b_tekme_aktif:
            tekme_x = b_x + b_w if b_yon == 1 else b_x - tekme_menzili_w
            tekme_rect = pygame.Rect(tekme_x, b_y + b_h - tekme_menzili_h - 25, tekme_menzili_w, tekme_menzili_h)
            
        
        # Mermi Çizimi
        if p_mer_aktif:
            pygame.draw.circle(ekran, MERMI_RENK_P, (int(p_mer_x), int(p_mer_y)), 10)
        if b_mer_aktif:
            pygame.draw.circle(ekran, MERMI_RENK_B, (int(b_mer_x), int(b_mer_y)), 10)

        # --- COOLDOWN GÖSTERGELERİ ---
        p_cooldown_x = 100
        p_cooldown_y = YUKSEKLIK - 50
        radius = 35
        spacing = 90
        
        draw_cooldown_circle(ekran, p_cooldown_x, p_cooldown_y, radius, 
                            p_yumruk_cooldown_orani, pygame.key.name(p1_yumruk), 
                            p_yumruk_cooldown_kaldi, not p_yumruk_aktif and p_yumruk_cooldown_orani >= 1.0)
        
        draw_cooldown_circle(ekran, p_cooldown_x + spacing, p_cooldown_y, radius,
                            p_tekme_cooldown_orani, pygame.key.name(p1_tekme),
                            p_tekme_cooldown_kaldi, not p_tekme_aktif and p_tekme_cooldown_orani >= 1.0)
        
        draw_cooldown_circle(ekran, p_cooldown_x + spacing * 2, p_cooldown_y, radius,
                            p_dash_cooldown_orani, pygame.key.name(p1_dash),
                            p_dash_cooldown_kaldi, not p_dash_aktif and p_dash_cooldown_orani >= 1.0)
        
        draw_cooldown_circle(ekran, p_cooldown_x + spacing * 3, p_cooldown_y, radius,
                            p_yet_cooldown_orani, pygame.key.name(p1_skill),
                            p_yet_cooldown_kaldi, not p_mer_aktif and p_yet_cooldown_orani >= 1.0)
        
        b_cooldown_x = GENISLIK - 100
        b_cooldown_y = YUKSEKLIK - 50
        
        draw_cooldown_circle(ekran, b_cooldown_x - spacing * 3, b_cooldown_y, radius,
                            b_yumruk_cooldown_orani, pygame.key.name(p2_yumruk),
                            b_yumruk_cooldown_kaldi, not b_yumruk_aktif and b_yumruk_cooldown_orani >= 1.0)
        
        draw_cooldown_circle(ekran, b_cooldown_x - spacing * 2, b_cooldown_y, radius,
                            b_tekme_cooldown_orani, pygame.key.name(p2_tekme),
                            b_tekme_cooldown_kaldi, not b_tekme_aktif and b_tekme_cooldown_orani >= 1.0)
        
        draw_cooldown_circle(ekran, b_cooldown_x - spacing, b_cooldown_y, radius,
                            b_dash_cooldown_orani, pygame.key.name(p2_dash),
                            b_dash_cooldown_kaldi, not b_dash_aktif and b_dash_cooldown_orani >= 1.0)
        
        draw_cooldown_circle(ekran, b_cooldown_x, b_cooldown_y, radius,
                            b_yet_cooldown_orani, pygame.key.name(p2_skill),
                            b_yet_cooldown_kaldi, not b_mer_aktif and b_yet_cooldown_orani >= 1.0)

        # --- BİTİŞ KONTROLÜ ---
        if p_can <= 0 or b_can <= 0:
            oyun_durumu = "OYUN_BITTI"
            if p_can <= 0 and b_can <= 0:
                kazanan_metni = "BERABERLİK!"
            elif p_can <= 0:
                kazanan_metni = "2. OYUNCU KAZANDI!"
            else:
                kazanan_metni = "1. OYUNCU KAZANDI!"

    
    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()
