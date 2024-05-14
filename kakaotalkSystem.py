#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Handling
import sys
import os
import pandas as pd
import threading
import time

# System 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, StringVar

# Visualize
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import font_manager, rc
from matplotlib.ticker import FuncFormatter

# Moduel
from kakaotalk import * ## 22years old
from kakaotalkAnalysis import *


# In[2]:


# Action: 기본 설정

# 모든 경고 무시
warnings.filterwarnings('ignore')

# 멜건 폰트 설정
font_path = r"C:\Users\pc021\Desktop\싸인랩\업무\말뭉치\형태소분석_최종v1.1\프로그램소스\morpheme\fonts\malgun.ttf"  # 경로는 시스템에 맞게 조정하세요
font_prop = fm.FontProperties(fname=font_path)

plt.rc('font', family=font_prop.get_name())
plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지


# In[3]:


def find_kakaotalk_txt(folder_selected):
    # 파일 경로 리스트 생성
    kakaotalk_dataframes = {}
    
    for filename in os.listdir(folder_selected):
        ## 파일 이름과 확장자를 분리
        file_name_with_extension = os.path.basename(filename)
        file_name = os.path.splitext(file_name_with_extension)[0]
        
        # 데이터 프레임 경로
        file_path = os.path.join(folder_selected, filename)
        remove_extension_file_path = os.path.join(folder_selected, file_name)
        
        # 데이터 프레임 생성
        data = pd.read_table(file_path)
        
        # 텍스트 데이터 프레임 폴더 저장 
        kakaotalk_dataframes[remove_extension_file_path] = data

    return kakaotalk_dataframes


# In[4]:


def upload_folder():

    # 현재 폴더 생성
    folder_selected = filedialog.askdirectory()

    # 데이터 프레임 리스트 반환
    kakaotalk_dataframes = find_kakaotalk_txt(folder_selected)
    
    for to_save_file_path,dataframe in kakaotalk_dataframes.items():
        #print(file_path)
        preprocessing_data  = apply_preprocess_fuctions(dataframe)
        preprocessing_data.to_csv(f"{to_save_file_path}.csv", index=False)

        messagebox.showinfo("information",'데이터 처리가 완료되었습니다.')


# In[5]:


def upload_file():
    # 전역 변수 설정
    global data
    global file_name
    
    # 파일 경로 로드
    file_path = filedialog.askopenfilename()

    # 파일 이름만 추출
    file_name_with_extension = os.path.basename(file_path)

    # 확장자 제거
    file_name, _ = os.path.splitext(file_name_with_extension)
    
    # 데이터 로드
    data = pd.read_csv(fr"{file_path}")


# In[6]:


def on_button_click(button_name):
    messagebox.showinfo("버튼 클릭", f"{button_name} 버튼이 클릭되었습니다.")


# In[7]:


def embed_figure():
    """ 피규어 시스템 임베딩 
    """
    tag_menu_get = tag_menu.get()
    
    if tag_menu_get == '단답형 메시지 인원 분석':
        fig = analyze_short_answer_messages(data)
        
    elif tag_menu_get == '월별 대화량':
        fig = analyze_monthly_conversations(data,file_name)
        
    elif tag_menu_get == '애정도 분석':
        fig = analyze_degree_of_affection(data,file_name)
        
    elif tag_menu_get == '대화 주도 분석':
        fig = analyze_lead_conversation(data,file_name)   
        
    elif tag_menu_get == '대화 주제 분석':
        fig = analyze_topic_conversation(data,file_name)
        
    elif tag_menu_get == '대화 주제 분석(클라우드)':
        fig = analyze_topic_conversation_word_cloud(data,file_name)
        
    else:
        fig = analyze_conversations_by_time(data,file_name)
        
    # 전역 변수 설정
    global canvas
    
    if canvas:
        canvas.get_tk_widget().destroy()  # 기존 캔버스 제거
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # 캔버스를 팩을 사용하여 프레임에 추가


# In[8]:


def only_numbers(char):
    return char.isdigit()

def update_user_input(*args):
    user_input.delete(0, 'end')
    user_input.insert(0, tag_options[tag_variable.get()])


# In[9]:


# 크기 조절 함수
def adjust_combobox_size(event):
    width = len(tag_menu.get()) + 2  # 선택된 항목의 길이에 따라 너비 조절
    tag_menu.config(width=width)


# In[10]:


# Action: 스타일 설정

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')  # 클램 테마는 더 현대적인 느낌을 줍니다.
    style.configure('TLabel', font=('Arial', 10), background='white')
    style.configure('TEntry', font=('Arial', 10), padding=5)
    style.configure('TButton', font=('Arial', 10), padding=5)
    style.configure('TCombobox', font=('Arial', 10), padding=5)
    style.configure("TCombobox", arrowsize=15, padding=(5, 5, 5, 5))  # padding=(왼쪽, 위, 오른쪽, 아래)
    style.configure("TCombobox", width=5)  # 너비 조절
    style.map('TCombobox', fieldbackground=[('readonly', 'white')],
              selectbackground=[('readonly', 'white')],
              selectforeground=[('readonly', 'black')])
    style.configure('TFrame', background='white')  # 프레임 배경색 설정
    style.configure('Horizontal.TProgressbar', background='#FA8072')


