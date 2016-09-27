#-*- coding: utf-8 -*-
#pandasをインポート
#pandasは追加でインストールするライブラリみたいなもの
#インストール方法は「http://qiita.com/mojaie/items/241eb7006978e6962d05」に詳しく書いてある
#csvを書き込むのにデータフレームの考え方用いて簡単に行う。
#numpyをインポート
#インストール方法は上のURLと同じように　[python -m pip install matplotlib]でインストール
import pandas as pd
import csv
import numpy as np
import datetime
import os
import RPi.GPIO as GPIO
import Coloring
import ScrapingWTHK as Scraping
import Image
import random
import sys
#import os #ディレクトリ参照するためのインポート
#csvの表示
#print clothes;
#print clothes[["ID","color"]];
#print clothes["color"];
#print type(clothes);
#print clothes;

#sleeve,material,kindの情報を配列形式で格納して用意しておく
sleeve = ["none","long","short"]
#material = ["none","great","not so good"]
#kind = ["none","expensive","cheap"]
material = ["none", "cotton", "linen", "wool", "polyester", "denim", "knit"]
kind = [["none", "T-shirt", "shirt", "polo-shirt", "parker", "sweater", "jacket", "cardigan"], ["none", "jeans", "chinos", "cargo"]]
#kind_bottom = ["jeans", "chinos", "cargo"]
colors = Scraping.Call_Colors()

# 素材の英語と日本語の対応をディクショナリで作成
Material_Trans_dic = {"none": "タグなし",
                "cotton": "綿",
                "linen": "麻",
                "wool": "ウール",
                "polyester": "ポリエステル",
                "denim": "デニム",
                "knit": "ニット"
                }

# 種類の英語と日本語の対応をディクショナリで作成
Kind_Trans_dic = {"none": "タグなし",
                "T-shirt": "Tシャツ",
                "shirt": "シャツ",
                "polo-shirt": "ポロシャツ",
                "parker": "パーカー",
                "sweater": "セーター",
                "jacket": "ジャケット",
                "cardigan": "カーディガン",
                "jeans": "ジーパン",
                "chinos": "チノパン",
                "cargo": "カーゴパンツ"
                }

def Call_Trans():
    return Material_Trans_dic, Kind_Trans_dic

