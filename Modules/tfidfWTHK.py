#!/usr/bin/env python
# -*- coding: utf-8 -*-


import MeCab
import re
import math
import sys
import codecs



def calc_tf(sentence):
    '''
    TFを計算する関数
    '''

    ### 文章を形態素解析する ###
    mecab = MeCab.Tagger("--node-format=%m\s%f[0]\\n --eos-format='' ") # MeCabのフォーマット指定

    result = mecab.parse(sentence) # MeCabによって形態素解析を行う

    # 形態素解析結果をタブ・空白・スペースなどで分割し，リストに追加する
    split = result.split()

    noun = [] # 名詞を格納するリスト
    word = split[0::2] # 単語（偶数番目）を取り出す
    part = split[1::2] # 品詞（奇数番目）を取り出す

    del word[len(word)-1] # wordの最後にある''を削除し，wordとpartの長さを揃える

    # ストップワードのリスト
    stoplist = set('てる いる なる れる する ある こと これ さん して くれる やる くださる そう せる した 思う それ ここ ちゃん くん て に を は の が と た し で ない も な い か ので よう です ます ん'.split()) # 通常の文字列でよい

    ### 名詞を取り出す ###
    for num in range(len(part)):
        searchOb_noun = re.search("名詞", part[num])
        searchOb_half = re.search('[!-~]+', word[num])
        searchOb_full = re.search("[、-◯]+", word[num])
        searchOb_full2 = re.search(u"[０-９ａ-ｚＡ-Ｚ]+", word[num].decode('utf-8'))
        searchOb_halfsymbol = re.search("[!-/:-@≠\[-`{-~]+", word[num])
        searchOb_fullsymbol = re.search(u"[、。，．・：；？！゛゜´｀¨＾￣＿ヽヾゝゞ〃仝々〆〇ー―‐／＼～∥｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋－±×÷＝≠＜＞≦≧∞∴♂♀°′″℃￥＄￠￡％＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓∈∋⊆⊇⊂⊃∪∩∧∨￢⇒⇔∀∃∠⊥⌒∂∇≡≒≪≫√∽∝∵∫∬Å‰♯♭♪†‡¶◯ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя─│┌┐┘└├┬┤┴┼━┃┏┓┛┗┣┳┫┻╋┠┯┨┷┿┝┰┥┸╂①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ�㍉㌔㌢㍍㌘㌧㌃㌶㍑㍗㌍㌦㌣㌫㍊㌻㎜㎝㎞㎎㎏㏄㎡㍻〝〟№㏍℡㊤㊥㊦㊧㊨㈱㈲㈹㍾㍽㍼≒≡∫∮∑√⊥∠∟⊿∵∩∪]+", word[num].decode('utf-8'))
        searchOb_hk = re.search(u"[ぁ-んァ-ン]{2}", word[num].decode('utf-8'))

        # ヲタフク用のマッチング
        searchOb_kana = re.search(u"[ァ-ン]+", word[num].decode('utf-8')) # カタカナのマッチング
        searchOb_mens = re.search(u"メンズ", word[num].decode('utf-8')) # 「メンズ」のマッチング

        # 特定の文字を除く
        if searchOb_half or searchOb_full2 or searchOb_halfsymbol or searchOb_fullsymbol or searchOb_mens:
            continue

        # ストップワードを除く
        if word[num] in stoplist:
            continue

        # 1文字を除く
        if len(word[num].decode('utf-8')) == 1:
            continue

        # if searchOb_noun: # 名詞の場合
        if searchOb_noun and searchOb_kana: # 名詞かつカタカナの場合
            noun.append(word[num]) # 名詞を追加する


    ### 名詞のTFを計算する ###
    tf_dic = {}
    for word in noun:
        # 初めて出現した単語は登録する必要がある
        if word not in tf_dic:
            tf_dic[word] = 0
        tf_dic[word] += 1 # TF値をカウントする


    ### 正規化TFを計算する ###
    nor_tf_dic = {}
    for key,value in tf_dic.items():
        nor_tf_dic[key] = value*1.0 / len(noun) # 各単語のTF値を正規化する（全単語数で割る）


    return nor_tf_dic



