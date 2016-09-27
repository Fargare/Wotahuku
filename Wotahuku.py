# -*- coding: utf-8 -*-
from datetime import datetime
import time
from Tkinter import *
import Image,ImageTk
import math
import sys
import pandas as pd
sys.path.append("/home/pi/Desktop/py")
sys.path.append("/home/pi/Desktop/Modules")
#from py import Scraping
import Coloring
import Managing_csv
import serial
import threading, time
import os
import RPi.GPIO as GPIO

import ScrapingWTHK as Scraping
import sys
import random
import copy

Material_Trans_dic, Kind_Trans_dic = Managing_csv.Call_Trans()
Color_dic = Scraping.Call_Color_dic()

cordinated_pairs = []# 5 cordinated pairs (Top and Bottom)

#画面サイズ
#width=640
width=480
#height=400
height=600
#画面のアスペクトがおかしいので補正をかける必要がある
#縦方向に0.74をかけることで解消できる
#正しい比での画面サイズは480*810
#縦の600に1.35をかけている

#####

Switch = [False]*5
SW_changing = [False]*5
GPIO_pin = [18,15,4,17,14]

#スイッチの状態を監視するサブスレッド
class Monitoring_switch(threading.Thread):

    def __init__(self):
        #threading.Thread.__init__(self)
        super(Monitoring_switch,self).__init__()

    def run(self):
        print "Start switch monitoring"
        #GPIO指定をGPIO番号で行う
        GPIO.setmode(GPIO.BCM)
        
        #GPIO14,15,18,20,21ピンを入力モードに設定
        #14:sleeved
        #15:material
        #18:kind
        GPIO.setup(4,GPIO.IN)
        GPIO.setup(17,GPIO.IN)
        GPIO.setup(14,GPIO.IN)
        GPIO.setup(15,GPIO.IN)
        GPIO.setup(18,GPIO.IN)
        
        
        while True:
            
            for gpio in range(5):
                if GPIO.input(GPIO_pin[gpio]) == 1 and Switch[gpio]==False:
                    #print gpio
                    Switch[gpio] = True
                elif GPIO.input(GPIO_pin[gpio]) == 0:
                    Switch[gpio] = False
                    SW_changing[gpio] = False
                else:
                    pass
            time.sleep(0.1)    
        GPIO.cleanup()
        

    