# In[11]:


def update_status_and_search():
    """
    로딩 함수 구현
    """
    try:
        # 로딩 상태 업데이트
        status_label.config(text="로딩 중...")
        root.update_idletasks()  # UI 업데이트 강제 실행

        # 기존 검색 함수 호출
        embed_figure()

        # 작업 완료 후 상태 업데이트
        status_label.config(text="작업 완료")
        
    except:
        # 오류 발생 시 메시지 업데이트
        status_label.config(text="작업 실패:")
        print(f"오류 발생: {e}")


# In[ ]:


# Action: 순찰 경로 최적화 GUI

# GUI 생성    
root = tk.Tk()
root.title("카카오톡 분석기 시스템")
root.geometry("800x800")

# 위젯들을 그리드에 배치하기 전에 각 행의 비율을 설정합니다.
root.grid_rowconfigure(0, weight=5)
root.grid_rowconfigure(2, weight=90)  # 그래프 프레임에 더 큰 가중치를 부여합니다.
root.grid_rowconfigure(3, weight=5)  

# 열의 비율도 설정합니다.
root.grid_columnconfigure(0, weight=5)
root.grid_columnconfigure(1, weight=25)  
root.grid_columnconfigure(2, weight=25)
root.grid_columnconfigure(3, weight=25)
#root.grid_columnconfigure(4, weight=100) 

configure_styles()

# (*,0)
tag_menu_label = tk.Label(root, text="기능 선택", anchor='w',width=0)
tag_menu_label.grid(row=0, column=0, sticky='we', padx=10, pady=5)

# (1,1)
tag_variable = StringVar(root)
tag_options = {
    "단답형 메시지 인원 분석": "",
    "애정도 분석":"",
    "월별 대화량": "",
    "시간대별 대화량":"",
    "대화 주도 분석":"",
    "대화 주제 분석":"",
    "대화 주제 분석(클라우드)":"",
    "직접 입력": "",
               }
tag_menu = ttk.Combobox(root, textvariable=tag_variable, values=list(tag_options.keys()), state='readonly', width=5)
tag_menu.grid(row=0, column=1, sticky='we', padx=10, pady=5)
tag_menu.set("직접 입력")

# (1,2) 
# 분석 시작 버튼
upload_button = ttk.Button(root, text="분석", command=update_status_and_search,width=0)
upload_button.grid(row=0, column=3, padx=10, pady=10, sticky='we')

# (3,1) 
# 프레임을 그리드에 추가합니다.
frame = ttk.Frame(root)
frame.grid(row=2, column=0, columnspan=4, sticky='nsew')  # 프레임을 네 번째 행에 배치합니다.

# (4,3)
# 파일 업로드 버튼
file_upload_button = ttk.Button(root, text="파일 업로드", command=upload_file, width=2)
file_upload_button.grid(row=3, column=2, padx=10, pady=10, sticky='we')

# (4,4)
# 폴더 업로드 버튼
upload_button = ttk.Button(root, text="폴더 업로드", command=upload_folder, width=2)
upload_button.grid(row=3, column=3, padx=10, pady=10, sticky='we')

# 초기 캔버스 설정을 None으로 합니다. 'embed_figure' 함수 정의가 필요합니다.
canvas = None

# Combobox에서 항목이 선택될 때 함수를 실행하도록 이벤트 바인딩
tag_menu.bind("<<ComboboxSelected>>", embed_figure)

# 상태 레이블
status_label = tk.Label(root, text="")
status_label.place(relx=0.5, rely=0.05, anchor='center')

root.mainloop()


# In[12]:


#departure_entry = ttk.Entry(root)
#departure_entry.grid(row=0, column=12, sticky='we', padx=10, pady=5)

# 도착지 라벨과 입력 필드를 그리드에 배치합니다.
#destination_label = tk.Label(root, text="도착지", anchor='w')
#destination_label.grid(row=12, column=0, sticky='we', padx=10, pady=5)

#destination_entry = ttk.Entry(root)
#destination_entry.grid(row=12, column=12, sticky='we', padx=10, pady=5)

# 검색 버튼을 그리드에 배치합니다.
#search_button = ttk.Button(root, text="검색",command=update_status_and_search)  # 'embed_figure' 함수 연결 필요
#search_button.grid(row=2, column=0, columnspan=2, pady=10, sticky='we')

#root.grid_rowconfigure(1, weight=12)
#root.grid_rowconfigure(2, weight=122)
#root.grid_rowconfigure(3, weight=212)
` 
# 열의 비율도 설정합니다.
#root.grid_columnconfigure(0, weight=12)
#root.grid_columnconfigure(12, weight=3)  # 입력 필드에 더 많은 공간을 할당합니다.

# 파일 업로드 버튼
#short_answer = ttk.Button(root, text="단답형 인원 분석", command=embed_figure, width=20)
#short_answer.grid(row=7, column=0, padx=10, pady=10, sticky='we')

# 상태 레이블
#status_label = tk.Label(root, text="")
#status_label.grid(row=3 ,column=0, columnspan=2, sticky='nsew', padx=10, pady=20)