def calc_df(sentences):
    '''
    DFを計算する関数
    '''

    df_dic = {}
    mecab = MeCab.Tagger("--node-format=%m\s%f[0]\\n --eos-format='' ") # MeCabのフォーマット指定


    # 各文書ごとに各単語が登場しているかどうかを見ていく
    for sentence in sentences:
        result = mecab.parse(sentence) # 形態素解析を行う

        # 形態素解析結果をタブ・空白・スペースなどで分割し，リストに追加する
        split = result.split()

        # 文書ごとに初期化する
        noun_df = [] # 名詞を格納するリスト
        noun_df_uniq = [] # 1つの文書におけるユニークな名詞リスト（noun_dfの中から重複なしで格納していく）

        noun = [] # 名詞を管理するリスト
        word = split[0::2] # 単語（偶数番目）を取り出す
        part = split[1::2] # 品詞（奇数番目）を取り出す

        del word[len(word)-1] # wordの最後にある''を削除し，wordとpartの長さを揃える

        # ストップワードのリスト
        stoplist = set('てる いる なる れる する ある こと これ さん して くれる やる くださる そう せる した 思う それ ここ ちゃん くん て に を は の が と た し で ない も な い か ので よう です ます ん'.split()) # 通常の文字列でよい

        ### 名詞を取り出す ###
        for num in range(len(part)):
            searchOb_noun = re.search("名詞", part[num])
            searchOb_half = re.search('[!-~]+', word[num])
            searchOb_full = re.search("[、-◯]+", word[num])
            searchOb_full2 = re.search(u"[０-９ａ-ｚＡ-Ｚ]+", word[num].decode('utf-8'))
            searchOb_halfsymbol = re.search("[!-/:-@≠\[-`{-~]+", word[num])
            searchOb_fullsymbol = re.search(u"[、。，．・：；？！゛゜´｀¨＾￣＿ヽヾゝゞ〃仝々〆〇ー―‐／＼～∥｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋－±×÷＝≠＜＞≦≧∞∴♂♀°′″℃￥＄￠￡％＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓∈∋⊆⊇⊂⊃∪∩∧∨￢⇒⇔∀∃∠⊥⌒∂∇≡≒≪≫√∽∝∵∫∬Å‰♯♭♪†‡¶◯ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя─│┌┐┘└├┬┤┴┼━┃┏┓┛┗┣┳┫┻╋┠┯┨┷┿┝┰┥┸╂①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ�㍉㌔㌢㍍㌘㌧㌃㌶㍑㍗㌍㌦㌣㌫㍊㌻㎜㎝㎞㎎㎏㏄㎡㍻〝〟№㏍℡㊤㊥㊦㊧㊨㈱㈲㈹㍾㍽㍼≒≡∫∮∑√⊥∠∟⊿∵∩∪]+", word[num].decode('utf-8'))
            searchOb_hk = re.search(u"[ぁ-んァ-ン]{2}", word[num].decode('utf-8'))

            # ヲタフク用のマッチング
            searchOb_kana = re.search(u"[ァ-ン]+", word[num].decode('utf-8')) # カタカナのマッチング
            searchOb_mens = re.search(u"メンズ", word[num].decode('utf-8')) # 「メンズ」のマッチング


            # 特定の文字を除く
            if searchOb_half or searchOb_full2 or searchOb_halfsymbol or searchOb_fullsymbol or searchOb_mens:
                continue

            # ストップワードを除く
            if word[num] in stoplist:
                continue

            # 1文字を除く
            if len(word[num].decode('utf-8')) == 1:
                continue

            # if searchOb_noun: # 名詞の場合
            if searchOb_noun and searchOb_kana: # 名詞かつカタカナの場合
                noun_df.append(word[num]) # 名詞を追加する

        ### 取り出した名詞を1文書内でユニークにする ###
        for word in noun_df:
            if word not in noun_df_uniq:
                noun_df_uniq.append(word) # ユニークリストにない単語を追加する

        ### 名詞のDFを計算する ###
        for word in noun_df_uniq:
            # 初めて出現した単語は登録する必要がある
            if word not in df_dic:
                df_dic[word] = 0
            df_dic[word] += 1 # DF値をカウントする


    return df_dic



def calc_idf(sentences, df_dic):
    '''
    IDFを計算する関数
    '''

    idf_dic = {}

    # IDFの計算を行い，値を格納する
    for word in df_dic:
        idf_dic[word] = math.log(len(sentences) * 1.0 / df_dic[word] ) + 1

    return idf_dic



def calc_tfidf(sentences):
    '''
    TF-IDFを計算する関数
    '''

    df_dic = {} # DF値（単語の出現文書数）を格納するディクショナリ
    idf_dic = {} # IDF値を格納するディクショナリ
    TF_list = [] # 要素にはディクショナリが入る（各文書における各単語のTF値が格納されている）
    TFIDF_list = [] # 要素にはディクショナリが入る(各文書における各単語のTF-IDF値が格納されている)

    ### 正規化TFを計算する ###
    for num in range(len(sentences)):
        TF_list.append(calc_tf(sentences[num]))

    ### DFを計算する ###
    df_dic = calc_df(sentences)

    ### IDFを計算する ###
    idf_dic = calc_idf(sentences, df_dic)

    ### TF-IDFを計算する ###
    for num in range(len(TF_list)):
        tfidf_dic = {} # 各文書ごとに初期化する
        for word in TF_list[num]:
            tfidf_dic[word] = TF_list[num][word] * idf_dic[word] * 1.0
        TFIDF_list.append(tfidf_dic)

    return TFIDF_list



if __name__ == '__main__':
    # -----------------------------------------------------------------------
    # 日本語を含む文字列を標準入出力とやり取りする場合に書く
    # UTF-8の文字列を標準出力に出力したり，標準入力から入力したりできるようになる
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)

    # デフォルトのエンコーディングを変更する
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # -----------------------------------------------------------------------


    ### 文書群を定義する ###
    sentences = ["今日の天気は晴れです．晴れです．",
                    "今日の天気は曇りです．",
                    "明日の天気は雨です．"]

    ### TF-IDFを計算する ###
    TFIDF_list = []
    TFIDF_list = calc_tfidf(sentences)

    for k,v in TFIDF_list[0].items():
        print k,v