#csv書き込み
def reload():
    #書き込みにはデータフレームで行の追加を行う
    #追加データフレームdf1を作成
    #何を追加するのかを変数で作成
    first_read=False
    fp = open('clothes.csv','a+')
    csv_line_len = len(fp.readlines()) 
    print csv_line_len
    if  csv_line_len ==0:
        print "line == 0"
        first_read=True
    fp.close()
    if first_read:
        print "write_first"
        fp = open('clothes.csv','w')
        w= csv.writer(fp)
        w.writerow(['ID','file_name','color','sleeved','material','kind','lastday','position'])
        fp.close()
        
    #.csvを読み込む
    clothes = pd.read_csv("clothes.csv");
    ID = 0;#自動で割り振り
    file_name = "test.jpeg";#自動で割り振り
    #ユーザーがスイッチで入力
    color = "none";
    sleeved = "none";
    material = "none";
    kind = "none";
    lastday = "none";#いつ着たかを保存するカラム
    #df1 = pd.DataFrame([[ID,file_name,color,sleeved,material,kind,lastday]], columns=['ID','file_name','color','sleeved','material','kind','lastday']);
    #print df1;
    #csvから読み込んだclothesに新たなデータフレームと追加dfを結合
    #clothes=pd.concat([clothes,df1],ignore_index=True);
    #print clothes;

    # os.listdir('パス')
    # 指定したパス内の全てのファイルとディレクトリを要素とするリストを返す
    #files = os.listdir('C:\')

    #print clothes ["file_name"][0]
    
    #USBメモリから服の 画像データの名前を取得するため、パスの指定
    topslist = os.listdir('/media/usb0/Clothings/Tops/')
    bottomslist = os.listdir('/media/usb0/Clothings/Bottoms/')

    
    print "top_search_start"
    #まずはトップスから読み込み
    for top in topslist:
        #print topslist
        #print clothes["file_name"].tolist()
                      
        if top in clothes["file_name"].tolist():
            print "pass!!!!!!!!!"
            pass
        else:
            print "not pass!!!!"
            image_pre = Image.open('/media/usb/Clothings/Tops/'+top)
            image = image_pre.resize((150,250))
            pxs=image.load()
            total = [0,0,0]
            for w in range(image.size[0]/6,image.size[0]/6*5):
                for h in range(image.size[1]/6,image.size[1]/6*5):
                    for i in range(3):
                        total[i]+= pxs[w,h][i]
            for i in range(3):
                total[i] /= (image.size[0]/6*4*image.size[1]/6*4)
            judged_rgb = Coloring.judge_colors(Coloring.collect_color2(total))
            
            #print judged_rgb
            position = "top"
            #csvに書き込むためにフォーマットを指定
            df1 = pd.DataFrame([[ID,top,judged_rgb,sleeved,material,kind,lastday,position]], columns=['ID','file_name','color','sleeved','material','kind','lastday','position'])

            #csvから読み込んだclothesに新たなデータフレームと追加dfを結合
            clothes=pd.concat([clothes,df1],ignore_index=True)
            # print top

            #IDをインクリメント
            ID += 1

    print "-------------------"

    print "bottom_search_start"
    #次にボトムスを読み込み
    for bottom in bottomslist:
       if bottom in clothes["file_name"].tolist():
            print "pass!!!!!!!!!"

       else:
           image_pre = Image.open('/media/usb/Clothings/Bottoms/'+bottom)
           image = image_pre.resize((150,250))
           pxs=image.load()
           total = [0,0,0]
           for w in range(image.size[0]/6,image.size[0]/6*5):
               for h in range(image.size[1]/6,image.size[1]/6*5):
                   for i in range(3):
                       total[i]+= pxs[w,h][i]
           for i in range(3):
               total[i] /= (image.size[0]/6*4*image.size[1]/6*4)
           judged_rgb = Coloring.judge_colors(Coloring.collect_color2(total))
           #print judged_rgb
           position = "bottom"
           #csvに書き込むためにフォーマットを指定
           df1 = pd.DataFrame([[ID,bottom,judged_rgb,sleeved,material,kind,lastday,position]], columns=['ID','file_name','color','sleeved','material','kind','lastday','position'])
           #csvから読み込んだclothesに新たなデータフレームと追加dfを結合
           clothes=pd.concat([clothes,df1],ignore_index=True)
           #print bottom
           #IDをインクリメント
           ID += 1

    #csv書き込み
    #同じファイル名ならば上書きをする
    clothes.to_csv("clothes.csv",index=False)


#スイッチを押すことで服の「sleeved」情報を書き換え、更新する関数
def switch_sleeved(file_name,clothes):

    #clothes = pd.read_csv("clothes.csv")
    #print clothes

    cnt = 0

    #print clothes["file_name"][1]
    #print file_name

    for csv_file_name in clothes["file_name"]:
        #print "Search file_name_sleeve"
        if file_name == csv_file_name:

            #print "Hit!!!"
            #該当した行のIDを持ってくる
            clothes_ID = clothes[ (clothes.file_name == file_name)].ID.values[0]
            '''
            print clothes_ID

            print clothes["sleeved"][(clothes_ID)]

            print sleeve.index(clothes["sleeved"][clothes_ID])

            print sleeve[(sleeve.index((clothes["sleeved"][clothes_ID])))%3]
            '''
            #現在のsleeveの次の要素を代入
            clothes.loc[cnt,"sleeved"] = sleeve[(sleeve.index((clothes["sleeved"][clothes_ID]))+1)%len(sleeve)]
            #clothes.loc[cnt,"sleeved"] = sleeve[(sleeve.index((clothes["sleeved"][clothes_ID-1]))+1)%len(sleeve)]

        else:
            pass
            #print "Not Hit"
        cnt += 1

    #print clothes
        
    #clothes.to_csv("clothes.csv",index=False)
    return clothes

#スイッチを押すことで服の「material」情報を書き換え、更新する関数
def switch_material(file_name,clothes):

    #clothes = pd.read_csv("clothes.csv")
    #print clothes


    cnt = 0
    #print clothes["file_name"][1]
    #print file_name

    for csv_file_name in clothes["file_name"]:
        #print "Search file_name_material"
        if file_name == csv_file_name:

            #print "Hit!!!"
            #該当した行のIDを持ってくる
            clothes_ID = clothes[ (clothes.file_name == file_name)].ID.values[0]
            
            #print clothes_ID

            #print clothes["material"][(clothes_ID)]

            #print material.index(clothes["material"][clothes_ID])

            #print material[(material.index((clothes["material"][clothes_ID]))+1)%3]
            
            #現在のsleeveの次の要素を代入
            clothes.loc[cnt,"material"] = material[(material.index((clothes["material"][clothes_ID]))+1)%len(material)]
            #clothes.loc[cnt,"material"] = material[(material.index((clothes["material"][clothes_ID-1]))+1)%len(material)]
        else:
            pass
            #print "Not Hit"
        cnt += 1

    #print clothes

    #clothes.to_csv("clothes.csv",index=False)
    return clothes

