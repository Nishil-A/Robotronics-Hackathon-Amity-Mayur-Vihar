#THINGS ADITYA DOESN'T NEED TO SEE :-
from logging import debug
from  flask import Flask, render_template, request
main=Flask(__name__)

@main.route('/')
def login():
    return render_template("homepage.html")
@main.route('/decision')
def decision():                            
    return render_template("decision.html")
@main.route('/decision3')
def decision3():                            
    return render_template("decision3.html")
@main.route('/decision2')
def decision2():                            
    return render_template("decision2.html")
@main.route('/result')
def result():                            
    return render_template("result.html")
@main.route('/maps')
def map():                            
    return render_template("map.html")
@main.route('/about')
def about():                            
    return render_template("about.html")
@main.route('/med')
def med():                            
    return render_template("medicine.html")




#THINGS ADITYA NEEDS TO CHECK :-
#Ignore all code with empty '#' at end as its flask based....

@main.route('/login_ch', methods = ["GET","POST"])     #
#This code is for chemist login verification
def ch_login():                                        #
    if request.method == "POST":                       #
        global username,info_entered                   #Global so that username and info entered can be accessible to other portion of code too.
        req=request.form                               
#req contains a dictionary - ["username":username,password":password,"email":email,"mobile":mobile,"city":city,"state":state]
        username=req["username"]                       #Will be storing username as entered by user
        info_entered=[req["password"],req["email"],req["mobile"],req["city"],req["state"]]
        import chemist                                  
        if chemist.verify(username,info_entered):       #Should give True if verified
            return render_template("homepage.html")     #
        else:
            return "Wrong info entered"                 #
    return render_template("login_chemist.html")        #

@main.route('/login_cl', methods = ["GET","POST"])      #
#This code is for client login verification, all variables are storing equivalent values as for chemist verification
def cl_login():                                         #
    if request.method == "POST":                        #
        global username,info_entered
        req=request.form
        username=req["username"]
        info_entered=[req["password"],req["email"],req["mobile"],req["city"],req["state"]]
        import client
        if client.verify(username,info_entered):        #Should give true if verified
            return render_template("homepage.html")     #
        else:
            return "wrong info entered"                 #
    return render_template("login_client.html")         #

@main.route('/signup_cl', methods = ["GET","POST"])     #
#This code is for client registration all variables are carying similiar value as before
def cl_signup():                                        #
    if request.method == "POST":                        #
        global username,info_entered
        req=request.form
        username=req["username"]
        info_entered=[req["password"],req["email"],req["mobile"],req["city"],req["state"]]
        import client
        client.set_client_data(username,info_entered)   #Should store client info in db
        return render_template("homepage.html")         #
    return render_template("form_client.html")          #

@main.route('/signup_ch', methods = ["GET","POST"])     #
#This code is for chemist registration all variables are carying similiar value as before
def ch_signup():                                        #    
    if request.method == "POST":                        #
        global username,info_entered
        req=request.form
        username=req["username"]
        info_entered=[req["password"],req["email"],req["mobile"],req["city"],req["state"]]
        import chemist
        chemist.set_chem_data(username,info_entered)     #Should store chemist data in db
        return render_template("homepage.html")          #
    return render_template("form_chemist.html")          #

@main.route('/update_ch', methods = ["GET","POST"])      #
#This code is to update any of the details of a specific chemist username, variables similiar
def ch_update():                                         #
    if request.method == "POST":                         #
        req=request.form
        new_info=[req["password"],req["email"],req["mobile"],req["city"],req["state"]]
        #This new variable 
        import chemist
        try:
            if chemist.verify(username,info_entered):    #Should give true if verified
                chemist.update_profile(username,info_entered,new_info)
                #Is supposed to update info of the chemist username

#info entered will be available as a global variable if already 'signed in'/'registered just now', 
#else code returns error and 'except' will run which you dont need to worry about 
        except:
            return "Wrong info entered or not signed in."#
        return render_template("homepage.html")          #
    return render_template("update_chemist.html")        #

@main.route('/update_cl', methods = ["GET","POST"])      #
#This code is to update any of the details of a specific client username, variables similiar, working also similiar
def cl_update():                                         #
    if request.method == "POST":                         #
        req=request.form
        new_info=[req["password"],req["email"],req["mobile"],req["city"],req["state"]]
        #This variable stores details in same way as info_entered
        import client
        try:
            if client.verify(username,info_entered):
                client.update_profile(username,info_entered,new_info)
                return render_template("homepage.html")  #
        except:
            return "Wrong info entered or not signed in."#
    return render_template("update_client.html")         #




#THINGS ADITYA NEEDS TO WRITE FOR :-
#Ignore all code with empty '#' at end as its flask based....

@main.route('/stock', methods = ["GET","POST"])          #
#This function stores medicines and quantity available to db for specific chemist username
def stock():                                             #
    if request.method == "POST":                         #
        med_info=request.form     #Will give you {"med1":quantity,"med2":quantity,"med3":quantity}
        #We only have exactly 3 medicines for now as its a prototype!
        import chemist
        try:
            if chemist.verify(username,info_entered):    #Gives True if verified
                chemist.
        #If verified then here goes the function which will add medicines along with quantity to database
        except:
            return "Wrong info entered or not signed in." #
    return render_template("stock.html")                  #

@main.route('/medicine', methods = ["GET","POST"])        #
#This function finds best store for medicine and returns its data, adress etc.
def med_name():                                           #
    if request.method == "POST":                          #
        import client
        try :
            if client.verify(username,info_entered):      #Gives true if verified
                req=request.form                          #req contains a dictionary={"medname":Name of medicine to find store for}
                medicine=req["medname"].lower()        
#At this moment info_entered variable contains : [email,password,mobile,city,state] for client's account.
                st=[]
#Create code such that this st list contains the best store's data in this order : 
# [username,city,state,mobile]
                numbers = [0,1,2,3]                       #
                give=["Shop name","City","State","Mobile"]#
                return render_template("result.html",store_information=st,numbers=numbers,give=give) #
        except:                                           
                return "Medicine not found or not logged in"#
        return render_template("form_client.html")        #



#APP Runner :-

if __name__== "__main__":                                # 
     main.run(debug=True)                                #