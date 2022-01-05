# run it in terminal using: streamlit run tomek_streamlit.py
# it requires:
#    tomek's xls in the same folder
#    digiready.py in the same folder
#    deci_logo.jpg in the same folder


import numpy as np
import pandas as pd
from math import pi
import plotly.graph_objects as go
import random
import streamlit as st

readiness = {}

def read_excel_file(file_path):
    xls = pd.ExcelFile(file_path)
    return xls

def read_all_sheets(xls):
    df_list = {}
    for sheet in xls.sheet_names:
        df_list[sheet] = pd.read_excel(xls, sheet)
    return df_list

def get_summary(df_list):
    summary = df_list['Summary']
    summary = summary.iloc[2:]
    summary = summary[['Unnamed: 1', 'Unnamed: 2']]
    summary = summary.rename(columns={'Unnamed: 1':'dimension', 'Unnamed: 2': 'result'})
    return summary

def fill_random(summary):
    summary['result'] = np.random.randint(50, 70, size=len(summary))
    return summary

def get_par(df_list, sheet='Arkusz2', comparison='On Par'):
    sh = df_list[sheet]
    sh = sh.rename(columns=lambda x: x.strip())
    sh = sh[['Dimension', 'On Par']]
    sh = sh.iloc[7:13]
    on_par = list(sh[comparison])
    on_par = [x*100 for x in on_par]
    return on_par

def simple_plt(df):
    categories=list(df['dimension'])
    values=df['result'].values.flatten().tolist()
    N = len(categories)

    values.append(values[0])
    categories.append(categories[0])

    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(values))
    plt.figure(figsize=(10, 10))
    plt.subplot(polar=True)
    plt.plot(label_loc, values)
    plt.title('Digital readiness', size=30, y=1.05)
    plt.ylim(0, 100)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)

def get_sheet(df_list,sheet_name):
    sheet = df_list[sheet_name]
    col = [key for key in sheet.keys() if 'Unnamed:' not in key][0]
    df = sheet[sheet[col].notna()]
    df = df[[col, 'Unnamed: 2']]
    df = df.rename(columns={'Unnamed: 2': 'answer'})
    return df

def get_answers(df, rand=False):
    col = [key for key in df.keys() if 'answer' not in key][0]
    for question in df[col]:
        if rand:
            answer = random.choice([0, 1])
        else:
            answer = 0
        df.loc[df[col]==question, 'answer'] = answer
    return df

def add_answers(df, answers_dict):
    key = df.keys()[0]
    result =  sum(df['answer'])/len(df)
    answers_dict[key] = result   


# def answers_plot(df_list, answers_dict):
#     for key = df.keys()[0]
#     result =  sum(df['answer'])/len(df)
#     answers_dict[key] = result   answers_dict[key] = result


def get_all_answers(df_list, sheets, ans, rand=False):
    for sheet in sheets[1:-1]:
        df = get_sheet(df_list, sheet)
        df = get_answers(df, rand)
        df_list[sheet] = df
        add_answers(df, ans)

def get_score(df_list, sheets):
    dx_readiness = {}
    for sheet in sheets[1:-1]:
        df = df_list[sheet]
        key = df.keys()[0]
        result =  sum(df['answer'])/len(df)
        dx_readiness[key] = result
    return dx_readiness
            


def plot_vs_industry(answers, on_par):
    cat = list(answers.keys())
    val = [val*100 for val in answers.values()]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=on_par,
        theta=cat,
        fill='toself',
        name='industry average'
    ))
    fig.add_trace(go.Scatterpolar(
        r=val,
        theta=cat,
        fill='toself',
        name='your company'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 100]
        )),
    showlegend=False
    )
    fig.update_polars(angularaxis_rotation=20)
    fig.update_layout(showlegend=True)
    return fig


def update_answers(df, questions_cat):
    for question in df[questions_cat]:
        if st.checkbox(question):
            df.loc[df[questions_cat]==question, 'answer'] = 1
        else:
            df.loc[df[questions_cat]==question, 'answer'] = 0
    return df

def checkboxes(df, questions_cat):
    for question in df[questions_cat]:
        if int(df.loc[df[questions_cat]==question]['answer']):
            st.checkbox(question, True)
