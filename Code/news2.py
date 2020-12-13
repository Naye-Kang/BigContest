import pandas as pd 
from konlpy.tag import Okt
from collections import Counter
import gensim
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
from matplotlib import rc
from PIL import Image
from datetime import datetime
 
now = datetime.now()
nowDate = now.strftime('%m%d')
print(nowDate) 

################### font settings
rc('font', family='NanumBarunGothic')


################### nonelders data, elders data
list_data = [["./data/0916nonelders_data.xlsx", "nonelders"], ["./data/0916elders_data.xlsx", "elders"]]
#print(df_news)
#print(df_news.columns)


for k in range(2):
    ################### import data into dataframe
    data = pd.read_excel(list_data[k][0])
    data.rename(columns={"제목":"title"},inplace=True)
    ################### extract titles, keywords and concat 
    print(data)


    ################### tokenization and extraction of nouns into series
    okt = Okt()

    def oktTokenizer(raw, stopword=[], pos=['Noun', 'Alpha']):
        list = []
        for word, tag in okt.pos(raw, #raw data
                                     norm=True, #normalize
                                     stem=True #stemming
                                     ):
            if len(word) > 1 and tag in pos and word not in stopword: 
                if tag == 'Alpha':
                    word = word.lower()
                if word == "진자":
                    word = "확진자"
                list.append(word)        
        return list

    title_tokenized = data["title"].apply(lambda row: oktTokenizer(row))
    print(title_tokenized)
    title_tokenized.to_excel("./data/"+nowDate+list_data[k][1]+".xls") ##############


    ################### nouns series into list
    list_title_tokenized = []
    for i in range(len(title_tokenized)):
        for j in range(len(title_tokenized.values[i])):
            list_title_tokenized.append(title_tokenized.values[i][j])
    #print(list_title_tokenized)


    ################### most frequent 120 words
    ################### delete words used for extracting news
    eldersdelete = ['60대', '70대', '80대', '90대', '노년', '노인', '코로나']
    noneldersdelete = ['10대', '20대', '30대', '40대', '50대', '청년', '중장년', '중년', '코로나']
    count = Counter(list_title_tokenized)
    common120 = count.most_common(1000)
    #print(common120.index('코로나',))
    for (word, freq) in common120:
        if k==0:
            if word in noneldersdelete:
                del common120[common120.index((word, freq))]
        else:
            if word in eldersdelete:
                del common120[common120.index((word, freq))]
    #print(common120)
    #print(len(common120))
    sr_common120 = pd.Series(common120)
    sr_common120.to_excel("./data/"+nowDate+list_data[k][1]+"common120.xlsx")##########


    ################### wordlists dropped duplicates
    id2word = gensim.corpora.Dictionary(title_tokenized)

    wordlist = []
    for i in range(len(id2word)):
        #print(id2word[i])
        wordlist.append(id2word[i])
    #print(wordlist)
    seriesWordlist = pd.Series(wordlist)
    seriesWordlist.to_excel("./data/"+nowDate+list_data[k][1]+"ordlist.xls") #################

    corpus=[id2word.doc2bow(text) for text in title_tokenized]
    #print("id2word for each document : ", corpus)
    print("# words in total : ", len(id2word))
    print("# documents : ", len(corpus))


    ################### wordcloud
    cloud_mask = np.array(Image.open("cloud.png"))
    wordcloud = WordCloud(font_path = '/Library/Fonts/NanumBarunGothic.ttf',
                          mask=cloud_mask,
                          background_color='white')
    
    wordcloud_words = wordcloud.generate_from_frequencies(dict(common120[:100]))###
    print(len(dict(common120[:100])))###

    fig = plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()
    fig.savefig("./data/"+nowDate+list_data[k][1]+"_worldcloud.png") ################# 