#!pip install openai
import os
import openai
import pandas as pd
import numpy as np
import time
import random


openai.organization = "org-XXXXXXXXXXXXXXXXXXXXXX"
openai.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


lazy_doc_df = pd.read_excel("lazy_doc_with_source_code_GPT-3_DocAdded_new.xlsx")

lazy_doc_df = lazy_doc_df.replace({r"_x([0-9a-fA-F]{4})_": ""}, regex=True)

non_lazy_doc_df = non_lazy_doc_df.replace({r"_x([0-9a-fA-F]{4})_": ""}, regex=True)
non_lazy_code = row['Method Code']
non_lazy_doc = row['Documentation']

generated_doc_list = []


for idx,row in lazy_doc_df.iterrows():
	print(idx)
	code = row['Method Code']
	
	prompt = "Method Code:\n"+non_lazy_code+"\nDocumentation:\n"+non_lazy_doc+"\n\nMethod Code:\n"+code+"\nDocumentation:\n"
	zero_shot_results = dict()
	response = openai.Completion.create(
	    engine="text-davinci-002",#"code-davinci-002",#
	    prompt=prompt,
	    temperature=0.5,
	    max_tokens=128,
	    top_p=1,
	    frequency_penalty=0,
	    presence_penalty=0,
	    best_of = 1,
	    stop=["Code:"]
	)
	#print(response["choices"][0].text)
	#break

	generated_doc_list.append(response["choices"][0].text)

lazy_doc_df['GPT-3 documentation'] = generated_doc_list



lazy_doc_df.to_excel("lazy_doc_with_source_code_GPT-3_DocAdded_FINAL.xlsx", index = False,encoding='utf8')


