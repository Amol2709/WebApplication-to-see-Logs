"""
 		.SYNOPSIS
 				
 				This is only python script in this Web-Based Application.
 				This script contains defination of all routes (html pages).
 				To run this script open command prompt in same directory and type python main.py.
 				To run this application you must have flask and flask paginate module installed.
 				To installed both module type --------------> pip install flask
 				                              --------------> pip install flask_paginate in command prompt.
 		

 		. Description
				This script contain two main function : home and second
				Function home will get all attribute whatever user will eneterd on very first html page when user will run application
				Function second will handle pagination and read respective log file and display Logs on another html page

		

		.INPUTS
				None
		.OUTPUTS
                Display Log on second html page if found any.
        

        .NOTES
        		Author: Amol Chaudhari
        		Creation Date: 10-02-2021
        		purpose: CIS Automation OJT Task
        		Assigned By: Nikhil Kumar

        .Example
        		To run this Web Application type: Python main.py 
        		Then open any browser and type : http://127.0.0.1:5000/


    """









#### ------------------------ Importin all Necessary Packages ------------------------------####


from flask import Flask, render_template,request,redirect,url_for
from flask_paginate import Pagination, get_page_args


####------------------------ Initailizing Flask app variable -----------------------------#####
app = Flask(__name__)
pagination_counter = list(range(100)) # Initializing variable  for Pagination 


###----------------------- Defining Route if any error occured -------------------------#####

@app.route("/error_html")
def error_html():
	temp_error=request.args.get('TEMP_ERROR')
	return render_template('error_html.html',ERROR=temp_error)

@app.route("/error")
def error():
	return render_template('error.html')



#### ----------------------- Defining Route for Home Page -------------------------------------------
@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():

	'''
		This Function will read all Inputs Entered By Users and Pass it to second route.
	'''
	try:
		if request.method =='POST':
			if request.form["submit"] == "ShowDetails":
				name = request.form.get("name")
				Type = request.form.get("type")
				dd = request.form.get("DATE")
				return redirect(url_for('second',username=name,usertype=Type,userdate=dd))
		return render_template('index.html')
	except:
		return redirect(url_for('error_html'))


#### ------------------------------------------- Function Defined to initialize pagination variable------------------------####
def get_users(offset=0, per_page=10):
	return pagination_counter[offset: offset + per_page]

