#!/usr/bin/env python
# coding: utf-8

# In[54]:


# Handling  22years old
import pandas as pd 
import numpy as np
import math
from collections import Counter
from re import match 

# Visualize
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import matplotlib.cm as cm
from wordcloud import WordCloud

# TextMining
import konlpy.tag
from konlpy.tag import *


# In[27]:


# 나눔고딕 폰트 설정
# 멜건 폰트 설정
font_path = r"C:\Users\pc021\Desktop\싸인랩\업무\말뭉치\형태소분석_최종v1.1\프로그램소스\morpheme\fonts\malgun.ttf"  # 경로는 시스템에 맞게 조정하세요
font_prop = fm.FontProperties(fname=font_path)

plt.rc('font', family=font_prop.get_name())
plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지


# In[63]:


# Action: 데이터 로드

data = pd.read_csv(r"C:\Users\pc021\Desktop\성장\웹 개발\kakaotalk\데이터\버거 앤 파스타.csv")
stopwords = pd.read_csv(r"C:\Users\pc021\Desktop\성장\웹 개발\kakaotalk\스탑워드\stopword_final_app.csv", encoding='cp949', index_col=0)

stopwords.columns = ['Word']


# In[3]:


def plot_bar(conversation_length_dict):
    fig = plt.figure(figsize=(8,6))
    with plt.style.context('fivethirtyeight'):
        plt.bar(conversation_length_dict.keys(),conversation_length_dict.values())
        plt.ylabel("대화 길이 평균",fontsize=12)
        plt.xlabel("이름",fontsize=12)
    plt.show()


# In[4]:


def analyze_short_answer_messages(data):
    """ 단단형 메시지 인원분석
    """

    # 단톡방 이름 생성
    names = data['Name'].unique()
    conversation_length_dict = {}
    
    for name in names:
        conversation_length_list = []
        specific_data = data[data['Name']==name]['Processing_Sentence']
        
        for sentence in specific_data:
            conversation_length_list.append(len(sentence))  
        
        conversation_length_dict[name] = np.round(np.mean(conversation_length_list),2)
    # 값을 기준을 순서 정렬
    conversation_length_dict = dict(sorted(conversation_length_dict.items(), key=lambda item: item[1], reverse=True))

    plot_bar(conversation_length_dict)


# In[5]:


def monthly_conversations_plot(data):
    # 피규어 설정
    fig = plt.figure()

    # 대화 횟수를 기준으로 데이터프레임 정렬
    sorted_indices = list(data['Month'].value_counts().sort_values().index.values)

    with plt.style.context('fivethirtyeight'):
        # 데이터 시각화
        fig = data['Month'].value_counts().sort_values().plot(kind='bar')

        # 라벨 설정
        plt.xlabel("월",fontsize=12,labelpad=15)
        plt.ylabel("대화 횟수",fontsize=12)

        # xticks 설정
        months = [f'{month}월' for month in sorted_indices]
        
        plt.xticks(list(range(len(data['Month'].unique()))),months)

        #print(list(data['Month'].unique()))
        #print(months)
        
    return fig


# In[74]:


# Action: 시간별 대화 횟수 분석

def analyze_conversations_by_time(data):

    # 데이트 컬럼을 시간 형식으로 변환
    #data['Date'] = pd.to_datetime(data['Date'], format='%H:%M').dt.time

    # 데이트 컬럼을 시간대별로 그룹화하여 빈도수 계산
    data['Hour'] = pd.to_datetime(data['Date'], format='%H:%M').dt.hour
    hourly_counts = data['Hour'].value_counts().sort_index()

    # 시간대별 빈도수 시각화
    fig = plt.figure(figsize=(10,5))
    # 바 그래프
    plt.bar(hourly_counts.index, hourly_counts.values, color='skyblue')
    # 라인 차트 (같은 축에 겹쳐서 그리기)
    plt.plot(hourly_counts.index, hourly_counts.values, color='purple', alpha=0.4, marker='o', label='Frequency (Line)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Frequency')
    plt.title('Frequency by Hour of Day')
    plt.xticks(range(0, 24))
    plt.grid(axis='y')
    plt.show()

    return fig


# In[66]:


# Action: 애정도 분석

def analyze_degree_of_affection(data):
    # 피규어 생성
    fig=plt.figure(figsize=(15,12))

    # 이름 리스트 추출
    names = data['Name'].unique()

    num_names = len(names)
    
    # 필요한 행과 열의 수 계산
    num_cols = 2
    num_rows = math.ceil(num_names / num_cols)
    
    for i,name in enumerate(names):
        pattern = f'{name}|{name[1:]}'
        names_counts=data[data['Processing_Sentence'].str.contains(pattern,na=False)]['Name'].value_counts()
        
        with plt.style.context('grayscale'):
            ax = fig.add_subplot(num_rows,num_cols,i+1)
            ax.bar(names_counts.index, names_counts, color='pink', alpha=0.6)
            ax.set_title(f'{name}님에 대한 애정도')
            ax.set_xlabel('이름',fontsize=15)
            ax.set_ylabel('애정도') 
            
    plt.tight_layout()
    plt.show()

    return fig


