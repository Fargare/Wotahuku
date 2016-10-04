#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
# Webから情報を取得する関数群
# ・天気予報の取得
# ・ニューストピックの取得
# ・星座占いの取得
# ・ラッキーカラーの取得
# ・今日の色彩カラーの取得
# ・天気情報（tenki.jp）の取得
# ・ファッショントレンドワードの取得
##########################################

import json
import urllib2
from bs4 import BeautifulSoup
import re
import random
import sys
import codecs

import tfidfWTHK as tfidf # TF-IDFを計算する関数群

import os.path
import time
import Image
import math

import Coloring

###### Global ######
# 色とRGBの対応をディクショナリで作成しておく
RGB_dic = {"赤": [255, 0, 0],
                "緑": [0, 128, 0],
                "青": [0, 0, 255],
                "黒": [0, 0, 0],
                "白": [255, 255, 255],
                "紫": [128, 0, 128],
                "黄": [255, 255, 0],
                "紺色": [0, 0, 128],
                "茶色": [124, 96, 53],
                "ベージュ": [172, 166, 123],
                "グレー": [128, 128, 128],
                "ピンク": [239, 143, 15],
                "黄緑": [0, 255, 255]
                }

color_to_rgb = {"red": [255, 0, 0],
                "orange":[255,183,76],
                "green": [0, 128, 0],
                "blue": [0, 0, 255],
                "black": [0, 0, 0],
                "white": [255, 255, 255],
                "purple": [128, 0, 128],
                "yellow": [255, 255, 0],
                "navy": [0, 0, 128],
                "brown": [124, 96, 53],
                "beige": [172, 166, 123],
                "gray": [128, 128, 128],
                "pink": [239, 143, 15],
                "yellowgreen": [0, 255, 255]
                }

# 色とRGBの対応をディクショナリで作成しておく
Color_Trans_dic = {"赤": "red",
                "緑": "green",
                "青": "blue",
                "黒": "black",
                "白": "white",
                "紫": "purple",
                "黄": "yellow",
                "紺色": "navy",
                "茶色": "brown",
                "ベージュ": "beige",
                "グレー": "gray",
                "ピンク": "pink",
                "黄緑": "yellowgreen"
                }

# 星座の日本語名と英語名の対応表
Constellation_Trans_dic = {"Capricorn": "山羊座",
               "Aquarius": "水瓶座",
               "Pisces": "魚座",
               "Aries": "牡羊座",
               "Taurus":"牡牛座",
                "Gemini": "双子座",
               "Cancer": "蟹座",
                "Leo": "獅子座",
               "Virgo": "乙女座",
                "Libra": "天秤座",
                "Scorpoi": "蠍座",
                "Sagittarius": "射手座"
                }

#Base Color RGB
red = [204,0,0] #0
orange = [255,183,76] #1
yellow= [255,255,0]#2
green = [40,175,12]#3
pink = [239,143,15]#4
brown = [124,96,53]#5 #
blue = [40,47,203]#6
purple = [135,0,204]#7
white = [220,220,220]#8
black = [0,0,0]#9
gray = [80,80,80]#10 #

# addition
navy = [0, 0, 128]
beige = [245, 245, 220]

colors = []
colors.append(["red",red])
colors.append(["orange",orange])
colors.append(["yellow",yellow])
colors.append(["green",green])
colors.append(["pink",pink])
colors.append(["brown",brown]) #
colors.append(["blue",blue])
colors.append(["purple",purple])
colors.append(["white",white])
colors.append(["black",black])
colors.append(["gray",gray]) #

# addition
colors.append(["navy",navy])
colors.append(["beige",beige])

def Call_Colors():
    return colors
def Call_Color_dic():
    return color_to_rgb
# -----------------------------------------------------------------------
# 日本語を含む文字列を標準入出力とやり取りする場合に書く
# UTF-8の文字列を標準出力に出力したり，標準入力から入力したりできるようになる
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

