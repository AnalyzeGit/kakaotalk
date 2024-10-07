#!/usr/bin/env python
# coding: utf-8

# In[45]:


# Handling
import pandas as pd # 22 years old
import numpy as np
import re
import warnings


# In[46]:


# 카카오톡 GUI 시스템 설계

# A. 원시 데이터 전처리 시스템

# B. 단답형 메시지 인원 분석

# C. 월별 대화 횟수

# D. 시간별 대화 횟수

# E. 애정도 분석

# F. 애정도 비율 분석

# I. 대화 주도 분석

# J. 월별 대화 주도 분석

# K. 대화 주제 분석(텍스트 마이닝)

# l. 워드 클라우드

# M. 사회 연결망 분석

# N. 애정도 순위 선정


# In[47]:


# Action: 초기 설정

warnings.filterwarnings('ignore')


# In[153]:


# Action: 데이터 로드

# 원시 데이터
df = pd.read_table(r"C:\Users\pc021\Desktop\성장\웹 개발\kakaotalk\데이터\KakaoTalk_20240508_1140_38_790_group.txt")

# 스탑워드 예시a
stopword = pd.read_table(r"C:\Users\pc021\Desktop\성장\웹 개발\kakaotalk\스탑워드\stopwords.txt")

# 스탑워드 예시b
stopwordb = pd.read_csv(r"C:\Users\pc021\Desktop\성장\웹 개발\kakaotalk\스탑워드\stopword_final_app.csv",encoding='cp949',index_col=0)

# 정제 예시 파일
data = pd.read_csv(r"C:\Users\pc021\Downloads\남자들의 카카오마이닝.csv",index_col = 0)


# In[154]:


# Action: 시간 데이터 추출

def generate_date_dictionary(df):
    
    df.columns=['Sentence']
    
    # 딕셔너리 생성
    date_dict = {}

    # 시간 데이터 추출
    date_data = df[df['Sentence'].str.startswith('---')]

    # 시간 데이터 정제
    date_data['Sentence'] = date_data['Sentence'].str.replace('-','')

    # 시간 데이터 딕셔너리 생성
    for index,rows in date_data.iterrows():
        date_dict[index] = rows['Sentence']

    return date_dict


# In[155]:


# Action: 데이터 전처리

def preprocess_data(df):
    # 컬럼 설정
    df.columns=['Sentence']

    # 시간 딕셔너리 생성
    date_dict = generate_date_dictionary(df)

    # 제거 인덱스 설정
    drop_list = list(date_dict.keys())
    drop_list.append(0)

    # 데이터 정제
    df_drop = df.drop(index=drop_list)

    return df_drop


# In[156]:


# Action: 이름_시각 데이터 생성

def generate_name_date_data(data):

    name_date_data = data[data['Sentence'].str.startswith('[')]

    name_date_data['name_date'] = name_date_data['Sentence'].str.split(' ').str[0:2]

    name_date_dict = {}

    for index,rows in name_date_data.iterrows():
        name_date_dict[index] = rows['name_date']
        
    return name_date_dict


# In[168]:


# Action: 문장 데이터 정제

def preprocess_sentence(data):

    data = preprocess_data(data)
    
    name_date_dict = generate_name_date_data(data)

    check_num = 0  

    for index,rows in data.iterrows():
        if rows['Sentence'].startswith('['):
            data.loc[index,'Name'] = rows['Sentence'].split(' ')[0]
            data.loc[index,'Date'] = rows['Sentence'].split(' ')[1]
            data.loc[index,'Processing_Sentence'] = rows['Sentence'].split(']')[2]
            check_num = index 
        else:
            data.loc[index,'Name'] = name_date_dict[check_num][0]
            data.loc[index,'Date'] = name_date_dict[check_num][1]
            data.loc[index,'Processing_Sentence'] = rows['Sentence']
            
    return data


# In[288]:


def apply_preprocess_fuctions(data):

    preprocessing_data = preprocess_sentence(data)
    
    date_range_dict = generate_date_dictionary(data)

    last_data = generate_date_range(preprocessing_data,date_range_dict)

    last_data = substitute_last_date(date_range_dict,last_data)

    last_data = preprocess_data_ragne(last_data)

    last_data = remove_symbol(last_data)

    last_data = refine_dataframe(last_data)

    return last_data


# In[236]:


def generate_date_range(data,date_range_dict):

    date_indexs = list(date_range_dict.keys())

    pre_index = 0
    
    for num, dict_index in enumerate(date_indexs[3-2:]):
        #print(f"현재 딕셔너리 인덱스:{dict_index}")
        for index,rows in pre_data.iterrows():
            #print(f"현재 데이터 인덱스:{index}")
            if (dict_index > index) & (index > pre_index):
                #print('조건통과')
                data.loc[index,'data_range'] = date_range_dict[date_indexs[(num+1)-1]]
                #print(f'추가:{date_range_dict[date_indexs[(num+1)-1]]}')
            else:
                #print(f'조건 실패, 과거 인덱스:{pre_index}')
                pass
        pre_index = dict_index

    return data


# In[291]:


def substitute_last_date(date_range_dict,last_data):

    date_indexs = list(date_range_dict.keys())

    null_index = last_data[last_data['data_range'].isna()].index

    last_data.loc[null_index,'data_range'] = date_range_dict[date_indexs[-1]]
    
    return last_data