#スイッチを押すことで服の「kind」情報を書き換え、更新する関数
def switch_kind(file_name,clothes, now_focus):

    #clothes = pd.read_csv("clothes.csv")
    #print clothes

    cnt = 0
    #print clothes["file_name"][1]
    #print file_name

    for csv_file_name in clothes["file_name"]:
        print "Search file_name_kind"
        if file_name == csv_file_name:

            print "Hit!!!"
            #該当した行のIDを持ってくる
            clothes_ID = clothes[ (clothes.file_name == file_name)].ID.values[0]
            #print clothes_ID

            #print clothes["kind"][(clothes_ID)]

            #print kind.index(clothes["kind"][clothes_ID])

            #print kind[(kind.index((clothes["kind"][clothes_ID]))+1)%3]

            #現在のkindの次の要素を代入
            clothes.loc[cnt,"kind"] = kind[now_focus][(kind[now_focus].index((clothes["kind"][clothes_ID]))+1)%len(kind[now_focus])]
            #現在のkindの次の要素を代入
            #clothes.loc[cnt,"kind"] = kind[(kind.index((clothes["kind"][clothes_ID-1]))+1)%len(kind)]
        else:
            print "Not Hit"
        cnt += 1

    #print clothes

    #clothes.to_csv("clothes.csv",index=False)
    return clothes

#スイッチを押すことで服の「sleeved」情報を書き換え、更新する関数
def switch_color(file_name,clothes):

    #clothes = pd.read_csv("clothes.csv")
    #print clothes

    cnt = 0

    
    print colors
    #print clothes["file_name"][1]
    #print file_name

    for csv_file_name in clothes["file_name"]:
        #print "Search file_name_sleeve"
        if file_name == csv_file_name:

            print "Hit!!!"
            #該当した行のIDを持ってくる
            clothes_ID = clothes[ (clothes.file_name == file_name)].ID.values[0]
            
            #print clothes_ID

            #print clothes["color"][(clothes_ID)]
            colornum = 0
            for i in range(len(colors)):
                if clothes["color"][(clothes_ID)] in colors[i]:
                    colornum =i
            
            #print colors.index(clothes["color"][clothes_ID])

            #print colors[(colors.index((clothes["color"][clothes_ID])))%3]
            
            #現在のsleeveの次の要素を代入
            clothes.loc[cnt,"color"] = colors[(colornum+1)%(len(colors))][0]
            #clothes.loc[cnt,"sleeved"] = sleeve[(sleeve.index((clothes["sleeved"][clothes_ID-1]))+1)%len(sleeve)]

        else:
            pass
            #print "Not Hit"
        cnt += 1

    #print clothes
        
    #clothes.to_csv("clothes.csv",index=False)
    return clothes

