import pickle
import streamlit as st
import plotly.express as px
from digiready import *

#icon = Image.open("deci_logo.jpg")
st.set_page_config(page_title="Digital Transformation Readiness")

# xls = read_excel_file('DX.xlsx')
# df_list = read_all_sheets(xls)
# sheets = [key for key in df_list.keys()]
# get_all_answers(df_list, sheets, readiness, rand=False)
with open('df_list.pickle', 'rb') as f:
    df_list = pickle.load(f)

sheets = [key for key in df_list.keys()]
on_par = get_par(df_list)

for sheet in sheets:
    df = df_list[sheet]
    if sheet not in st.session_state:
        st.session_state[sheet] = df

for sheet in sheets:
    df_list[sheet] = st.session_state[sheet]
    
summary = get_summary(df_list)

st.title('Digital Transformation Readiness')
st.sidebar.image("deci_logo.jpg")

category = st.sidebar.selectbox('select a category', ['Home'] + sheets[:-1])
if category == 'Home':
    with st.container():
        image_col, text_col = st.columns([1,2])
        with image_col:
            st.image('tk.jpg', width=200)
        with text_col:
            st.markdown("""**Compare your digital readiness to your peers.**
            To unlock your digital agenda, you need a clear vision of where you are starting from. 
            You need to understand digital across all the component parts of your business and assess the sum of these parts. 
            This gives you essential context against which to make decisions about all of your digital initiatives, helping you to identify priorities and develop a common digital vision for your organization.""")

elif category == 'Summary':
    st.header(f'your readiness vs. industry')
    dx_readiness = get_score(df_list, sheets)
    fig = plot_vs_industry(dx_readiness, on_par)
    st.plotly_chart(fig)
else:
    df = st.session_state[category]
    questions_cat = df.keys()[0]
    st.header(f'Your answers in {category}')
    st.write('Select your answer below and click "update"')

    
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
            else:
                st.checkbox(question, False)
    
    update = st.button('update')

    if update:
        for question in df[questions_cat]:
            if st.checkbox(question):
                df.loc[df[questions_cat]==question, 'answer'] = 1
            else:
                df.loc[df[questions_cat]==question, 'answer'] = 0
    else:
        checkboxes(df, questions_cat)
    
    # save = st.button('save answers')
    # if save:
    st.session_state[category]=df

    st.dataframe(df)