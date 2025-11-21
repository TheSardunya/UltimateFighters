import pygame
import sys
import math
import random 

# 1. AYARLAR VE KURULUM
pygame.init()

# Tam Ekran
ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
GENISLIK = info.current_w
YUKSEKLIK = info.current_h

pygame.display.set_caption("Ultimate Fighter (Menü)")

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
bot_hizlanma = p_hizlanma * 0.9 # Bot için özel hızlanma

# --- OYUNCU VE BOT TEMEL DEĞİŞKENLERİ ---
p_w, p_h = 80, 120
b_w, b_h = 80, 120
p_max_can, b_max_can = 100, 100 

# Yumruk/Tekme
yumruk_suresi = 15      
yumruk_bekleme_suresi = 2000 
yumruk_hasari = 5
tekme_suresi = 20
tekme_bekleme_suresi = 3000 
tekme_hasari = 7 
tekme_menzili_w, tekme_menzili_h = 80, 30 

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

# P2/BOT
b_x, b_y, b_y_hiz, b_x_hiz, b_yon, b_can, b_yumruk_aktif, b_yumruk_sayaci, b_son_vurus_zamani, b_tekme_aktif, b_tekme_sayaci, b_son_tekme_zamani = 0, 0, 0, 0, -1, 100, False, 0, 0, False, 0, 0
b_mer_aktif, b_mer_x, b_mer_y, b_mer_hiz, b_son_yet_zamani = False, 0, 0, 0, 0
b_stun_bitis_zamani = 0 
b_cekme_hakki_bitis_zamani = 0
b_dash_aktif = False
b_dash_sayaci = 0
b_son_dash_zamani = 0
b_dash_hasar_verdi = False 