# In[147]:


# Action: 대화 주도 분석

def analyze_lead_conversation(data):

    unique_date_dict = data.groupby('Month').apply(lambda x: x['Day'].unique().tolist()).to_dict()
    
    # 리스트 생성
    name_count = []

    for key,values in unique_date_dict.items():
        for value in values:
            selected_data = data.loc[(data['Month']==key)|(data['Day']==value)]
            selected_data = selected_data.reset_index()
            name_count.append(selected_data.loc[0,'Name'])

    # 대화 주도 리스트 카운트
    counter=Counter(name_count)
    text_nouns=dict(counter.most_common())
    
    plot_pie_chart(text_nouns)

#analyze_lead_conversation(data)


# In[146]:


def plot_pie_chart(text_nouns):

    labels = list(text_nouns.keys())
    sizes = list(text_nouns.values())
    
    # 데이터의 길이에 따라 색상 배열 생성
    num_colors = len(sizes)
    colors = cm.get_cmap('viridis', num_colors)

    # 파이 차트의 각 조각을 강조하기 위해 explode 설정
    explode = [0.1 if size == max(sizes) else 0 for size in sizes]  # 가장 큰 조각을 강조하는 예

    fig = plt.figure(figsize=(12, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors(np.arange(num_colors)),
        autopct='%0.1f%%', shadow=True)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #plt.title('종화 애정도 비율')
    plt.show()

    return fig


# In[62]:


# 대화 주제 분석

def analyze_topic_conversation(data):

    # 한글 텍스트 처리 okt 객체 생성
    okt = Okt()

    # 스탑워드 리스트 생성
    stop_words=[x for x in stopwords['Word']]
    
    # 명사  리스트 생성
    nouns = []
    
    for sentence in data['Processing_Sentence'] :
        for noun in okt.nouns(sentence) :
        # 단어 전처리 : 2음절 이상, 수사 제외 및 텍스트 마이닝을 위해 대화 내용을 명사 단위로 추출
            if len(str(noun)) >= 2 and not(match('^[0-9]', noun)) and str(noun) not in stop_words :
                nouns.append(noun)
        
    colletion_nouns = collet_nouns(nouns)

    fig = plot_collet_nouns(colletion_nouns)

    #fig = plot_word_cloud(colletion_nouns)
    
    return fig


# In[ ]:


# 대화 주제 분석(워드 클라우드)

def analyze_topic_conversation_cloud(data):

    # 한글 텍스트 처리 okt 객체 생성
    okt = Okt()

    # 스탑워드 리스트 생성
    stop_words=[x for x in stopwords['Word']]
    
    # 명사  리스트 생성
    nouns = []
    
    for sentence in data['Processing_Sentence'] :
        for noun in okt.nouns(sentence) :
        # 단어 전처리 : 2음절 이상, 수사 제외 및 텍스트 마이닝을 위해 대화 내용을 명사 단위로 추출
            if len(str(noun)) >= 2 and not(match('^[0-9]', noun)) and str(noun) not in stop_words :
                nouns.append(noun)
        
    colletion_nouns = collet_nouns(nouns)

    #fig = plot_collet_nouns(colletion_nouns)

    fig = plot_word_cloud(colletion_nouns)
    
    return fig


# In[48]:


def collet_nouns(nouns):
    # 횟수 설정
    num=20

    # 명사 카운트
    nouns_counter=Counter(nouns)

    # 딕셔너리 변경
    text_nouns=dict(nouns_counter.most_common(num))
    
    return text_nouns


# In[49]:


def plot_collet_nouns(data):

    fig = plt.figure()

    keys = list(data.keys())
    values = list(data.values())

    sns.barplot(x=keys,y=values,alpha=0.7)

    plt.xticks(rotation=90)

    plt.show()

    return fig


# In[60]:


# Action: 대화 주도 워드 클라우드

def plot_word_cloud(data):

    wordcloud = WordCloud(background_color="white",font_path=r"C:\Users\pc021\Desktop\싸인랩\업무\말뭉치\형태소분석_최종v1.1\프로그램소스\morpheme\fonts\malgun.ttf",
                     max_words=100,
                     ).generate_from_frequencies(data)

    fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    return fig


# In[61]:


analyze_topic_conversation(data)

