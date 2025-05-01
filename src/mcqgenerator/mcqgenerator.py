import os, json , pandas as pd, traceback
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


from langchain.llms import OpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks  import get_openai_callback
import PyPDF2


load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    openai_api_key=KEY,
    model_name="gpt-4",
    temperature=0.3 
)
print(KEY)
template_1 = """
Text:{text}

you are an expert MCQ question maker. given the above text, it is your job to create a quiz of {number} of MCQ for {subject} students in {tone} .
Make sure the questions are not repeated and check all the questions to be relevent to the given text as well. make sure to format your responses like RESPONSE_JSON 
below and use it as a guide.

Ensure to make {number} MCQs.

###RESPONSE JSON
{response_json}

"""
template_2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""


quiz_generation_prompt = PromptTemplate(

    input_variables = ['text', 'number', 'subject', 'tone', 'response_json'],
    template = template_1
)
quiz_evaluation_prompot = PromptTemplate(
        input_variables = ['subject', 'quiz'],
        template = template_2

)
quiz_chain = LLMChain(llm = llm, prompt= quiz_generation_prompt, output_key ='quiz',verbose = True)
review_chain= LLMChain(llm=llm , prompt = quiz_evaluation_prompot , output_key = 'review', verbose = True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain],
                                        input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], 
                                        verbose=True,)