ai_bekleme_sayaci = 0 
b_engelleme_aktif = False 
b_engelleme_sayaci = 0 # Engellemenin ne zaman biteceğini tutar (frame cinsinden)

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
kolay_rect = pygame.Rect(center_x - button_w // 2, center_y - 100, button_w, button_h)
zor_rect = pygame.Rect(center_x - button_w // 2, center_y + 20, button_w, button_h)
tekrar_oyna_rect = pygame.Rect(center_x - button_w // 2, center_y + 150, button_w, button_h)


# --- YARDIMCI FONKSİYONLAR ---
def draw_button(ekran, rect, renk, metin, font, text_color):
    pygame.draw.rect(ekran, renk, rect)
    text_surface = font.render(metin, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    ekran.blit(text_surface, text_rect)

def reset_game_state():
    """Tüm karakter değişkenlerini başlangıç değerlerine sıfırlar."""
    global p_x, p_y, p_y_hiz, p_x_hiz, p_yon, p_can, p_yumruk_aktif, p_yumruk_sayaci, p_son_vurus_zamani, p_tekme_aktif, p_tekme_sayaci, p_son_tekme_zamani, p_mer_aktif, p_mer_x, p_mer_y, p_mer_hiz, p_son_yet_zamani, p_stun_bitis_zamani, p_cekme_hakki_bitis_zamani, p_dash_aktif, p_dash_sayaci, p_son_dash_zamani, p_dash_hasar_verdi
    global b_x, b_y, b_y_hiz, b_x_hiz, b_yon, b_can, b_yumruk_aktif, b_yumruk_sayaci, b_son_vurus_zamani, b_tekme_aktif, b_tekme_sayaci, b_son_tekme_zamani, b_mer_aktif, b_mer_x, b_mer_y, b_mer_hiz, b_son_yet_zamani, b_stun_bitis_zamani, b_cekme_hakki_bitis_zamani, b_dash_aktif, b_dash_sayaci, b_son_dash_zamani, b_dash_hasar_verdi
    global ai_bekleme_sayaci, b_engelleme_aktif, b_engelleme_sayaci, oyun_durumu, kazanan_metni

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

    ai_bekleme_sayaci = 0
    b_engelleme_aktif = False
    b_engelleme_sayaci = 0
    kazanan_metni = ""

def bot_can_ziplayabilir():
    """Botun zıplama koşulunu kontrol eder (Sadece yerde olmayı kontrol eder)."""
    return b_y + b_h >= zemin_y - 1

def p1_hasar_alabilir():
    """P1'in hasar alıp alamayacağını kontrol eder (Dash sırasında hasar almaz)."""
    # Dash aktif değilse ve stun aktif değilse hasar alabilir
    return not p_dash_aktif and not p_stun_bitis_zamani > pygame.time.get_ticks()

def p2_hasar_alabilir():
    """P2/Bot'un hasar alıp alamayacağını kontrol eder (Dash sırasında hasar almaz)."""
    # Dash aktif değilse ve stun aktif değilse hasar alabilir
    return not b_dash_aktif and not b_stun_bitis_zamani > pygame.time.get_ticks()


# 2. OYUN DÖNGÜSÜ
calisiyor = True
while calisiyor:
    mevcut_zaman = pygame.time.get_ticks()
    
    # Stun Durumu Kontrolü (Hareketsizlik)
    p1_stun_aktif = mevcut_zaman < p_stun_bitis_zamani 
    p2_stun_aktif = mevcut_zaman < b_stun_bitis_zamani 
    
    # Çekme Hakkı Kontrolü (Vuranın Q/J'ye tekrar basma hakkı)
    p1_cekme_hakki_aktif = mevcut_zaman < p_cekme_hakki_bitis_zamani
    p2_cekme_hakki_aktif = mevcut_zaman < b_cekme_hakki_bitis_zamani
    
    # --- GİRDİLER (Keydown) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            calisiyor = False
            
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
                    
            elif oyun_durumu == "OYUN_BITTI":
                if tekrar_oyna_rect.collidepoint(mouse_pos):
                    reset_game_state()
                    oyun_durumu = "MENU"
                    pygame.display.set_caption("Ultimate Fighter (Menü)")


        # OYUN İÇİ GİRDİLER (Sadece oyun devam ediyorsa)
        if (oyun_durumu == "TEK_OYUNCULU" or oyun_durumu == "IKI_OYUNCULU") and event.type == pygame.KEYDOWN:
            
            # --- P1 KONTROLLERİ ---
            
            # P1 Dash (F) 
            if event.key == pygame.K_f and not p_dash_aktif and not p_yumruk_aktif and not p_tekme_aktif and not p1_stun_aktif and mevcut_zaman - p_son_dash_zamani > DASH_BEKLEME_SURESI:
                p_dash_aktif = True
                p_dash_sayaci = DASH_SURESI
                p_son_dash_zamani = mevcut_zaman
                p_dash_hasar_verdi = False
                
                dash_hiz = DASH_MESAFESI / DASH_SURESI
                p_x_hiz = dash_hiz * p_yon
                
            if not p1_stun_aktif and not p_dash_aktif: # Stun ve dash aktif değilse normal hareket ve saldırı
                
                # P1 Zıplama (W) 
                if event.key == pygame.K_w and not p_yumruk_aktif and not p_tekme_aktif:
                    if p_y + p_h >= zemin_y - 1: 
                        p_y_hiz = p_ziplama
                
                # P1 Yumruk (S) 
                if event.key == pygame.K_s and not p_tekme_aktif and mevcut_zaman - p_son_vurus_zamani > yumruk_bekleme_suresi:
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

                # P1 Tekme (E) 
                if event.key == pygame.K_e and not p_yumruk_aktif and mevcut_zaman - p_son_tekme_zamani > tekme_bekleme_suresi:
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
            
            # P1 YETENEK (Q) - ATIŞ VEYA ÇEKME
            if event.key == pygame.K_q:
                
                # 1. ÇEKME KONTROLÜ 
                if p1_cekme_hakki_aktif:
                    if p2_stun_aktif:
                        b_x = p_x - p_w if p_yon == 1 else p_x + p_w 
                        b_y = zemin_y - b_h 
                        b_yon = p_yon 
                        b_stun_bitis_zamani = 0 
                    p_cekme_hakki_bitis_zamani = 0 

                # 2. ATIŞ KONTROLÜ
                elif not p_mer_aktif and mevcut_zaman - p_son_yet_zamani > yet_bekleme_suresi:
                    p_mer_aktif = True
                    p_mer_hiz = mer_hiz * p_yon
                    p_mer_x = p_x + p_w / 2 
                    p_mer_y = p_y + p_h / 2
                    p_son_yet_zamani = mevcut_zaman

            # --- P2 KONTROLLERİ (2 Oyunculu Mod) ---
            if oyun_durumu == "IKI_OYUNCULU":
                
                # P2 Dash (K)
                if event.key == pygame.K_k and not b_dash_aktif and not b_yumruk_aktif and not b_tekme_aktif and not p2_stun_aktif and mevcut_zaman - b_son_dash_zamani > DASH_BEKLEME_SURESI:
                    b_dash_aktif = True
                    b_dash_sayaci = DASH_SURESI
                    b_son_dash_zamani = mevcut_zaman
                    b_dash_hasar_verdi = False
                    
                    dash_hiz = DASH_MESAFESI / DASH_SURESI
                    b_x_hiz = dash_hiz * b_yon

                if not p2_stun_aktif and not b_dash_aktif: # Stun ve dash aktif değilse
                    
                    # P2 Zıplama (UP)
                    if event.key == pygame.K_UP and not b_yumruk_aktif and not b_tekme_aktif:
                        if b_y + b_h >= zemin_y - 1: 
                            b_y_hiz = p_ziplama
                    
                    # P2 Yumruk (DOWN) 
                    if event.key == pygame.K_DOWN and not b_tekme_aktif and mevcut_zaman - b_son_vurus_zamani > yumruk_bekleme_suresi:
                        b_son_vurus_zamani = mevcut_zaman
                        b_yumruk_aktif = True
                        b_yumruk_sayaci = yumruk_suresi
                        
                        yumruk_genislik, yumruk_yukseklik = 50, 40
                        b_yumruk_rect = pygame.Rect(b_x + b_w if b_yon == 1 else b_x - yumruk_genislik, b_y + 30, yumruk_genislik, yumruk_yukseklik)
                        p1_rect = pygame.Rect(p_x, p_y, p_w, p_h)
                        if b_yumruk_rect.colliderect(p1_rect) and p_can > 0 and p1_hasar_alabilir():
                            p_can -= yumruk_hasari 

                    # P2 Tekme (RCTRL) 
                    if event.key == pygame.K_RCTRL and not b_yumruk_aktif and mevcut_zaman - b_son_tekme_zamani > tekme_bekleme_suresi:
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
                    
                    # P2 YETENEK (J) - ATIŞ VEYA ÇEKME
                    if event.key == pygame.K_j:
                        
                        # 1. ÇEKME KONTROLÜ
                        if p2_cekme_hakki_aktif:
                            if p1_stun_aktif:
                                p_x = b_x - b_w if b_yon == 1 else b_x + b_w 
                                p_y = zemin_y - p_h
                                p_yon = b_yon 
                                p_stun_bitis_zamani = 0 
                            
                            b_cekme_hakki_bitis_zamani = 0 

                        # 2. ATIŞ KONTROLÜ
                        elif not b_mer_aktif and mevcut_zaman - b_son_yet_zamani > yet_bekleme_suresi:
                            b_mer_aktif = True
                            b_mer_hiz = mer_hiz * b_yon
                            b_mer_x = b_x + b_w / 2 
                            b_mer_y = b_y + b_h / 2
                            b_son_yet_zamani = mevcut_zaman
                        

    # --- OYUN DURUMUNA GÖRE ÇİZİM VE GÜNCELLEME ---

    if oyun_durumu == "MENU" or oyun_durumu == "DIFFICULTY_SELECT" or oyun_durumu == "OYUN_BITTI":
        # Menü ve Ekran Çizim Kodları
        if oyun_durumu == "MENU":
            ekran.fill(SIYAH)
            title_text = FONT_BUYUK.render("ULTIMATE FIGHTER", True, BEYAZ)
            title_rect = title_text.get_rect(center=(center_x, center_y - 200))
            ekran.blit(title_text, title_rect)
            draw_button(ekran, tek_oyuncu_rect, YESIL, "1 OYUNCULU", FONT_KUCUK, SIYAH)
            draw_button(ekran, iki_oyuncu_rect, MAVI, "2 OYUNCULU", FONT_KUCUK, SIYAH)

        elif oyun_durumu == "DIFFICULTY_SELECT":
            ekran.fill(SIYAH)
            title_text = FONT_BUYUK.render("ZORLUK SEÇİMİ", True, SARI)
            title_rect = title_text.get_rect(center=(center_x, center_y - 200))
            ekran.blit(title_text, title_rect)
            draw_button(ekran, kolay_rect, YESIL, "KOLAY (Hareketsiz Bot)", FONT_KUCUK, SIYAH)
            draw_button(ekran, zor_rect, CAN_DOLU_P, "ZOR (Yapay Zeka)", FONT_KUCUK, BEYAZ)

        elif oyun_durumu == "OYUN_BITTI":
            ekran.fill(SIYAH)
            
            kazanan_text = FONT_DEV.render(kazanan_metni, True, (255, 0, 0)) 
            kazanan_rect = kazanan_text.get_rect(center=(center_x, center_y - 50))
            ekran.blit(kazanan_text, kazanan_rect)
            
            draw_button(ekran, tekrar_oyna_rect, YESIL, "MENÜYE DÖN", FONT_KUCUK, SIYAH)
    

    elif oyun_durumu == "TEK_OYUNCULU" or oyun_durumu == "IKI_OYUNCULU":
        
        tuslar = pygame.key.get_pressed()
        
        # --- P1 FİZİK VE HAREKET HESAPLAMALARI ---
        
        # DASH FİZİĞİ
        if p_dash_aktif:
            p_dash_sayaci -= 1
            if p_dash_sayaci <= 0:
                p_dash_aktif = False
                p_x_hiz = 0 
            
            if p_y + p_h < zemin_y:
                p_y_hiz += yer_cekimi * 0.5 
        
        
        # Normal hareket (Stun, dash, yumruk, tekme aktif değilse)
        elif not p_yumruk_aktif and not p_tekme_aktif and not p1_stun_aktif: 
            if tuslar[pygame.K_a]: 
                p_x_hiz -= p_hizlanma
                p_yon = -1
            if tuslar[pygame.K_d]: 
                p_x_hiz += p_hizlanma
                p_yon = 1
        
        # P1 Hız ve Konum Güncelleme
        if p1_stun_aktif: 
            p_x_hiz = 0
            p_y_hiz += yer_cekimi * 0.5 
        elif not p_dash_aktif: 
            surtunme = p_yer_surtunmesi if p_y + p_h >= zemin_y - 1 else p_hava_surtunmesi
            p_x_hiz *= surtunme 
            if abs(p_x_hiz) > p_max_hiz:
                p_x_hiz = p_max_hiz if p_x_hiz > 0 else -p_max_hiz
            p_y_hiz += yer_cekimi
            if abs(p_x_hiz) < 0.5: p_x_hiz = 0 
            
        p_x += p_x_hiz
        p_y += p_y_hiz
        if p_y + p_h > zemin_y: p_y = zemin_y - p_h; p_y_hiz = 0
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
        
        # DASH FİZİĞİ
        if b_dash_aktif:
            b_dash_sayaci -= 1
            if b_dash_sayaci <= 0:
                b_dash_aktif = False
                b_x_hiz = 0
            
            if b_y + b_h < zemin_y:
                b_y_hiz += yer_cekimi * 0.5 

        # --- P2/BOT HAREKET KONTROLLERİ ---
        
        if oyun_durumu == "IKI_OYUNCULU":
            # P2 - İKİ OYUNCULU KONTROLLER
            if not b_yumruk_aktif and not b_tekme_aktif and not p2_stun_aktif and not b_dash_aktif:
                if tuslar[pygame.K_LEFT]:
                    b_x_hiz -= p_hizlanma
                    b_yon = -1
                if tuslar[pygame.K_RIGHT]:
                    b_x_hiz += p_hizlanma
                    b_yon = 1
                    
        elif oyun_durumu == "TEK_OYUNCULU":
            # BOT KONTROLLERİ
            
            if bot_zorluk == "KOLAY":
                b_x_hiz *= p_yer_surtunmesi
                
            elif bot_zorluk == "ZOR":
                
                # --- YAPAY ZEKA MODU BELİRLEME ---
                SAVUNMA_CAN_SINIRI = b_max_can * 0.6 # %60 canın altı
                
                if b_can > SAVUNMA_CAN_SINIRI:
                    ai_modu = "SALDIRGAN"
                    # Saldırgan mod, daha hızlı hareket eder
                    hiz_carpan = 1.5 
                    yakın_menzil = 100
                    uzak_menzil = 400
                else:
                    ai_modu = "PASIF"
                    # Pasif mod, daha yavaş ve temkinli hareket eder
                    hiz_carpan = 1.0 
                    yakın_menzil = 80
                    uzak_menzil = 600

                
                # Değişkenler
                yatay_mesafe = p_x - b_x
                
                # Yönü Oyuncuya Çevir
                b_yon = 1 if yatay_mesafe > 0 else -1 
                
                # 1. BOT ÇEKME HAKKI KONTROLÜ
                if p2_cekme_hakki_aktif and p1_stun_aktif and random.random() < 0.1: # %10 şans
                    p_x = b_x - b_w if b_yon == 1 else b_x + b_w 
                    p_y = zemin_y - p_h
                    p_yon = b_yon 
                    p_stun_bitis_zamani = 0 
                    b_cekme_hakki_bitis_zamani = 0 

                
                # 2. TEMEL HAREKET, SALDIRI VE YETENEK KULLANIMI (Dash/Stun aktif değilse)
                
                if not p2_stun_aktif and not b_dash_aktif:
                    
                    
                    # --- YETENEK (Q/J) VE DASH KARARI ---

                    # Bot aktif olarak mermi atmıyorsa, dash veya yetenek kararı ver
                    if not b_mer_aktif:
                        
                        # A) DASH KARARI
                        dash_uygula = False
                        
                        if ai_modu == "SALDIRGAN":
                            # Saldırgan Dash: Gap kapatma ve hasar (Orta mesafeyi kapat)
                            if abs(yatay_mesafe) > yakın_menzil and abs(yatay_mesafe) < uzak_menzil and random.random() < 0.05: # %5 şans
                                dash_uygula = True
                        
                        elif ai_modu == "PASIF":
                            # Pasif Dash: Kaçış (Çok yakın mesafeden veya mermiden kaç)
                            if (abs(yatay_mesafe) < 100 or (p_mer_aktif and abs(p_mer_x - b_x) < 400)) and random.random() < 0.07: # %7 şansla kaç
                                dash_uygula = True
                                # Oyuncudan uzaklaş
                                b_yon = 1 if yatay_mesafe < 0 else -1 

                        
                        if dash_uygula and mevcut_zaman - b_son_dash_zamani > DASH_BEKLEME_SURESI:
                            b_dash_aktif = True
                            b_dash_sayaci = DASH_SURESI
                            b_son_dash_zamani = mevcut_zaman
                            b_dash_hasar_verdi = False
                            
                            dash_hiz = DASH_MESAFESI / DASH_SURESI
                            b_x_hiz = dash_hiz * b_yon

                        # B) MENZİL YETENEĞİ KARARI
                        
                        elif mevcut_zaman - b_son_yet_zamani > yet_bekleme_suresi:
                            
                            yet_kullanma_sansi = 0.15 if ai_modu == "SALDIRGAN" and abs(yatay_mesafe) > 500 else 0.10 # Saldırgan uzaktan sıkılırsa %15
                            
                            if ai_modu == "PASIF" and abs(yatay_mesafe) > 300: # Pasif modda mesafeyi korurken kullan
                                yet_kullanma_sansi = 0.18
                            
                            if random.random() < yet_kullanma_sansi:
                                b_mer_aktif = True
                                b_mer_hiz = mer_hiz * b_yon
                                b_mer_x = b_x + b_w / 2 
                                b_mer_y = b_y + b_h / 2
                                b_son_yet_zamani = mevcut_zaman
                                b_x_hiz = 0 # Atış sırasında dur

                    
                    # --- YAKIN DÖVÜŞ VE KONUMLANMA ---
                    
                    elif not b_yumruk_aktif and not b_tekme_aktif:
                        
                        
                        if abs(yatay_mesafe) < yakın_menzil + 20: # Yumruk/Tekme menzili
                            
                            # YUMRUK KARARI (Hızlı ve sık)
                            yumruk_sansi = 0.25 if ai_modu == "SALDIRGAN" else 0.08
                            if mevcut_zaman - b_son_vurus_zamani > yumruk_bekleme_suresi * 0.5 and random.random() < yumruk_sansi:
                                b_son_vurus_zamani = mevcut_zaman
                                b_yumruk_aktif = True
                                b_yumruk_sayaci = yumruk_suresi
                                b_x_hiz = 0
                                
                            # TEKME KARARI (Yavaş ama güçlü)
                            tekme_sansi = 0.10 if ai_modu == "SALDIRGAN" else 0.03
                            if mevcut_zaman - b_son_tekme_zamani > tekme_bekleme_suresi and random.random() < tekme_sansi:
                                b_son_tekme_zamani = mevcut_zaman
                                b_tekme_aktif = True
                                b_tekme_sayaci = tekme_suresi
                                b_x_hiz = 0
                                
                            # ENGELLEME KARARI (Pasif mod öncelikli)
                            elif ai_modu == "PASIF" and random.random() < 0.15: # %15 Engelle
                                b_engelleme_aktif = True
                                b_engelleme_sayaci = random.randint(30, 90) # 0.5 ile 1.5 saniye
                                b_x_hiz = 0

                            # YAKINDAKİ HAREKET (Pasif modda geri çekilme şansı)
                            else: # Saldırı ve engelleme kararı yoksa hareket et
                                if ai_modu == "PASIF" and random.random() < 0.1:
                                    # Geri Çekil
                                    b_x_hiz += bot_hizlanma * hiz_carpan * (-b_yon)
                                elif ai_modu == "SALDIRGAN":
                                    # Çok yakında olsa bile hafifçe ittirmeye devam et
                                    if yatay_mesafe > 0: b_x_hiz += bot_hizlanma * hiz_carpan
                                    else: b_x_hiz -= bot_hizlanma * hiz_carpan
                                else:
                                    # Pasif: Dur
                                    b_x_hiz *= p_yer_surtunmesi * 0.5

                            
                        
                        elif abs(yatay_mesafe) > yakın_menzil: # Yakınlaşma/Uzaklaşma

                            if ai_modu == "SALDIRGAN":
                                # Oyuncuya doğru koş (Yakınlaş)
                                if yatay_mesafe > 0:
                                    b_x_hiz += bot_hizlanma * hiz_carpan
                                else:
                                    b_x_hiz -= bot_hizlanma * hiz_carpan
                            
                            elif ai_modu == "PASIF":
                                # Kontrollü hareket (Çok uzaksa yakınlaş, ideal mesafeye gelince dur)
                                if abs(yatay_mesafe) > uzak_menzil:
                                     # Oyuncuya doğru yürü
                                    if yatay_mesafe > 0: b_x_hiz += bot_hizlanma * hiz_carpan
                                    else: b_x_hiz -= bot_hizlanma * hiz_carpan
                                else:
                                    # Yavaşla/Dur
                                    b_x_hiz *= p_yer_surtunmesi * 0.5
                                
                            # Zıplama (Her iki modda da rastgele)
                            if bot_can_ziplayabilir() and random.random() < 0.005:
                                b_y_hiz = p_ziplama 
                                
                    
                    # Engellemeyi bitirme sayacı
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
        if b_y + b_h > zemin_y: b_y = zemin_y - b_h; b_y_hiz = 0
        if b_x < 0: b_x, b_x_hiz = 0, 0
        if b_x > GENISLIK - b_w: b_x, b_x_hiz = GENISLIK - b_w, 0
        
        # P2/BOT DASH HASAR KONTROLÜ
        if b_dash_aktif and not b_dash_hasar_verdi and b_rect.colliderect(p_rect) and p_can > 0:
            if p1_hasar_alabilir():
                p_can -= DASH_HASARI
                b_dash_hasar_verdi = True
        
        # --- SALDIRI SAYACI VE TEMİZLEME ---

        # P1 Saldırı Temizleme
        if p_yumruk_aktif:
            p_yumruk_sayaci -= 1
            if p_yumruk_sayaci <= 0: p_yumruk_aktif = False
        
        if p_tekme_aktif:
            p_tekme_sayaci -= 1
            if p_tekme_sayaci <= 0: p_tekme_aktif = False
            
        # P2/Bot Saldırı Temizleme
        if b_yumruk_aktif:
            b_yumruk_sayaci -= 1
            if b_yumruk_sayaci <= 0: b_yumruk_aktif = False
        
        if b_tekme_aktif:
            b_tekme_sayaci -= 1
            if b_tekme_sayaci <= 0: b_tekme_aktif = False


        # --- MERMİ FİZİĞİ VE ÇARPIŞMA ---
        
        # P1 Mermisi
        if p_mer_aktif:
            p_mer_x += p_mer_hiz
            
            p_mer_rect = pygame.Rect(p_mer_x, p_mer_y, 10, 10)
            b_rect = pygame.Rect(b_x, b_y, b_w, b_h)
            
            # Çarpışma Kontrolü
            if p_mer_rect.colliderect(b_rect) and b_can > 0 and p2_hasar_alabilir():
                p_mer_aktif = False
                
                if b_engelleme_aktif:
                    b_can -= yet_hasari * 0.1 
                else:
                    b_can -= yet_hasari
                    b_stun_bitis_zamani = mevcut_zaman + YETENEK_STUN_SURESI
                    p_cekme_hakki_bitis_zamani = mevcut_zaman + 2000 # 2 saniye içinde Q'ya basma hakkı
                b_engelleme_aktif = False
                b_engelleme_sayaci = 0

            # Ekran dışı kontrolü
            if p_mer_x < 0 or p_mer_x > GENISLIK:
                p_mer_aktif = False

        # P2/Bot Mermisi
        if b_mer_aktif:
            b_mer_x += b_mer_hiz
            
            b_mer_rect = pygame.Rect(b_mer_x, b_mer_y, 10, 10)
            p_rect = pygame.Rect(p_x, p_y, p_w, p_h)
            
            # Çarpışma Kontrolü
            if b_mer_rect.colliderect(p_rect) and p_can > 0 and p1_hasar_alabilir():
                b_mer_aktif = False
                p_can -= yet_hasari
                p_stun_bitis_zamani = mevcut_zaman + YETENEK_STUN_SURESI
                b_cekme_hakki_bitis_zamani = mevcut_zaman + 2000 # 2 saniye içinde J'ye basma hakkı
            
            # Ekran dışı kontrolü
            if b_mer_x < 0 or b_mer_x > GENISLIK:
                b_mer_aktif = False
        

        # --- ÇİZİM ---
        ekran.fill(GOKYUZU) 
        pygame.draw.rect(ekran, ZEMIN_RENGI, (0, zemin_y, GENISLIK, zemin_yuksekligi))
        
        # Can Barları Arka Plan
        pygame.draw.rect(ekran, SIYAH, (p_bar_x, p_bar_y, bar_genislik, bar_yukseklik))
        pygame.draw.rect(ekran, SIYAH, (b_bar_x, b_bar_y, bar_genislik, bar_yukseklik))
        
        # P1 Can Barı
        p_can_genislik = int(bar_genislik * (p_can / p_max_can))
        p_can_rect = pygame.Rect(p_bar_x, p_bar_y, p_can_genislik, bar_yukseklik)
        pygame.draw.rect(ekran, CAN_DOLU_P, p_can_rect)

        # P2 Can Barı (Sağdan sola doğru)
        b_can_genislik = int(bar_genislik * (b_can / b_max_can))
        b_can_rect = pygame.Rect(b_bar_x + bar_genislik - b_can_genislik, b_bar_y, b_can_genislik, bar_yukseklik)
        pygame.draw.rect(ekran, CAN_DOLU_B, b_can_rect)
        
        # Karakter Çizimi
        p_cizim_renk = OYUNCU_RENK
        b_cizim_renk = BOT_RENK
        
        if p_dash_aktif: p_cizim_renk = DASH_RENK
        if b_dash_aktif: b_cizim_renk = DASH_RENK
        
        # P1 Vücut
        pygame.draw.rect(ekran, p_cizim_renk, (p_x, p_y, p_w, p_h))
        # P2 Vücut
        pygame.draw.rect(ekran, b_cizim_renk, (b_x, b_y, b_w, b_h))
        
        # Engelleme Çizimi (Bot için)
        if b_engelleme_aktif:
            pygame.draw.rect(ekran, ENGELLEME_RENK, (b_x, b_y, b_w, b_h), 4)

        # Stun Parlaması
        if p1_stun_aktif:
             pygame.draw.rect(ekran, STUN_PARLAMA_RENGI, (p_x, p_y, p_w, p_h), 5)
        if p2_stun_aktif:
             pygame.draw.rect(ekran, STUN_PARLAMA_RENGI, (b_x, b_y, b_w, b_h), 5)
        
        # Saldırı Kutularını Çiz
        
        # P1 Yumruk
        if p_yumruk_aktif:
            yumruk_genislik, yumruk_yukseklik = 50, 40
            yumruk_x = p_x + p_w if p_yon == 1 else p_x - yumruk_genislik
            yumruk_rect = pygame.Rect(yumruk_x, p_y + 30, yumruk_genislik, yumruk_yukseklik)
            pygame.draw.rect(ekran, YUMRUK_RENGI, yumruk_rect, 2)
        
        # P1 Tekme
        if p_tekme_aktif:
            tekme_x = p_x + p_w if p_yon == 1 else p_x - tekme_menzili_w
            tekme_rect = pygame.Rect(tekme_x, p_y + p_h - tekme_menzili_h, tekme_menzili_w, tekme_menzili_h)
            pygame.draw.rect(ekran, TEKME_RENGI, tekme_rect, 2)
            
        # P2/Bot Yumruk
        if b_yumruk_aktif:
            yumruk_genislik, yumruk_yukseklik = 50, 40
            yumruk_x = b_x + b_w if b_yon == 1 else b_x - yumruk_genislik
            yumruk_rect = pygame.Rect(yumruk_x, b_y + 30, yumruk_genislik, yumruk_yukseklik)
            pygame.draw.rect(ekran, YUMRUK_RENGI, yumruk_rect, 2)
        
        # P2/Bot Tekme
        if b_tekme_aktif:
            tekme_x = b_x + b_w if b_yon == 1 else b_x - tekme_menzili_w
            tekme_rect = pygame.Rect(tekme_x, b_y + b_h - tekme_menzili_h, tekme_menzili_w, tekme_menzili_h)
            pygame.draw.rect(ekran, TEKME_RENGI, tekme_rect, 2)
        
        # Mermi Çizimi
        if p_mer_aktif:
            pygame.draw.circle(ekran, MERMI_RENK_P, (int(p_mer_x), int(p_mer_y)), 10)
        if b_mer_aktif:
            pygame.draw.circle(ekran, MERMI_RENK_B, (int(b_mer_x), int(b_mer_y)), 10)


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
