import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks  import get_openai_callback


with open("F:\projects\data engineering and AI\gen AI projects\mcqgen\Response.json", 'r') as file:
    RESPONSE_JSON= json.load(file)

st.title("MCQ creater application with langChain")
response = None 
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("upload a PDF or txt file")

    mcq_count = st.number_input("No. MCQs " , min_value =3 , max_value =50)
    subjects = st.text_input("insert subject", max_chars = 20)
    tone = st.text_input("complexity", max_chars = 20, placeholder = 'simple')
    button = st.form_submit_button("Create MCQs")


    if button and uploaded_file  is not None and mcq_count and subject and tone:
        with st.spinner("loading-----"):
            try:
                text= read_file(uploaded_file)
                
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {

                                'text': TEXT,
                                'number': NUMBER,
                                'subject': SUBJECT,
                                'tone' : TONE,
                                'response_json': json.dumps(RESPONSE_JSON)


                                    }
                        )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("error")
    else:
        if isinstance(response,dict):
            quiz = response.get("quiz", None)
            if quiz is not None:
                table_data = get_table_data(quiz)
                if table_data is not None:
                    df = pd.Dataframe(table_data)
                    df.index = df.index + 1
                    st.table(df)

                    st.text_area(label="review" , value = response["review"])
                else:
                    st.error("error in table data")
            else:
                st.write(response)
