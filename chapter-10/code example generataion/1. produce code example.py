#!pip install openai
import os
import openai
import pandas as pd
import numpy as np
import time
import random

import backoff  # for exponential backoff




openai.organization = "org-XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
openai.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"



@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


lazy_doc_df = pd.read_excel("lazy_doc_with_source_code_GPT-3_DocAdded_FINAL.xlsx")

lazy_doc_df = lazy_doc_df.replace({r"_x([0-9a-fA-F]{4})_": ""}, regex=True)


generated_code_list = []


for idx,row in lazy_doc_df.iterrows():
	print(idx)

	code = row['Method Code']
	class_name = row['Class Name']
	documentation_new_gpt3 = row['GPT-3 documentation']
	method_name = row['Method Name']

	prompt = "Method Code:\n"+code+"\nClass:\n"+class_name+"\nDocumentation:\n"+documentation_new_gpt3+"\nGenerate a code example for the above method and documentation:\n"
	zero_shot_results = dict()
	
	response = completions_with_backoff(
	    engine="text-davinci-003", #"text-davinci-002" #"code-davinci-002",
	    prompt=prompt,
	    temperature=0.5,
	    max_tokens=512,#768,
	    top_p=1,
	    frequency_penalty=0,
	    presence_penalty=0,
	    best_of = 1,
	    #stop=["Code:"]
	)
	#print(response["choices"][0].text)
	#break

	generated_code_list.append(response["choices"][0].text)

lazy_doc_df['GPT-3 Code Example'] = generated_code_list



lazy_doc_df.to_excel("lazy_doc_with_source_code_GPT-3_CodeExampleAdded_withComment.xlsx", index = False,encoding='utf8')