#####
class animation(object):
    H=0
    rgb = [0]*3
    now_focus = True #True:Top False:Bottom
    def __init__(self):
        #Tkinterでのgui作成の初期設定
        self.root = Tk()
        self.canvas = Canvas(self.root, width=480, height=600)
        self.canvas.pack()
        #アニメーション処理ここから

        self.root.after(0,self.run)#アニメーションの中身が書かれた，runメソッドを実行

        #アニメーション処理ここまで
        self.root.mainloop()

    def run(self):

        clothes = pd.read_csv("clothes.csv");
        BG_image = Image.open('/home/pi/Desktop/Resources/Wotahuku_BG.png')
        white_image = Image.open('/home/pi/Desktop/Resources/Wotahuku_white.png')
        shade_image = Image.open('/home/pi/Desktop/Resources/Wotahuku_shade.png')
        focus_image = Image.open('/home/pi/Desktop/Resources/Wotahuku_focus.png')
        s_BS_image = Image.open('/home/pi/Desktop/Resources/sleeve_BS.png')
        s_BL_image = Image.open('/home/pi/Desktop/Resources/sleeve_BL.png')
        s_TS_image = Image.open('/home/pi/Desktop/Resources/sleeve_TS.png')
        s_TL_image = Image.open('/home/pi/Desktop/Resources/sleeve_TL.png')
        s_n_image = Image.open('/home/pi/Desktop/Resources/sleeve_none.png')
        p_T_image = Image.open('/home/pi/Desktop/Resources/pointer_T.png')
        p_F_image = Image.open('/home/pi/Desktop/Resources/pointer_F.png')
        BG = ImageTk.PhotoImage(BG_image)
        white = ImageTk.PhotoImage(white_image)
        shade = ImageTk.PhotoImage(shade_image)
        focus = ImageTk.PhotoImage(focus_image)

        sleeve_BS = ImageTk.PhotoImage(s_BS_image)
        sleeve_BL = ImageTk.PhotoImage(s_BL_image)
        sleeve_TS = ImageTk.PhotoImage(s_TS_image)
        sleeve_TL = ImageTk.PhotoImage(s_TL_image)
        sleeve_none = ImageTk.PhotoImage(s_n_image)
        pointer_True = ImageTk.PhotoImage(p_T_image)
        pointer_False = ImageTk.PhotoImage(p_F_image)
        self.white = self.canvas.create_image(width/2,height/2,image=white)
        
        
        
        
        
        #count =[0,40,80,120]
        move = [False]*4
        count = [0]*4
        step = [30,50,50,30]
        move_length = [0]*4
        final_length = [0]*8
        
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%
        cordinated_pairs,comment, weather_str = Managing_csv.recommend_cordinate(clothes)
        
        #cordinated_pairs = [["P9090242.JPG","P9090249.JPG"],["P9090231.JPG","P9090251.JPG"]]
        print cordinated_pairs
        now_selected = 0
        now_focus = 2
            
        while True:
            #####################
            #
            now_top = clothes[clothes['file_name'].isin([cordinated_pairs[now_selected][0]])]
            now_bottom = clothes[clothes['file_name'].isin([cordinated_pairs[now_selected][1]])]
            top =  now_top.values.tolist()
            bottom =  now_bottom.values.tolist()
            #print bottom
            top_img = Image.open('/media/usb/Clothings/Tops/'+cordinated_pairs[now_selected][0])
            top_photo = ImageTk.PhotoImage(top_img.resize((240,int(316*0.74))))

            bottom_img = Image.open('/media/usb/Clothings/Bottoms/'+cordinated_pairs[now_selected][1])
            bottom_photo = ImageTk.PhotoImage(bottom_img.resize((240,int(316*0.74))))
            
            #キャンバスの消去（背景以外），（アニメーション配置ここから）
            self.canvas.delete('item')#delete item of tag"item"

            ##############Text_Animation##############
            
            #print move_length,"before"
            for i in range(4):
                if move[i] == True:
                    if count[i] < len(step):
                        move_length[i] += step[count[i]]
                        if now_focus ==0:
                            if count[i]<1:
                                final_length[i] = -(move_length[i])
                                print final_length 
                            else:
                                final_length[i] = 160-move_length[i]
                                print final_length
                            final_length[i+4]=0
                            print final_length,"after"
                        elif now_focus ==1:
                            if count[i]<1:
                                final_length[i+4] = -(move_length[i])
                            else:
                                final_length[i+4] = 160-move_length[i]
                            final_length[i] = 0
                        else:
                            now_selected = (now_selected +1)%len(cordinated_pairs)
                            clothes.to_csv("clothes.csv",index=False)
                            count[i]+=len(step)-1
                        ############
                        if  count[i]==1:
                            
                            if i== 0:
                                clothes = Managing_csv.switch_color(cordinated_pairs[now_selected][now_focus],clothes)
                            elif i== 1:
                                clothes = Managing_csv.switch_sleeved(cordinated_pairs[now_selected][now_focus],clothes)
                            elif i== 2:
                                clothes = Managing_csv.switch_material(cordinated_pairs[now_selected][now_focus],clothes)
                            elif i== 3:
                                clothes = Managing_csv.switch_kind(cordinated_pairs[now_selected][now_focus],clothes, now_focus)
                        count[i]+=1
                        
                    else:
                        final_length[i] = 0
                        final_length[i+4] = 0
                        move[i]=False
                        count[i] = 0
                        move_length[i]=0
                else:
                    final_length[i+4] = 0
                    final_length[i] = 0
            #print move_length,"after"
            #print final_length,"after"
            top_rgb=Color_dic[top[0][2]]
            top_color='#%02x%02x%02x' %(top_rgb[0],top_rgb[1],top_rgb[2])
            bottom_rgb=Color_dic[bottom[0][2]]
            bottom_color='#%02x%02x%02x' %(bottom_rgb[0],bottom_rgb[1],bottom_rgb[2])
            
            self.color = self.canvas.create_oval(370+final_length[0]-20,172-(20*0.74),370+final_length[0]+20,172+(20*0.74),fill = top_color,outline = 'black',tag='item')
            if top[0][3] =="none":
                self.news = self.canvas.create_image(370+final_length[1],227,image=sleeve_none,tag='item')
            elif top[0][3] =="long":
                self.news = self.canvas.create_image(370+final_length[1],227,image=sleeve_TL,tag='item')
            else:
                self.news = self.canvas.create_image(370+final_length[1],227,image=sleeve_TS,tag='item')
            self.text = self.canvas.create_text(370+final_length[2],277,text=Material_Trans_dic[top[0][4]],font=("Sawarabi Gothic",13),tag='item')
            self.text = self.canvas.create_text(370+final_length[3],320,text=Kind_Trans_dic[top[0][5]],font=("Sawarabi Gothic",13),tag='item')

            self.color = self.canvas.create_oval(370+final_length[4]-20,385-(20*0.74),370+final_length[4]+20,385+(20*0.74),fill = bottom_color,outline = 'black',tag='item')
            if bottom[0][3] =="none":
                self.news = self.canvas.create_image(370+final_length[5],442,image=sleeve_none,tag='item')
            elif bottom[0][3] =="long":
                self.news = self.canvas.create_image(370+final_length[5],442,image=sleeve_BL,tag='item')
            else:
                self.news = self.canvas.create_image(370+final_length[5],442,image=sleeve_BS,tag='item')
            self.text = self.canvas.create_text(370+final_length[6],492,text=Material_Trans_dic[bottom[0][4]],font=("Sawarabi Gothic",13),tag='item')
            self.text = self.canvas.create_text(370+final_length[7],535,text=Kind_Trans_dic[bottom[0][5]],font=("Sawarabi Gothic",13),tag='item')
            


            self.BG = self.canvas.create_image(width/2,height/2,image=BG,tag='item')

            ############time_text################
            time_format = "%H %M"
            day_format ="%m/%d"
            t= time.strftime(time_format,time.localtime())
            d = time.strftime(day_format,time.localtime())
            #self.text = self.canvas.create_text(188,63,text=sf,font=("Eraser",40),fill = "black",tag='item')
            self.text = self.canvas.create_text(320,35,text=t,font=("Eraser",35),fill = "white",tag='item')
            self.text = self.canvas.create_text(150,35,text=d,font=("Eraser",35),fill = "white",tag='item')
            dt = datetime.now()
            if dt.second%2 == 0:
                #self.text = self.canvas.create_text(293,63,text=":",font=("Eraser",40),fill = "black",tag='item')
                self.text = self.canvas.create_text(305,35,text=":",font=("Eraser",35),fill = "white",tag='item')

            today_comment = "今日は"+weather_str+"、"+comment
            self.text = self.canvas.create_text(240,75,text=today_comment,font=("Sawarabi Gothic",14),fill = "white",tag='item')
            
            #self.img = self.canvas.create_image(width/2,height/2,image=photo1)#背景画像貼り付け
            #self.news = self.canvas.create_image(160,630*0.76,image=photo6,tag='item')

            self.news = self.canvas.create_image(142,576*0.76,image=shade,tag='item')
            self.news = self.canvas.create_image(150,565*0.76,image=bottom_photo,tag='item')
            
            self.news = self.canvas.create_image(142,296*0.76,image=shade,tag='item')
            self.news = self.canvas.create_image(150,285*0.76,image=top_photo,tag='item')
            
            
            
            if now_focus == 0:
                self.news = self.canvas.create_image(375,320*0.76,image=focus,tag='item')
            elif now_focus ==1:
                self.news = self.canvas.create_image(375,605*0.76,image=focus,tag='item')
            if now_focus ==2:
                self.news = self.canvas.create_image(375,140*0.76,image=pointer_True,tag='item')
            else:
                self.news = self.canvas.create_image(375,140*0.76,image=pointer_False,tag='item')
            self.canvas.update()
            
            
            
            #print Switch
            ##############Switching##################
            if Switch[4] == True and SW_changing[4] == False:
                print "Switch!!!"
                
                now_focus = (now_focus+1)%3
                
                SW_changing[4] = True
                
            for i in range(4):
                if Switch[i] == True and SW_changing[i] == False:
                    print "Switch"+str(i)+"!!!"
                    
                    SW_changing[i] = True
                    move[3-i] = True

            time.sleep(0.001)
        clothes.to_csv("clothes.csv",index=False)

        #######################################

            

#スイッチが入力されたか監視するサブスレッド


if __name__ == '__main__':
    Managing_csv.reload()
    ms = Monitoring_switch()
    ms.setDaemon(True)
    ms.start()

    animation() 