#### ------------------------------------------ Defining Defination of Second Route ----------------------------------------####
@app.route("/second")
def second():

	'''
		This Function will read respective logs file and if found any entry matched according to details entered by user that will be displayed.
	'''
	try:

		###---------------- Reading Input Entered By User in Home Page----------------------####

		temp_user=request.args.get('username')
		#print(type(temp_user))
		temp_type=request.args.get('usertype')
		#print(temp_type)
		temp_date=request.args.get('userdate')

		### --------------- Converting Input into Lower Case -----------------------------######
		temp_user = temp_user.lower()
		temp_type = temp_type.lower()

		###--------------- Making Date into Correct Format as appeared in Log File ---------#####
		temp_L=temp_date.split("-")
		temp_L1 = temp_L.copy()
		temp_L[0]=temp_L1[2]
		temp_L[2]=temp_L1[0]
		str1="-"
		per_date = str1.join(temp_L)

		FINAL_OUTPUT=[] # Initializing List to store logs
		


		###------------------  Reading Log File -------------------------------------------####
		for i in range(1,4):
			###----------------- Try Catch Block if Log Do not Exist then it will show Error Message and redirect to Error.html ---------------###
			try:
				filename= "Log_"+str(i)+".txt";
				file1 = open(filename, 'r')
				Lines = file1.readlines()
				file1.close()
				
			except:
				return redirect(url_for('error'))
			### ------------------------------ Reading File and Store Logs if matched with Entered User Details ----------------------------- #####
			else:
				for line in Lines:
					line = line.lower()
					#print(line)
					#print(per_date)
					#print('Ammmmmmmmm')
					#print(line.find(per_date))
					if line.find(per_date) !=-1 and line.find(temp_user) !=-1 and line.find(temp_type) !=-1 and (temp_user!='all' and temp_type!='all'):
						#print("found")
						#print(line)
						number=line.find(temp_user)
						#print(number)
						#print(line[number+len(temp_user):-1])
						FINAL_OUTPUT.append(line[number+len(temp_user):-1])

					elif line.find(per_date) !=-1 and( temp_type=='all' and temp_user=='all'):
						#print('oooo')
						number=line.find(per_date)
						print(line)
						line[number+len(per_date):-1]
						FINAL_OUTPUT.append(line[number+len(per_date):-1])

					if line.find(per_date) !=-1 and( temp_type=='all' and (line.find(temp_user) !=-1 and temp_user!='all')):
						#print('oooo')
						#print(line.find(temp_user))
						number=line.find(temp_user)
						line[number+len(temp_user):-1]
						FINAL_OUTPUT.append(line[number+len(temp_user):-1])
					if line.find(per_date) !=-1 and( temp_user=='all' and (line.find(temp_type) !=-1 and temp_type!='all')):
						#print('2222')
						number=line.find(temp_user)
						line[number+len(temp_user):-1]
						FINAL_OUTPUT.append(line[number+len(temp_user):-1])
					

					
						
					
			### ------------------------------------------------------------------------------------------------------------------------------- ###




		### -----------  Logic To define only 4 Logs in one page (Pagination) so that it look neat and clean-----------------------------------------------------------######
		if len(FINAL_OUTPUT)!=0:


			###------------------------Pagination Initialization ------------------------------------------####
			page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
			pagination_users = get_users(offset=offset, per_page=per_page)
			pagination = Pagination(page=page, per_page=4, total= len(pagination_counter),css_framework='bootstrap4')
			print(len(FINAL_OUTPUT))


			if len(FINAL_OUTPUT)>=4:
				if (len(FINAL_OUTPUT) - ((page-1)*4)) >0:
					if (len(FINAL_OUTPUT) - ((page-1)*4)) >=4:
						temp_msg_1 = []
						for j in range((page-1)*4,((page-1)*4)+4):
							temp_msg_1.append(FINAL_OUTPUT[j])
							#print(j)
						return render_template('second.html',user=temp_user.upper(),TYPE=temp_type.upper(),DATE=temp_date,msg=temp_msg_1,LEN=len(temp_msg_1),pagination=pagination)
						
					else:
						temp_msg_2=[]
						for k in range(len(FINAL_OUTPUT),((page-1)*4),-1):
							temp_msg_2.append(FINAL_OUTPUT[k-1])
						return render_template('second.html',user=temp_user.upper(),TYPE=temp_type.upper(),DATE=temp_date,msg=temp_msg_2,LEN=len(temp_msg_2),pagination=pagination)
				else:
					return render_template('second.html',user=temp_user.upper(),TYPE=temp_type.upper(),DATE=temp_date,msg="No Records to display",LEN=0,pagination=pagination)
			else:
				if (len(FINAL_OUTPUT) - ((page-1)*4)) >=0:
					return render_template('second.html',user=temp_user.upper(),TYPE=temp_type.upper(),DATE=temp_date,msg=FINAL_OUTPUT,LEN=len(FINAL_OUTPUT),pagination=pagination)
				else:
					return render_template('second.html',user=temp_user.upper(),TYPE=temp_type.upper(),DATE=temp_date,msg="No Records to display",LEN=0,pagination=pagination)


		###------------------------------------If No Records Found -------------------------------------------------------------------- ###
		if len(FINAL_OUTPUT)==0:
			page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
			pagination_users = get_users(offset=offset, per_page=per_page)
			pagination = Pagination(page=page, per_page=4, total= len(pagination_counter),css_framework='bootstrap4')
			return render_template('second.html',user=temp_user.upper(),TYPE=temp_type.upper(),DATE=temp_date,msg="No Records to display",LEN=0,pagination=pagination)

	except Exception as E:
		####-----------------------------IF any Exception Occured Redirect User to Error Page-------------------------####
		return redirect(url_for('error_html',TEMP_ERROR=E))





if __name__ == '__main__':
    app.run(debug=True)