# デフォルトのエンコーディングを変更する
reload(sys)
sys.setdefaultencoding('utf-8')
# -----------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# ------ 天気予報の取得 --------
def Download(url):
    img = urllib2.urlopen(url)
    localfile = open( os.path.basename("weather_image.png"), 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()



def JudgeWeather(weather):
    '''
    晴れ，雨，曇り，雪を判定する関数
    0：晴れ
    1：雨
    2；曇り
    3：雪
    6：なし
    '''

    result_list = []
    str_list = []
    searchOb_sunny = re.search(u"晴", weather)
    searchOb_rainy = re.search(u"雨", weather)
    searchOb_cloudy = re.search(u"曇", weather)
    searchOb_snowy = re.search(u"雪", weather)

    if searchOb_sunny:
        result_list.append(0)
        str_list.append(u"晴")
    if searchOb_rainy:
        result_list.append(1)
        str_list.append(u"雨")
    if searchOb_cloudy:
        result_list.append(2)
        str_list.append(u"曇")
    if searchOb_snowy:
        result_list.append(3)
        str_list.append(u"雪")
    if len(result_list) < 2:
        result_list.append(6)
        str_list.append(u"無")

    return result_list, str_list



def JudgeMain(weather):
    '''
    天気予報の結果を判定する関数
    0：晴れ
    1：雨
    2；曇り
    3：雪
    4：時々
    5；のち
    6：なし
    '''

    judge_list = []
    result_list, str_list = JudgeWeather(weather)
    searchOb_double1 = re.search(u"時々", weather)
    searchOb_double2 = re.search(u"のち", weather)

    # 「時々」の場合
    if searchOb_double1:
        matchOb_before = re.match(str_list[0], weather)
        if matchOb_before:
            judge_list.append(result_list[0])
            judge_list.append(4)
            judge_list.append(result_list[1])
        else:
            judge_list.append(result_list[1])
            judge_list.append(4)
            judge_list.append(result_list[0])

    # 「のち」の場合
    elif searchOb_double2:
        matchOb_before = re.match(str_list[0], weather)
        if matchOb_before:
            judge_list.append(result_list[0])
            judge_list.append(5)
            judge_list.append(result_list[1])
        else:
            judge_list.append(result_list[1])
            judge_list.append(5)
            judge_list.append(result_list[0])


    else:
        judge_list.append(result_list[0])
        judge_list.append(6)
        judge_list.append(6)

    return judge_list


def Weather(code):
    '''
    天気予報を取得する関数
    input：地域コード（int型 or str型）
    output：天気（str型）
    '''

    # 天気取得のURL設定
    # cityに地域コードを設定
    city = str(code)
    # 取得URLを生成
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' % city

    try:
        # 天気データ取得
        # 最初に指定URLのデータ取得
        response = urllib2.urlopen(url)
        # jsonデータ取得
        weather = json.loads(response.read())

        # 天気のコメントを表示する
        weather_com = ""
        weather_com = weather["description"]["text"]

        # 今日と明日の天気を表示する
        weather_list = []
        for num in range(0, 2):
            day_list = []
            day_list.append(weather["forecasts"][num]["dateLabel"] + "の天気")
            day_list.append(weather["title"])
            day_list.append(weather["forecasts"][num]["telop"])
            try:
                day_list.append("最高気温：" + weather["forecasts"][num]["temperature"]["max"]["celsius"]+"℃")
            except:
                day_list.append("最高気温：--")
            try:
                day_list.append("最低気温：" + weather["forecasts"][num]["temperature"]["min"]["celsius"]+"℃")
            except:
                day_list.append("最低気温：--")
            # print "画像のURL：", weather["forecasts"][num]["image"]["url"]
            # Download(weather["forecasts"][num]["image"]["url"])
            weather_list.append(day_list)


    finally:
        response.close()

    # Converting string to number
    judge_list = []
    for num in range(0, 2):
        judge_list_pre = []
        judge_list_pre = JudgeMain(weather["forecasts"][num]["telop"])
        judge_list.append(judge_list_pre)

    # return weather['title'] + " : " + weather['forecasts'][0]['telop']
    return weather_list, weather_com, judge_list

# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# ------ ニューストピックの取得 ------

def Topics(url):
    '''
    Yahoo!ニューストップのトピックを抽出する関数
    input：Yahoo!ニュースのURL
    output：ニューストピック（list型），各ニューストピックの詳細URL（list型）
    '''

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    # HTMLのmain部分を取得する
    main_body = soup.find("div", {"id": "main"})

    # main内のul部分を取得する
    topics = main_body.find("ul", {"class": "topics"})

    # liタグを指定して検索
    # li（リストアイテム）を取得する
    out_str = ""
    topic_list = [] # ニューストピックを管理するリスト
    url_list = []   # ニューストピックの詳細のURLを管理するリスト
    for li in topics.findAll("li"):
        url_list.append(li.a.attrs['href']) # トピックの詳細URLの取得
        for content in li.a.contents:
            topic_list.append(content.string)
            break # 2番目以降は除く処理

    del topic_list[len(topic_list)-1] # 「もっと見る」を消す処理

    # for num in range(len(topic_list)):
    #     print num, "番目のトピック：", topic_list[num]
    #     print "URL：", url_list[num]

    return topic_list, url_list



def FlashTopics(url):
    '''
    Yahoo!ニュース速報のトピックを抽出する関数
    '''

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    # extract main body which tag is div
    # divタグのidがmainと一致するものを取得する
    main_body = soup.find("div", {"id": "main"})

    # extract list items in main_body which class name equals to "topics"
    # ulの中身を取得する
    topics = main_body.find("ul", {"class": "listBd"})

    # liタグを指定して検索
    # li（リストアイテム）を取得する
    out_str = ""
    topic_list = []
    for li in topics.findAll("li"):
        # aでfindAllしないと，画像があるニュースの本文を取得できない
        # 通常のfindは最初だけしか取得しないため，画像のみしか取得しない
        for a in li.findAll("a"):
            for content in a.contents:
                # 文字列であれば取得する
                if content.string is not None:
                    topic_list.append(content.string)

    return topic_list



def TopicDetail(url):
    '''
    Yahoo!ニュースのトピックの詳細を抽出する関数
    input：Yahoo!ニュースのニューストピックの詳細URL
    output：詳細に書かれた記事全文の文字列（str型）
    '''

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    # extract main body which tag is div
    # divタグのidがmainと一致するものを取得する
    main_body = soup.find("div", {"id": "main"})

    # extract list items in main_body which class name equals to "topics"
    # ニュースの本文を取得する
    text = main_body.find("h2", {"class": "newsTitle"})

    # ニュースの「記事全文」へのURLを取得する
    url_all_text = text.a.attrs['href']

    # 「全文記事」のURLのHTMLを読み取り，BeautifulSoupに読み込ませる
    soup = BeautifulSoup(urllib2.urlopen(url_all_text).read(), "lxml")

    try:
        # main部分内の記事全文部分を取得する
        all_text = soup.find("p", {"class": "ynDetailText"})

        # 記事全文を取得できなかった場合（映像がある場合）
        # 特別処理を行う
        if all_text is None:
            all_text = soup.find("div", {"class": "marB10 clearFix yjMt"})


        # 記事全文の文字列だけを抽出する
        all_text_str = ""
        for content in all_text.contents:
            if content.string is not None:
                # 文字が存在する場合のみ取得する（空白文字列を除く処理）
                searchOb = re.search(".+", str(content.string.rstrip().lstrip()))
                if searchOb:
                    all_text_str += content.string.rstrip().lstrip()
    except:
        # 上記の方法で取得できない場合はあきらめる
        all_text_str = "取得できませんでした・・・"

    return all_text_str



def Keyword(topic_list, url_list, keyword_num):
    '''
    ニューストピックのキーワードを抽出する関数
    input：ニューストピック（list型），各トピックの詳細URL（list型）
    output：キーワード（listのlist）
    '''

    # ####### URLの設定 ######
    # ### ニューストップのURL ###
    # url_main = "http://news.yahoo.co.jp/" # URLの設定（主要）
    # url_sports = "http://news.yahoo.co.jp/hl?c=c_spo" # URLの設定（スポーツ）
    # url_IT = "http://news.yahoo.co.jp/hl?c=c_sci" # URLの設定（IT・科学）

    # ### ニュースのトピックと詳細URLを取得する ###
    # topic_list, url_list = Topics(url_main)

    # URLの最後に余分なものが入っているのを確認したため，その対処をする
    if len(topic_list) != len(url_list):
        del url_list[len(url_list)-1]

    ### 各トピックの記事全文を取得する ###
    texts = []
    article = ""
    for url in url_list:
        article = TopicDetail(url)
        article = str(article)
        texts.append(article)


    ### TF-IDFを計算する ###
    TFIDF_list = []
    TFIDF_list = tfidf.calc_tfidf(texts)

    ### TF-IDF上位5単語をキーワードとして取得する ###
    keyword_list = []
    for num in range(len(TFIDF_list)):
        rank = 1
        keywords = []
        for k,v in sorted(TFIDF_list[num].items(), key=lambda x: x[1], reverse=True):
            if rank <= keyword_num:
                keywords.append(k)
                # print k,v
            rank += 1
        keyword_list.append(keywords)

    return keyword_list



def DisplayTopics(url):
    '''
    抽出したトピックを表示する関数
    input：Yahoo!ニュースのURL
    output：なし
    '''

    ###### トピックの抽出 ######
    topic_list, url_list = Topics(url)

    ###### キーワードの抽出 ######
    keyword_num = 10 # キーワード数
    keyword_list = Keyword(topic_list, url_list, keyword_num)


    ###### トピックの詳細の選択と表示 ######
    fin_flag = 0
    while fin_flag == 0:
        print "何番目のトピックの詳細を見たいですか？数字を入力してください．"
        print "終わる場合は100を入力してください．"
        input_num = raw_input('>>>  ')

        if int(input_num) == 100:
            fin_flag = 1

        elif int(input_num) > len(topic_list)-1:
            print "数字が大きいです．"

        else:
            all_text_str = TopicDetail(url_list[int(input_num)])
            print all_text_str

            # キーワードの表示
            print "--- キーワード ---"
            for word in keyword_list[int(input_num)]:
                print word



def GetTopics(url):
    '''
    必要なトピックだけを抽出する関数
    '''
    ###### トピックの抽出 ######
    topic_list, url_list = Topics(url)

    ###### キーワードの抽出 ######
    keyword_num = 10 # キーワード数
    keyword_list = Keyword(topic_list, url_list, keyword_num)

    # トピックを指定した数だけ表示する
    # get_list = []
    # rand_list = []
    # rand_count = 0
    # while rand_count < 5:
    #    rand_num = random.randint(0, 7) # 0から7まで間で乱数を発生させる
    #     if rand_num not in rand_list:
    #       # print topic_list[rand_num], keyword_list[rand_num][0], keyword_list[rand_num][1], keyword_list[rand_num][2]
    #        get_list.append(topic_list[rand_num])
    #       rand_list.append(rand_num)
    #        rand_count += 1

    return topic_list # トピックのリストだけを返す
    # return get_list

# ----------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------
# ------ 星座占いの取得 ------
def ConvertNum(zodiac):
    '''
    # 星座を文字列から数字に変更する関数
    '''

    zodiac_num = 0
    searchOb1 = re.search(u"山羊", zodiac)
    searchOb2 = re.search(u"水瓶", zodiac)
    searchOb3 = re.search(u"魚", zodiac)
    searchOb4 = re.search(u"牡羊", zodiac)
    searchOb5 = re.search(u"牡牛", zodiac)
    searchOb6 = re.search(u"双子", zodiac)
    searchOb7 = re.search(u"蟹", zodiac)
    searchOb8 = re.search(u"獅子", zodiac)
    searchOb9 = re.search(u"乙女", zodiac)
    searchOb10 = re.search(u"天秤", zodiac)
    searchOb11 = re.search(u"蠍", zodiac)
    searchOb12  =  re.search(u"射手", zodiac)

    if searchOb1:
        zodiac_num = 1
    elif searchOb2:
        zodiac_num = 2
    elif searchOb3:
        zodiac_num = 3
    elif searchOb4:
        zodiac_num = 4
    elif searchOb5:
        zodiac_num = 5
    elif searchOb6:
        zodiac_num = 6
    elif searchOb7:
        zodiac_num = 7
    elif searchOb8:
        zodiac_num = 8
    elif searchOb9:
        zodiac_num = 9
    elif searchOb10:
        zodiac_num = 10
    elif searchOb11:
        zodiac_num = 11
    else:
        zodiac_num = 12

    return zodiac_num



def FortuneTelling():
    '''
    占い結果を抽出する関数
    input：なし
    output：占い結果の星座順位（list型で順位順），占い結果のコメント（list型で順位と対応）
    '''

    ####### URLの設定 ######
    ### 占いサイトのURL ###
    url = "https://goisu.net/daily/" # URLの設定

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    # 占い結果の全体部分を取得する
    ft_result = soup.find("div", {"id": "entryBody"}, {"class": "clearfix"})

    # 星座の順位を取得する
    # 順位は<h3>タグに書かれている
    constellation_list = []
    for constellation in ft_result.findAll("h3"):
        for content in constellation.contents:
            constellation_list.append(content)


    # 占い結果のコメントを取得する
    # コメントは<p>タグに書かれている
    # しかし，"p"で探すと他のものもマッチするため，if文で対処する
    comment_list = []
    comment_str = ""
    count = 1
    flag = 0
    for comment in ft_result.findAll("p"):
        flag = 0
        for content in comment.contents:
            # 文字列だけを取得する
            if content.string is not None and count%3 ==0: # 関係ない文字列はスキップ
                count += 1
            elif content.string is not None and flag == 0: # 最初は文字列を連結させるだけ
                comment_str += str(content.string) # 文字列の連結
                count += 1
                flag = 1
            elif content.string is not None and flag == 1: # すべてのコメントを取得したら，リストに追加する
                # comment_str += str(content.string) # 文字列の連結
                comment_list.append(comment_str) # 文字列の追加
                comment_str = "" # 文字列の初期化
                count += 1

    # for num in range(len(constellation_list)):
    #     print constellation_list[num]
    #     # print "### 一言コメント ###"
    #     print comment_list[num]

    # 星座を数字に変換する
    num_list = []
    for num in range(len(constellation_list)):
        num_list.append(ConvertNum(constellation_list[num]))

    # ###### 星座のままの場合 ######
    # constellation_list2 = constellation_list[0:3]
    # constellation_list2.append(constellation_list[len(constellation_list)-1])

    # comment_list2 = comment_list[0:3]
    # comment_list2.append(comment_list[len(comment_list)-1])

    # # return constellation_list, comment_list
    # return constellation_list2, comment_list2
    # #############################

    ###### 数字に変換した場合 ######
    #num_list2 = num_list[0:3]
    #num_list2.append(num_list[len(num_list)-1])

    #comment_list2 = comment_list[0:3]
    #comment_list2.append(comment_list[len(comment_list)-1])

    # return constellation_list, comment_list
    #return num_list2, comment_list2
    #############################

    return constellation_list, num_list, comment_list # All give


# --------------------------------------------------------------------------------




# --------------------------------------------------------------------------------
def LuckyColor():
    '''
    ラッキーカラーを抽出する関数
    input：なし
    output：ディクショナリ（{"星座": "色"}）
    '''

    ####### URLの設定 ######
    ### 占いサイトのURL ###
    url = "http://www.sanspo.com/today/uranai.html" # URLの設定

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")


    # 占い結果の全体部分を取得する
    ft_result = soup.find("div", {"id": "Contents"})

    # 占い結果の詳細を取得する
    details = ft_result.findAll("table", {"class": "UranaiTable01"})

    color_dic = {}
    for detail in details:
        # print str(detail.img.attrs['alt']) # 星座
        # print str(detail.findAll("tr")[1].findAll("td")[1].string) # ラッキーカラー

        color_dic[str(detail.img.attrs['alt'])] = str(detail.findAll("tr")[1].findAll("td")[1].string)

    return color_dic


def TenjinLuckyColor():
    '''
    ラッキーカラーを抽出する関数
    input：なし
    output：ディクショナリ（{"星座": "色"}）
    '''

    ####### URLの設定 ######
    ### 占いサイトのURL ###
    url = "https://tenjinsite.jp/uranai/" # URLの設定

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    main_body = soup.find("div", {"class": "sp-mr30 sp-ml30"})

    horoscope_rank = main_body.findAll("div", {"class": "horoscope_num"})   # 順位部分を抽出する
    horoscope_kind = main_body.findAll("div", {"class": "horoscope_image"}) # 星座名部分を抽出する
    horoscope_info = main_body.findAll("div", {"class": "horoscope_info"})  # 占い結果の詳細部分を抽出する

    color_dic = {}
    for num in range(len(horoscope_rank)):
        # print horoscope_rank[num].img.attrs["alt"]
        # print horoscope_kind[num].img.attrs["alt"]
        # print horoscope_info[num].find("p", {"class": "pc-mb5"}).string

        # 星座名とラッキーカラーのディクショナリを作成する
        color_dic[str(horoscope_kind[num].img.attrs["alt"])] = str(horoscope_info[num].find("p", {"class": "pc-mb5"}).string).replace(u"ラッキーカラー：", "")

    return color_dic
# --------------------------------------------------------------------------------




# --------------------------------------------------------------------------------
# ------ 今日の色彩イメージの抽出 ------
def ColorImage(url):
    """
    今日の色彩イメージを抽出する関数
    """
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
    main_body = soup.find("div", {"style": "text-align:left; padding: 18px 0 12px 0px; margin:0 0 20px 0; border-top: 1px dotted #333333;"})

    # 画像のURLを取得する
    color_img = str(main_body.find("img").attrs["src"])
    color_img = color_img.replace("..", "http://iro-color.com")

    # 色画像をダウンロードし，保存する
    img = urllib2.urlopen(color_img)
    # localfile = open(os.path.basename(url) + ".gif", 'wb')
    localfile = open("color_image.gif", 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

    # gif形式をjpg形式に変換する
    img_gif = Image.open("color_image.gif")
    img_gif = img_gif.convert("RGB")
    img_gif.save("color_image.jpg", "jpeg")

    # 中央の画素からRGBを取得する
    img_jpg = Image.open("color_image.jpg")
    pixelSizeTuple = img_jpg.size
    rgb = ()
    rgb = img_jpg.getpixel((pixelSizeTuple[0]*1.0/2, pixelSizeTuple[1]*1.0/2))
    # color = str(main_body.text.lstrip().rstrip())

    return rgb





# ---------------------------------------------------------------------------------
# ---------- 天気に関する指数の抽出 --------------
def GetTenkiURL(url, mode):
    """
    URLを抽出する関数
    """

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    if mode == "prefecture":
        main_body = soup.find("div", {"id": "wrap_weathersVarious"})
        urls = main_body.findAll("a")

    elif mode == "area":
        main_body = soup.find("div", {"id": "forecast_point_entries"})
        urls = main_body.findAll("a")

    # 県名or地域名とURLのディクショナリを作成する
    prefecture_dic = {}
    for url in urls:
        prefecture_str = str(url.string)
        if prefecture_str != str(None):
            url_str = "http://www.tenki.jp" + str(url.attrs["href"])
            prefecture_dic[prefecture_str] = url_str
            # print prefecture_str, url_str # 確認のための出力

    return prefecture_dic


def GetTenkiAreaURL(url):
    """
    指定した地域の指数が書かれているURLを取得する関数
    """

    # 県名とURLのディクショナリを作成する
    prefecture_dic = GetTenkiURL(url, "prefecture")

    # 県名の入力と決定
    # input_str = raw_input(">> ")
    # prefecture_url = "" # 入力した県のURL
    # if input_str in prefecture_dic:
    #     prefecture_url = prefecture_dic[input_str]

    # 県名と「岐阜県」に固定する場合
    prefecture_url = prefecture_dic["岐阜県"]

    # 地域名とURLのディクショナリを作成する
    area_dic = GetTenkiURL(prefecture_url, "area")


    # 地域名の入力と決定
    # input_str = raw_input(">> ")
    # area_url = "" # 入力した地域のURL
    # if input_str in area_dic:
    #     area_url = area_dic[input_str]
    #     print area_url

    # 地域名を「美濃地方(岐阜)」に固定する場合
    area_url = area_dic["岐阜市"]

    return area_url


def GetOneDayTenki(soup):
    """
    一日の天気を抽出する関数
    """

    # 「今日明日の天気」のURLを取得する
    main_body = soup.find("ul", {"class": "forecast_select_btn clearfix"})
    oneday_url = "http://www.tenki.jp" + str(main_body.find("li", {"class": "forecast_select_daily"}).a.attrs["href"])

    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(oneday_url).read(), "lxml")

    today_body = soup.find("div", {"id": "townLeftOneBox"})
    tomorrow_body = soup.find("div", {"id": "townRightOneBox"})

    oneday_weather = []
    oneday_weather.append(str(today_body.p.string))
    oneday_weather.append(str(tomorrow_body.p.string))

    return oneday_weather


def GetTenki(url):
    """
    天気情報を抽出する関数
    """

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    main_body = soup.find("div", {"id": "bd-main"})

    # 天気を抽出する
    weather_info = []
    dummy = "" # try＆exceptのためのダミー

    day = main_body.findAll("tr", {"class": "head"})         # 日付
    weather = main_body.findAll("tr", {"class": "weather"})  # 天気
    temp = main_body.findAll("tr", {"class": "temperature"}) # 気温
    humi = main_body.findAll("tr", {"class": "humidity"})    # 湿度
    windb = main_body.findAll("tr", {"class": "windBlow"})   # 風向き
    winds = main_body.findAll("tr", {"class": "windSpeed"})  # 風速

    for num in range(0, 3):

        weather_dic = {}

        # 日付を抽出する
        # weather = main_body.find("tr", {"class": "weather"})
        day_detail = day[num].find("p")
        weather_dic["日付"] = str(day_detail.text)
        # weather_info[num].append(str(day_detail.text))

        # 天気を抽出する
        # weather = main_body.find("tr", {"class": "weather"})
        weather_detail = weather[num].findAll("td")
        for detail in weather_detail:
            try:
                dummy = detail.p.attrs["class"]
            except:
                weather_dic["天気"] = str(detail.p.string)
                break

        # 気温を抽出する
        # temp = main_body.find("tr", {"class": "temperature"})
        temp_detail = temp[num].findAll("td")
        for detail in temp_detail:
            try:
                dummy = detail.span.attrs["class"]
            except:
                weather_dic["気温"] = str(detail.span.string)
                break

        # 湿度を抽出する
        # humi = main_body.find("tr", {"class": "humidity"})
        humi_detail = humi[num].findAll("td")
        for detail in humi_detail:
            try:
                dummy = detail.span.attrs["class"]
            except:
                weather_dic["湿度"] = str(detail.span.string)
                break


        # 風向きを抽出する
        # windb = main_body.find("tr", {"class": "windBlow"})
        windb_detail = windb[num].findAll("p")
        for detail in windb_detail:
            try:
                dummy = detail.attrs["class"]
            except:
                weather_dic["風向き"] = str(detail.string)
                break

        # 風速を抽出する
        # winds = main_body.find("tr", {"class": "windSpeed"})
        winds_detail = winds[num].findAll("td")
        for detail in winds_detail:
            try:
                dummy = detail.span.attrs["class"]
            except:
                weather_dic["風速"] = str(detail.span.string)
                break
        weather_info.append(weather_dic)

    oneday_weather = GetOneDayTenki(soup)

    return weather_info, oneday_weather



def Tenki(url):
    """
    天気に関する指数を抽出する関数
    """

    # 指定した地域のURLを取得する
    area_url = GetTenkiAreaURL(url)

    # 今日と明日の指数を抽出する
    weather_info, oneday_weather = GetTenki(area_url)

    return weather_info, oneday_weather
# ----------------------------------------------------------------




# ---------------------------------------------------------------------------------
# ---------- 天気に関する指数の抽出 --------------
def GetURL(url):
    """
    URLを抽出する関数
    """

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    main_body = soup.find("div", {"id": "wrap_weathersVarious"})
    urls = main_body.findAll("li")

    # 県名とURLのディクショナリを作成する
    prefecture_dic = {}
    for url in urls:
        prefecture_str = str(url.string)
        url_str = "http://www.tenki.jp" + str(url.a.attrs["href"])
        prefecture_dic[prefecture_str] = url_str
        # print prefecture_str, url_str # 確認のための出力

    return prefecture_dic


def GetAreaURL(url):
    """
    指定した地域の指数が書かれているURLを取得する関数
    """

    # 県名とURLのディクショナリを作成する
    prefecture_dic = GetURL(url)

    # 県名の入力と決定
    # input_str = raw_input(">> ")
    # prefecture_url = "" # 入力した県のURL
    # if input_str in prefecture_dic:
    #     prefecture_url = prefecture_dic[input_str]

    # 県名と「岐阜県」に固定する場合
    prefecture_url = prefecture_dic["岐阜県"]

    # 地域名とURLのディクショナリを作成する
    area_dic = GetURL(prefecture_url)


    # 地域名の入力と決定
    # input_str = raw_input(">> ")
    # area_url = "" # 入力した地域のURL
    # if input_str in area_dic:
    #     area_url = area_dic[input_str]
    #     print area_url

    # 地域名を「美濃地方(岐阜)」に固定する場合
    area_url = area_dic["美濃地方(岐阜)"]

    return area_url



def GetIndex(url):
    """
    指数を抽出する関数
    """

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    main_body = soup.find("div", {"id": "exponentLarge"})
    today = main_body.find("dl", {"id": "exponentLargeLeft"})     # 今日の服装指数が書かれた部分を取得する
    tomorrow = main_body.find("dl", {"id": "exponentLargeRight"}) # 明日の服装指数が書かれた部分を取得する

    # 今日の服装指数を取得する
    today_str = ""
    # today_str = str(today.find("strong").string) + "：" + str(today.img.attrs["alt"])
    today_str = str(today.img.attrs["alt"])
    # print today_str

    # 明日の服装指数を取得する
    tomorrow_str = ""
    # tomorrow_str = str(tomorrow.find("strong").string) + "：" + str(tomorrow.img.attrs["alt"])
    tomorrow_str = str(tomorrow.img.attrs["alt"])
    # print tomorrow_str

    return today_str, tomorrow_str



def Index(url):
    """
    天気に関する指数を抽出する関数
    """

    # 指定した地域のURLを取得する
    area_url = GetAreaURL(url)

    # 今日と明日の指数を抽出する
    today_str, tomorrow_str = GetIndex(area_url)

    return today_str, tomorrow_str
# --------------------------------------------------------------------






# -------------------------------------------------------------------
# ------ トレンドワードの抽出 ------
# def CalcTrendWords(item_name):
#     """
#     トレンドワードを算出する関数
#     """

#     # TF-IDFの計算
#     TFIDF_list = tfidf.calc_tfidf(name_list)

#     trend_word = {}
#     rank = 1
#     for num in range(len(TFIDF_list)):
#         rank = 0
#         for k,v in sorted(TFIDF_list[num].items(), key=lambda x: x[1], reverse=True):
#             # print k,v
#             if k not in trend_word:
#                 trend_word[k] = 0
#             trend_word[k] += 1

#             # 上位3つまでの登場をカウントする
#             if rank == 3:
#                 break
#             else:
#                 rank += 1

#     return trend_word



def CalcTrendWords(item_name):
    """
    トレンドワードを算出する関数
    """

    # TF-IDFの計算
    TFIDF_list = tfidf.calc_tfidf(name_list)

    trend_word = {}
    for num in range(len(TFIDF_list)):
        for k,v in sorted(TFIDF_list[num].items(), key=lambda x: x[1], reverse=True):
            # print k,v
            if k not in trend_word:
                trend_word[k] = 0
            trend_word[k] += v # TF-IDF値そのものを加算する

    return trend_word



def TrendRakuten(url):
    """
    楽天市場から
    ファッションのトレンドワードを抽出する関数
    """

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    item_name = soup.findAll("div", {"class": "rnkRanking_itemName"})

    name_list = []
    for name in item_name:
        name_list.append(str(name.a.string))

    return name_list



def TrendYahoo(url, mode):
    """
    Yahoo!ショッピングから
    ファッションのトレンドワードを抽出する関数
    """

    # 設定したURLのHTMLを読み取る
    # 読み取ったHTMLをBeautifulSoupに読み込ませる
    # HTMLパーサ：lxml
    time.sleep(0.5)
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")

    # main_body = soup.find("div", {"class": "mdRankList"})

    if mode == "popular":
        item_name = soup.findAll("h4", {"class": "elTitle"})

    elif mode == "hot":
        item_name = soup.findAll("a")

    name_list = []
    name_str = ""
    for name in range(len(item_name)):
        if name < 0:
            name_str = str(item_name[name].a.string) + str(item_name[name].a.string) + str(item_name[name].a.string)
        else:
            name_str = str(item_name[name].a.string)
        name_list.append(name_str)

    return name_list
# -------------------------------------------------------------------




# -------------------------------------------------------------------
# ------ 色決定アルゴリズム ------
def ChangeColorName(color_name):
    """
    色の名前を変更する関数
    （簡単な色の名前に変更する）
    """

    if color_name == "クリーム色" or color_name == "カーキ色" or color_name == "アイボリー":
        color_name = "ベージュ"
    elif color_name == "ゴールド":
        color_name = "黄"
    elif color_name == "深緑" or color_name == "黄緑":
        color_name = "緑"
    elif color_name == "シルバー":
        color_name = "グレー"
    elif color_name == "オリーブ色":
        color_name = "緑"
    else:
        pass

    return color_name



def ChangeColorRGB(color_name):
    """
    色を文字列からRGBの値に変更する関数
    """

    # 色とRGBの対応をディクショナリで作成しておく
    RGB_dic = {"赤": [255, 0, 0],
                "緑": [0, 128, 0],
                "青": [0, 0, 255],
                "黒": [0, 0, 0],
                "白": [255, 255, 255],
                "紫": [128, 0, 128],
                "黄": [255, 255, 0],
                "紺色": [0, 0, 128],
                "茶色": [124, 96, 53],
                "ベージュ": [172, 166, 123],
                "グレー": [128, 128, 128],
                "ピンク": [239, 143, 15]
                }

    rgb = []
    try:
        rgb = RGB_dic[color_name]
    except:
        # ディクショナリにない色の名前であった場合
        rgb = [0, 0, 0]

    return rgb




# -----------------------------------------------------------
# keywordの画像リンクを探索
def url_search(keyword, n):

    img_url=[]
    url = "http://ajax.googleapis.com/ajax/services/search/images?q={0}&amp;v=1.0&amp;rsz=large&amp;start={1}"
    # keywordと一致する画像URLをn個取得
    for i in range((n/8)+1):
        res = urllib2.urlopen(url.format(keyword, i*8))
        data = json.load(res)
        img_url += [result["url"] for result in data["responseData"]["results"]]

    return img_url


# URL先の画像ファイルを保存
def url_download(keyword,urls):
    print("Download Start...")
    # keywordのフォルダが無ければ作成
    if os.path.exists(keyword)==False:
        os.mkdir(keyword)

    opener = urllib2.build_opener()
    # URLの数だけ画像DL
    for i in range(len(set(urls))):
        try:
            fn, ext = os.path.splitext(urls[i])
            req = urllib2.Request(urls[i], headers={"User-Agent" : "Magic Browser"})
            img_file = open(keyword+"\\"+str(i)+ext, "wb")  # 画像データの保存
            img_file.write(opener.open(req).read())
            img_file.close()
            print("DL Image Link:"+str(i+1))
        except:
            continue


def GetColorImage():
    """
    画像検索で色画像を取得する関数
    """
    keyword = "カーキ"         # 検索キーワード
    urls = url_search(keyword, n=1) # 画像URLの探索
    url_download(keyword,urls)          # 画像のダウンロード
    print("End...")


def main():
    ###### 天気情報の抽出 ######
    # weather_list, weather_com, judge_list = Weather(210010)

    ###### 天気情報の出力確認 ######
    # # 天気の概要
    # for day in range(len(weather_list)):
    #     for num in range(len(weather_list[day])):
    #         if num == 2:
    #             print weather_list[day][num]
    #         if num == 3 or num == 4:
    #             # print  weather_list[day][num]
    #             searchOb_temp = re.search("\d+", weather_list[day][num])
    #             # 気温の値だけを取得する
    #             if searchOb_temp:
    #                 print int(searchOb_temp.group())
    #             else:
    #                 print "unknown"

    # # 天気のコメント
    # print weather_com

    # 天気を数値化したもの
    # for i in judge_list:
    #     print i
    # sys.exit()


    ###### ラッキーカラーの抽出 ######
    ### 1つ目のサイト ###
    # lucky_color_dic = LuckyColor()
    # for k,v in lucky_color_dic.items():
    #     print k,v

    ### 2つ目のサイト ###
    lucky_color_dic2 = TenjinLuckyColor()
    # for k,v in lucky_color_dic2.items():
    #     print k,v
    # sys.exit()


    ###### 今日の色彩イメージの抽出 ######
    color_image = ColorImage("http://iro-color.com/sample/366color.php")
    color_img = []
    for i in color_image:
        color_img.append(i)
    # print color_img


    ###### 天気情報の抽出 ######
    weather_info, oneday_weather = Tenki("http://www.tenki.jp/")
    # for day in range(len(weather_info)):
    #     for k,v in weather_info[day].items():
    #         print k, v
    # sys.exit()


    ###### 今日と明日の服装指数の抽出 ######
    today_cloth, tomorrow_cloth = Index("http://www.tenki.jp/indexes/dress/")
    # print today_cloth
    # print tomorrow_cloth


    ###### 今日と明日の紫外線指数の抽出 ######
    today_uv, tomorrow_uv = Index("http://www.tenki.jp/indexes/uv_index_ranking/")
    # print today_uv
    # print tomorrow_uv


    ###### 楽天市場からのトレンドワードの抽出 ######
    # name_list = TrendRakuten("http://ranking.rakuten.co.jp/realtime/551177/")
    # trend_word = CalcTrendWords(name_list) # トレンドワードの算出
    # for k,v in sorted(trend_word.items(), key=lambda x: x[1], reverse=True):
    #     print k,v


    ###### Yahoo!ショッピングからのトレンドワードの抽出（全体） ######
    # ### 売れ筋商品ランキング ###
    # # # 1位〜20位までのアイテム
    # name_list = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/ranking/gender_male/generation_20/?sc_i=shp_pc_ranking-cate_mdRankListSort_generation-20#list", "popular")

    # # # 21位〜40位までのアイテム
    # # name_list21_40 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/ranking/gender_male/generation_20/cr_20/?sc_i=shp_pc_ranking-cate_mdRankListPager_21-40#list", "popular")
    # # for name in name_list21_40: # アイテムの追加
    # #     name_list.append(name)

    # # # 41位〜60位までのアイテム
    # # name_list41_60 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/ranking/gender_male/generation_20/cr_40/?sc_i=shp_pc_ranking-cate_mdRankListPager_41-60#list", "popular")
    # # for name in name_list41_60: # アイテムの追加
    # #     name_list.append(name)

    # trend_word = CalcTrendWords(name_list) # トレンドワードの算出
    # for k,v in sorted(trend_word.items(), key=lambda x: x[1], reverse=True):
    #     print k,v

    # ### 急上昇ランキング ###
    # 1位〜20位までのアイテム
    # name_list = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/ranking/burst/gender_male/generation_20/?sc_i=shp_pc_ranking-burst_mdRankListSort_generation-20#list", "hot")

    # CalcTrendWords(name_list) # トレンドワードの算出


    ###### Yahoo!ショッピングからのトレンドワードの抽出（トップス） ######
    # ### 売れ筋商品ランキング ###
    # # # 1位〜20位までのアイテム
    # name_list = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36504/ranking/gender_male/generation_20/?sc_i=shp_pc_ranking-cate_mdRankListSort_generation-20#list", "popular")

    # # 21位〜40位までのアイテム
    # name_list21_40 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36504/ranking/gender_male/generation_20/cr_20/?sc_i=shp_pc_ranking-cate_mdRankListPager_21-40#list", "popular")
    # for name in name_list21_40: # アイテムの追加
    #     name_list.append(name)

    # # 41位〜60位までのアイテム
    # name_list41_60 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36504/ranking/gender_male/generation_20/cr_40/?sc_i=shp_pc_ranking-cate_mdRankListPager_41-60#list", "popular")
    # for name in name_list41_60: # アイテムの追加
    #     name_list.append(name)

    # # 61位〜80位までのアイテム
    # name_list61_80 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36504/ranking/gender_male/generation_20/cr_60/?sc_i=shp_pc_ranking-cate_mdRankListPager_61-80#list", "popular")
    # for name in name_list61_80: # アイテムの追加
    #     name_list.append(name)

    # # 81位〜100位までのアイテム
    # name_list81_100 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36504/ranking/gender_male/generation_20/cr_80/?sc_i=shp_pc_ranking-cate_mdRankListPager_81-100#list", "popular")
    # for name in name_list81_100: # アイテムの追加
    #     name_list.append(name)

    # trend_word = CalcTrendWords(name_list) # トレンドワードの算出
    # for k,v in sorted(trend_word.items(), key=lambda x: x[1], reverse=True):
    #     print k,v



    ###### Yahoo!ショッピングからのトレンドワードの抽出（ボトムス，パンツ） ######
    # ### 売れ筋商品ランキング ###
    # # # 1位〜20位までのアイテム
    # name_list = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36624/ranking/gender_male/generation_20/?sc_i=shp_pc_ranking-cate_mdSideListCategory_02", "popular")

    # # 21位〜40位までのアイテム
    # name_list21_40 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36624/ranking/gender_male/generation_20/cr_20/?sc_i=shp_pc_ranking-cate_mdRankListPager_21-40#list", "popular")
    # for name in name_list21_40: # アイテムの追加
    #     name_list.append(name)

    # # 41位〜60位までのアイテム
    # name_list41_60 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36624/ranking/gender_male/generation_20/cr_40/?sc_i=shp_pc_ranking-cate_mdRankListPager_41-60#list", "popular")
    # for name in name_list41_60: # アイテムの追加
    #     name_list.append(name)

    # # 61位〜70位までのアイテム
    # name_list61_70 = TrendYahoo("http://shopping.yahoo.co.jp/category/13457/2495/36624/ranking/gender_male/generation_20/cr_60/?sc_i=shp_pc_ranking-cate_mdRankListPager_61-80#list", "popular")
    # for name in name_list61_70: # アイテムの追加
    #     name_list.append(name)

    # trend_word = CalcTrendWords(name_list) # トレンドワードの算出
    # for k,v in sorted(trend_word.items(), key=lambda x: x[1], reverse=True):
    #     print k,v



    ###### 色の決定 ######
    final_color = [0, 0, 0] # 最終的な色

    # 簡単な色の名前に変更する
    for k,v in lucky_color_dic2.items():
        lucky_color_dic2[k] = ChangeColorName(v)

    # ラッキーカラーを文字列からRGBに変更する
    lucky_color = ChangeColorRGB("赤")
    print lucky_color

    # ラッキーカラーと今日の色彩カラーを平均する
    final_color = [(x + y)*1.0/2 for (x, y) in zip(lucky_color, color_img)]
    print final_color

    # 天気を判断する
    searchOb_sunny = re.search(u"晴", weather_info[0]["天気"].decode("utf-8"))
    searchOb_rainy = re.search(u"雨", weather_info[0]["天気"].decode("utf-8"))
    searchOb_cloudy = re.search(u"曇", weather_info[0]["天気"].decode("utf-8"))

    # 天気によって色に補正をかける
    if searchOb_sunny:
        weather_color = [128, 0, 0]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, weather_color)]
    elif searchOb_rainy:
        weather_color = [0, 0, 128]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, weather_color)]
    elif searchOb_cloudy:
        weather_color = [128, 128, 128]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, weather_color)]
    else:
        pass
    print final_color


    # 気温によって色に補正をかける
    if float(weather_info[0]["気温"]) > 25:
        temp_color = [0, 0, 255]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, temp_color)]
    elif float(weather_info[0]["気温"]) < 15:
        temp_color = [255, 0, 0]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, temp_color)]
    else:
        pass
    print final_color


    # 紫外線を判断する
    searchOb_uv1 = re.search(u"弱い", today_uv.decode("utf-8"))
    searchOb_uv2 = re.search(u"やや強い", today_uv.decode("utf-8"))
    searchOb_uv3 = re.search(u"強い", today_uv.decode("utf-8"))
    searchOb_uv4 = re.search(u"非常に強い", today_uv.decode("utf-8"))
    searchOb_uv5 = re.search(u"きわめて強い", today_uv.decode("utf-8"))

    # 紫外線によって色に補正をかける
    if searchOb_uv1:
        # uv_color = [255*1.0/5, 255*1.0/5, 0]
        # final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, uv_color)]
        pass
    if searchOb_uv2:
        uv_color = [255*1.0/4, 255*1.0/4, 0]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, uv_color)]
    if searchOb_uv3:
        uv_color = [255*1.0/3, 255*1.0/3, 0]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, uv_color)]
    if searchOb_uv4:
        uv_color = [255*1.0/2, 255*1.0/2, 0]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, uv_color)]
    if searchOb_uv5:
        uv_color = [255, 255, 0]
        final_color = [(x + y)*1.0/2 for (x, y) in zip(final_color, uv_color)]
    else:
        pass
    print final_color

    result = Coloring.judge_colors(final_color)
    print result

    ### ユークリッド距離の算出 ###
    dist = 0
    for num in range(len(final_color)):
        dist += final_color[num]**2
    dist = math.sqrt(dist)
    print dist
    print today_cloth


