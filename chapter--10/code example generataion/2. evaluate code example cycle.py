import os.path,subprocess
from subprocess import STDOUT,PIPE
import pandas as pd
import numpy as np


new_cycle_int = 1
new_cycle_number = "Cycle-"+str(new_cycle_int)

prev_cycle_int = new_cycle_int-1
prev_cycle_number = "Cycle-"+str(prev_cycle_int) 


lazy_doc_df = pd.read_excel("lazy_doc_cycle"+str(new_cycle_int)+"_gen.xlsx")
lazy_doc_df = lazy_doc_df.replace({r"_x([0-9a-fA-F]{4})_": ""}, regex=True)




def compile_java(java_file_name):
    subprocess.check_call(['javac', java_file_name])

def execute_java(java_file_name):
    java_class,ext = os.path.splitext(java_file_name)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    return stdout,stderr




generated_code_example_list = []

code_example_output_list = []

unknown_issue_count = 0

error_count = 0

for idx,row in lazy_doc_df.iterrows():
	#print(idx)

	serial_id = row['Id']
	generated_code_example = row['Code Example ('+new_cycle_number+')']


	generated_code_example_list.append(generated_code_example)
	

	java_file_name = generated_class_name+".java"

	

	
	java_file = open(java_file_name, "w")
	java_file.write(generated_code_example)
	java_file.close()

	


	try:
		compile_java(java_file_name)
		code_example_output,error = execute_java(java_file_name)


		code_example_output_list.append(code_example_output.decode('utf-8').strip())
	except Exception as e:
		print("Unknown Issue")
		print(serial_id)
		print("DELIM")
		unknown_issue_count+=1
		code_example_output_list.append("Unknown Issue Occured")




for msg in code_example_output_list:
	try:
		if "error" in msg.lower():
			error_count+=1
	except:
		pass

print("Error Count:")
print(error_count)

lazy_doc_df['Output '+new_cycle_number] = code_example_output_list

lazy_doc_df['Code Example ('+new_cycle_number+')'] = generated_code_example_list


lazy_doc_df = lazy_doc_df.replace({r"_x([0-9a-fA-F]{4})_": ""}, regex=True)

lazy_doc_df.to_excel("lazy_doc_cycle"+str(new_cycle_int)+"_eval.xlsx", index=False)