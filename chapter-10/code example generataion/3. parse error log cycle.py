import os.path,subprocess
from subprocess import STDOUT,PIPE
import pandas as pd
import numpy as np

new_cycle_int = 1
new_cycle_number = "Cycle-"+str(new_cycle_int)

prev_cycle_int = new_cycle_int-1
prev_cycle_number = "Cycle-"+str(prev_cycle_int) 



log_file = open("log"+str(new_cycle_int)+".txt", "r")
 
#read whole file to a string
log_data = log_file.read()
 
#close file
log_file.close()


log_data_list = log_data.split('DELIM')

#print(log_data_list[0])

log_id_error_dict = {}

idx=0

for this_log_data in log_data_list:
	idx+=1
	print(idx)
	this_log_data_parsed = this_log_data.split('Unknown Issue')
	#print(this_log_data_parsed[1])
	#break
	this_log_error = this_log_data_parsed[0]
	this_log_id = int(this_log_data_parsed[1].strip())
	log_id_error_dict[this_log_id] = this_log_error


#print(log_id_error_dict.keys())
#print(log_id_error_dict[1453])

lazy_doc_df = pd.read_excel("lazy_doc_cycle"+str(new_cycle_int)+"_eval.xlsx")

lazy_doc_df = lazy_doc_df.replace({r"_x([0-9a-fA-F]{4})_": ""}, regex=True)


new_output_msg_list = []

for idx, row in lazy_doc_df.iterrows():
	output_msg = row['Output '+new_cycle_number]
	this_id = row['Id']
	if output_msg == 'Unknown Issue Occured':
		output_msg = log_id_error_dict[this_id]
	new_output_msg_list.append(output_msg)


lazy_doc_df['Output '+new_cycle_number] = new_output_msg_list


lazy_doc_df.to_excel("lazy_doc_cycle"+str(new_cycle_int)+"_final.xlsx", index=False)