def recommend_cordinate(clothes):
    # %%%%%%%% コーディネートのレコメンド %%%%%%%%%
      
    lucky_color, image_color = Scraping.RecommendColor()
    #print lucky_color, image_color

    weather_info, oneday_weather, sleeve, comment = Scraping.RecommendSleeve()
    #sleeve = "long"#for test
    #print sleeve, comment

    color_list_1_top = []
    color_list_2_top = []
    color_list_1_bottom = []

    color_list_2_bottom = []

    sleeved_list_1_top = []
    sleeved_list_2_top = []
    sleeved_list_1_bottom = []
    sleeved_list_2_bottom = []
    #search_top start
    search_position = "top"
    top_all_df = clothes[clothes["position"].isin([search_position])]
    top_name_list = top_all_df["file_name"].tolist()
    # top_color_list = top_all_df["color"].tolist()
    # top_sleeved_list = top_all_df["sleeved"].tolist()

    #top-color検索1
    search_color = [lucky_color, image_color]
    top_color_list = []
    for color in search_color:
        search_color_df = top_all_df[top_all_df["color"].isin([color])]
        top_color_list.append(search_color_df["file_name"].tolist())

    search_sleeved_df = top_all_df[top_all_df["sleeved"].isin([sleeve])]
    top_sleeved_list = search_sleeved_df["file_name"].tolist()
        
    # ---------------------
    search_position = ["top", "bottom"]
    #lucky_color = "red"
    #image_color = "red"
    search_color = [lucky_color, image_color]
    print search_color
    name_list = []
    name_color_list = []
    color_list = []
    sleeved_list = []
    recommend_list = [[], []]


    for pos in range(len(search_position)):
        if search_position[pos] == "top":
            all_df = clothes[clothes["position"].isin([search_position[pos]])]
            ###
        elif search_position[pos] == "bottom":
            #print all_df
            #print recommend_list[pos-1]
            remove_color1 = all_df[ (all_df.file_name== recommend_list[pos-1][0])].color.values[0]
            remove_color2 = all_df[ (all_df.file_name== recommend_list[pos-1][1])].color.values[0]
            bottom_df = clothes[clothes["position"].isin([search_position[pos]])]
            #print all_df
            all_df = bottom_df[bottom_df["color"].isin([remove_color1]) == False]
            all_df = all_df[all_df["color"].isin([remove_color2]) == False]
            #print all_df
            if len(all_df) < 5:
                all_df = bottom_df
            #print all_df
            #print remove_color1
            #print remove_color2
            ###
        name_list.append(all_df["file_name"].tolist())
        name_color_list.append(all_df["color"].tolist())

        search_color_list = []
        for color in search_color:
            search_color_df = all_df[all_df["color"].isin([color])]
            search_color_list.append(search_color_df["file_name"].tolist())
        color_list.append(search_color_list)

        search_sleeved_df = all_df[all_df["sleeved"].isin([sleeve])]
        sleeved_list.append(search_sleeved_df["file_name"].tolist())

        ### コーディネートの提案 ###
        for num in range(len(search_color)):
            #print color_list,"color_list"    
            color_sleeved = list(set(color_list[pos][num]) & set(sleeved_list[pos]))
            if len(color_sleeved) > 0:
                rec_name = color_sleeved[random.randint(0, len(color_sleeved)-1)]
                if search_color[0] == search_color[1]:
                    color_list[pos][0].pop(color_list[pos][0].index(rec_name))
                    color_list[pos][1].pop(color_list[pos][1].index(rec_name))
                else:
                    color_list[pos][num].pop(color_list[pos][num].index(rec_name))
                sleeved_list[pos].pop(sleeved_list[pos].index(rec_name))
    
            elif len(sleeved_list[pos]) > 0:
                rec_name = sleeved_list[pos][random.randint(0, len(sleeved_list[pos])-1)]
                sleeved_list[pos].pop(sleeved_list[pos].index(rec_name))
            
            elif len(color_list[pos][num]) > 0:
                rec_name = color_list[pos][num][random.randint(0, len(color_list[pos][num])-1)]
                if search_color[0] == search_color[1]:
                    color_list[pos][0].pop(color_list[pos][0].index(rec_name))
                    color_list[pos][1].pop(color_list[pos][1].index(rec_name))
                else:
                    color_list[pos][num].pop(color_list[pos][num].index(rec_name))
            
            else:
                #print sub_name_list,"subnamelist"
                rec_name = name_list[pos][random.randint(0, len(name_list[pos])-1)]
               
            #print rec_name,"rec_name"
            recommend_list[pos].append(rec_name)
            #print "pop:",rec_name
            name_list[pos].pop(name_list[pos].index(rec_name))
            #recommend_list[pos][0]
            #print name_list,"after"
                

        # 残りはランダムで決定する
        for num in range(3):
            if len(sleeved_list[pos]) > 0:
                rec_name = sleeved_list[pos][random.randint(0, len(sleeved_list[pos])-1)]
                sleeved_list[pos].pop(sleeved_list[pos].index(rec_name))
            else:
                rec_name = name_list[pos][random.randint(0, len(name_list[pos])-1)]

            recommend_list[pos].append(rec_name)
            name_list[pos].pop(name_list[pos].index(rec_name))

    #print name_list
    #print name_color_list
    #print color_list
    #print sleeved_list
    #print "###############################3"
        
    recommend_list2 = []
    for top, bottom in zip(recommend_list[0], recommend_list[1]):
        recommend_list2.append([top, bottom])
        
    #print name_list
    #print color_list
    #print sleeved_list
    #print color_sleeved
    return recommend_list2, comment, oneday_weather[0]
        


#if __name__ == "__main__":
    #switch_test();
    #reload();

