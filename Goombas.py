import pygame as pg
from Const import *

BAT_DEBUG = False

class Goombas:
    
    def __init__(self, vi_tri_x, vi_tri_y, huong_di_chuyen):

        self.trang_thai = 0
        
        self.van_toc_ngang = 1 if huong_di_chuyen else -1
        
        self.van_toc_doc = 0
        
        self.dang_cham_dat = False

        self.hinh_chu_nhat = pg.Rect(vi_tri_x, vi_tri_y, 32, 32)

        self.chi_so_anh_hien_tai = 0
        
        self.bo_dem_doi_anh = 0

        self.danh_sach_anh = [
            
            pg.image.load('images/goombas_0.png').convert_alpha(),
           
            pg.image.load('images/goombas_1.png').convert_alpha(),
           
            pg.image.load('images/goombas_dead.png').convert_alpha()
        ]
        self.bo_dem_thoi_gian_chet = 0

    def in_log_debug(self, *thong_diep):
     
        if BAT_DEBUG:  
            print("[GOOMBA-DEBUG]:", *thong_diep)

    def cap_nhat_vi_tri_ngang(self, danh_sach_khoi):
       
        self.hinh_chu_nhat.x += self.van_toc_ngang

        for khoi in danh_sach_khoi:
          
            if self.hinh_chu_nhat.colliderect(khoi):
               
                if self.van_toc_ngang > 0:
                   
                    self.hinh_chu_nhat.right = khoi.left
                    
                    self.van_toc_ngang *= -1
                    
                    self.in_log_debug("Va chạm phải → quay đầu")

                elif self.van_toc_ngang < 0:
                   
                    self.hinh_chu_nhat.left = khoi.right
                    
                    self.van_toc_ngang *= -1
                    
                    self.in_log_debug("Va chạm trái → quay đầu")

    def cap_nhat_vi_tri_doc(self, danh_sach_khoi):
        
        self.hinh_chu_nhat.y += self.van_toc_doc
        
        self.dang_cham_dat = False

        for khoi in danh_sach_khoi:
            if self.hinh_chu_nhat.colliderect(khoi):

                if self.van_toc_doc > 0:
                   
                    self.hinh_chu_nhat.bottom = khoi.top
                    
                    self.van_toc_doc = 0
                    
                    self.dang_cham_dat = True

    def cap_nhat_hoat_hinh(self):

        self.bo_dem_doi_anh += 1
        
        if self.bo_dem_doi_anh == 12:
            self.chi_so_anh_hien_tai = 1
            
        elif self.bo_dem_doi_anh == 24:
            self.chi_so_anh_hien_tai = 0
            self.bo_dem_doi_anh = 0  
        
    def cap_nhat(self, danh_sach_khoi):

        if self.trang_thai == 0:

            self.cap_nhat_hoat_hinh()

            if not self.dang_cham_dat:

                self.van_toc_doc += GRAVITY

            self.cap_nhat_vi_tri_ngang(danh_sach_khoi)
            
            self.cap_nhat_vi_tri_doc(danh_sach_khoi)

        elif self.trang_thai == -1:

            self.bo_dem_thoi_gian_chet -= 1
            
            if self.bo_dem_thoi_gian_chet <= 0:
                return "dead"

        return "alive"

    def bi_giam(self):
        
        self.trang_thai = -1
        
        self.chi_so_anh_hien_tai = 2
        
        self.bo_dem_thoi_gian_chet = 30

    def ve(self, man_hinh):
        
        man_hinh.blit(self.danh_sach_anh[self.chi_so_anh_hien_tai], self.hinh_chu_nhat)