def RecommendColor():
    # %%%%%%%% 色の決定 %%%%%%%%
    ###### ラッキーカラーの抽出 ######
    ### 1つ目のサイト ###
    # lucky_color_dic = LuckyColor()
    # for k,v in lucky_color_dic.items():
    #     print k,v

    ### 2つ目のサイト ###
    lucky_color_dic2 = TenjinLuckyColor()
    for k,v in lucky_color_dic2.items():
        lucky_color_dic2[k] = ChangeColorName(v)
    f = open("/media/usb/Clothings/profile.txt", "r")
    constellation = f.readline().rstrip()
    f.close()
    lucky_color = Color_Trans_dic[str(lucky_color_dic2[Constellation_Trans_dic[constellation]])]
    #print lucky_color


    ###### 今日の色彩イメージの抽出 ######
    image_color = ColorImage("http://iro-color.com/sample/366color.php")
    color_img = []
    for i in image_color:
        color_img.append(i)
    image_color = Coloring.judge_colors(color_img)
    #print image_color

    ###### 今日と明日の紫外線指数の抽出 ######
    today_uv, tomorrow_uv = Index("http://www.tenki.jp/indexes/uv_index_ranking/")

    # 紫外線を判断する
    searchOb_uv1 = re.search(u"弱い", today_uv.decode("utf-8"))
    searchOb_uv2 = re.search(u"やや強い", today_uv.decode("utf-8"))
    searchOb_uv3 = re.search(u"強い", today_uv.decode("utf-8"))
    searchOb_uv4 = re.search(u"非常に強い", today_uv.decode("utf-8"))
    searchOb_uv5 = re.search(u"きわめて強い", today_uv.decode("utf-8"))

    # 紫外線によって色に補正をかける
    if searchOb_uv4:
        lucky_color = "black"
    elif searchOb_uv5:
        lucky_color = "yellow"
    else:
        pass

    return lucky_color, image_color

    

