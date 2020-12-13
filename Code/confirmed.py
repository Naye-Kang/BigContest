# 신규 확진자 그래프

import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns
import plotly.express as px
import numpy as np
from matplotlib import rc

rc('font', family='AppleGothic')

# 데이터 출처 : https://www.kaggle.com/kimjihoo/coronavirusdataset의 Time
case = pd.read_csv('./corona/Time.csv',usecols=['date','confirmed'])
case = case.sort_values(['date'])
case = case[12:133]
case = case.reset_index()
case = case.drop(['index'],axis=1)
#print(case)

dict_case=[]
for i in range(len(case)-1):
    dict_case.append(case['confirmed'][i+1]-case['confirmed'][i])
dict_case.append(1)

case['daily']=dict_case
case = case.sort_values(['date'],ascending=True)
case = case.reset_index()
case = case.drop(['index'],axis=1)
print(case)

# x축에 분기 기준이 되는 날짜만 표시되도록 하기
"""
'2020-02-01' : 분석 기간의 시작
'2020-02-23' : 개학 연기 
'2020-03-09' : 마스크 5부제
'2020-03-22' : 고강도 사회적 거리두기 시행
'2020-04-19' : 사회적 거리두기 상도 완화(5월 5일까지 연장)
'2020-05-26' : 대중교통 마스크 착용 의무화
'2020-06-01' : 분석 기간의 끝
"""
dateindex = []
#print(case[case['date']=='2020-02-23'].index.values)
dateindex.append(case[case['date']=='2020-02-23'].index.values[0])
dateindex.append(case[case['date']=='2020-03-09'].index.values[0])
dateindex.append(case[case['date']=='2020-03-22'].index.values[0])
dateindex.append(case[case['date']=='2020-04-19'].index.values[0])
dateindex.append(case[case['date']=='2020-05-26'].index.values[0])
print(dateindex)

# 그래프에 나타내기 
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(10, 8.5))
plt.title('코로나바이러스 신규 확진자 수')
plt.xlabel('날짜')
plt.ylabel('신규 확진자 수')
plt.xticks(dateindex, rotation=30)
plt.bar(case['date'], case['daily'], color='red', alpha = 0.8)
#print(case['date'].loc[dateindex].values)
for x, y in zip(case['date'].loc[dateindex].values, case['daily'].loc[dateindex].values):
    plt.annotate(y, (x,y), textcoords="offset points", xytext=(0,10), ha='center')
plt.show()