def RecommendSleeve():
    # %%%%%%%% 半袖・長袖の決定 %%%%%%%%
    ###### 天気情報の抽出 ######
    weather_info, oneday_weather = Tenki("http://www.tenki.jp/")
    # for day in range(len(weather_info)):
    #     for k,v in weather_info[day].items():
    #         print k, v


    ###### 今日と明日の服装指数の抽出 ######
    today_cloth, tomorrow_cloth = Index("http://www.tenki.jp/indexes/dress/")
    # print today_cloth
    # print tomorrow_cloth

    # 気温によって半袖・長袖を決定する
    sleeve = ""
    #wind_temp = float(weather_info[0]["風速"])
    #print float(weather_info[0]["気温"])-wind_temp
    #if (float(weather_info[0]["気温"]-weather_info[0]["風速"])) >= 22:
    #if (float(weather_info[0]["気温"])- wind_temp) >= 22:
    if (float(weather_info[0]["気温"])-float(weather_info[0]["風速"])) >= 22:
        sleeve = "short"
    else:
        sleeve = "long"

    searchOb_val = re.search("\d{2}", today_cloth)
    cloth_index = searchOb_val.group()
    comment = today_cloth.replace("指数:"+cloth_index+":", "")
    return weather_info, oneday_weather, sleeve, comment
    

    
if __name__ == '__main__':

    lucky_color, image_color = RecommendColor()
    print lucky_color, image_color

    sleeve, comment = RecommendSleeve()
    print sleeve
    
    
    
    




