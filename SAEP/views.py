from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from . import models
import time
from django.core.mail import send_mail
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import settings
import pymongo
from collections import defaultdict
import time

curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL
client = pymongo.MongoClient("mongodb+srv://analytics:analytics-password@mfix.m0l9v.mongodb.net/mflix?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["mflix"]
col = db["logins"]
prof=db['profile']
cor=db['course']
bog=db['blog']
subs=db['subscription']
feed=db['feedback']
pay=db['payment_id']

def home(request):	
    courseDetails= list(cor.find({},{'_id':0,'name':1,'content':1,'coverfilename':1}))
    course=defaultdict(list)
    t=len(courseDetails)
    if t>4:
        t=4
    for sub in courseDetails:
        for key in sub:
            course[key].append(sub[key]) 
    datad=list()
    data=list()
    for i in range(t):
        data=[]            
        data.append(course['coverfilename'][i])
        data.append(course['name'][i])
        data.append(course['content'][i])
        datad.append(data)
    blogDetails= list(bog.find({},{'_id':0,'title':1,'content':1,'filename':1}))
    blog=defaultdict(list)
    r=len(blogDetails)
    if r>3:
        r=3
    for sub in blogDetails:
        for key in sub:
            blog[key].append(sub[key]) 
    bloglist1=list()
    bloglist2=list()
    for j in range(r):
        bloglist1=[]            
        bloglist1.append(blog['filename'][j])
        bloglist1.append(blog['title'][j])
        bloglist1.append(blog['content'][j])
        bloglist2.append(bloglist1)
    feedDetails=list(feed.find({}))
    feeds=defaultdict(list)
    for sub in feedDetails:
        for key in sub:
            feeds[key].append(sub[key])
    h=len(feedDetails)
    if h>3:
        h=3
    test=list()
    test1=list()
    for b in range(h):
        proDetails=list(prof.find({'email':feeds['email'][b]},{'_id':0,'name':1,'lastname':1,'filename':1}))
        profile=defaultdict(list)
        for sub in proDetails:
            for key in sub:
                profile[key].append(sub[key])
        test=[]
        test.append(feeds['review'][b])
        test.append(profile['name'][0])
        test.append(profile['lastname'][0])
        test.append(profile['filename'][0])
        test1.append(test)
    countstudent=len(list(col.find({'role':"student"})))
    countteacher=len(list(col.find({'role':"tutor"})))
    countcourse=len(list(cor.find({})))
    countpayment=len(list(pay.find({})))
    return render(request,'index.html',{'curl':curl,'media_url':media_url,'data':datad,'blog':bloglist2,'test':test1,'totals':countstudent,'totalt':countteacher,'totalc':countcourse,'totalp':countpayment})

def course(request):
    corDetails=list(cor.find({}))
    cors=defaultdict(list)
    for sub in corDetails:
        for key in sub:
            cors[key].append(sub[key])
    l=len(corDetails)
    data=list()
    datad=list()
    for j in range(l):
        data=[]
        data.append(cors['coverfilename'][j])
        data.append(cors['name'][j])
        data.append(cors['content'][j])
        datad.append(data)
        
    return render(request,'courses.html',{'curl':curl,'media_url':media_url,'data':datad})

def teacher(request):
    faDetails=list(col.find({'role':"tutor",'status':1}))
    fac=defaultdict(list)
    for sub in faDetails:
        for key in sub:
            fac[key].append(sub[key])
    t=len(faDetails) 
    data=list()
    datad=list()   
    for i in range(t):
        data=[]
        try:
            fDetails=list(prof.find({'email':fac['email'][i]},{'_id':0,'filename':1,'name':1,'lastname':1}))
            f=defaultdict(list)
            for sub in fDetails:
                for key in sub:
                    f[key].append(sub[key])
            data.append(f['filename'][0])
            data.append(f['name'][0])
            data.append(f['lastname'][0])
            datad.append(data)
        except:
            continue
    return render(request,'teacher.html',{'curl':curl,'media_url':media_url,'data':datad})

def about(request):
    countstudent=len(list(col.find({'role':"student"})))
    countteacher=len(list(col.find({'role':"tutor"})))
    countcourse=len(list(cor.find({})))
    countpayment=len(list(pay.find({})))
    return render(request,'about.html',{'curl':curl,'media_url':media_url,'totals':countstudent,'totalt':countteacher,'totalc':countcourse,'totalp':countpayment})

def pricing(request):
    return render(request,'pricing.html',{'curl':curl})

def blog(request):
    blogDetails= list(bog.find({},{'_id':0,'title':1,'content':1,'filename':1}))
    blog=defaultdict(list)
    r=len(blogDetails)
    for sub in blogDetails:
        for key in sub:
            blog[key].append(sub[key]) 
    bloglist1=list()
    bloglist2=list()
    for j in range(r):
        bloglist1=[]            
        bloglist1.append(blog['filename'][j])
        bloglist1.append(blog['title'][j])
        bloglist1.append(blog['content'][j])
        bloglist2.append(bloglist1)
    return render(request,'blog.html',{'curl':curl,'media_url':media_url,'blog':bloglist2})

def contact(request):
    if request.method=="GET":
        return render(request,'contact.html',{'curl':curl})
    else:
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        mes=request.POST.get('message')
        me = "burhanuddin.argalon@gmail.com"
        you = "burhanuddinbootwala6864@gmail.com"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Contact Mail Student Asisted E-Learning"
        msg['From'] = me
        msg['To'] = you

        html = """<html>
                    <head></head>
                    <body>
                        <h1>Welcome to Student Assisted E-Learning</h1>
                        <p>Following details have been sent through contact us!</p>
                        <h2>Name : """+fname+" "+lname+"""</h2>
                        <h2>Email : """+email+"""</h2>
                        <h2>Subject : """+subject+"""</h2>
                        <h2>Message : """+mes+"""</h2>
                        <br>		
                    </body>
                </html>
                """
    
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        s.sendmail(me,you, str(msg)) 
        s.quit() 
        print("mail send to server successfully....")
        me = "burhanuddin.argalon@gmail.com"
        you = email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Contact Mail Student Asisted E-Learning"
        msg['From'] = me
        msg['To'] = you

        html = """<html>
                    <head></head>
                    <body>
                        <h1>Welcome to Student Assisted E-Learning</h1>
                        <p>Following details have been filled by you!</p>
                        <h2>Name : """+fname+" "+lname+"""</h2>
                        <h2>Subject : """+subject+"""</h2>
                        <h2>Message : """+mes+"""</h2>
                        <br>		
                    </body>
                </html>
                """
    
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        s.sendmail(me,you, str(msg)) 
        s.quit() 
        print("mail send to sender successfully....")
        return render(request,'contact.html',{'curl':curl,'output':"Mail Sent Successfully"})
        

def login(request):
    if request.method=="GET":
        return render(request,'login.html',{'curl':curl,'output':''})
    else:
        email=request.POST.get('email')	
        password=request.POST.get('password')
        userDetails1 = list(col.find({'email':email,'password':password},{'_id': 0, 'email': 1,
                 'password': 1, 'role': 1 ,'status':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        try:
            if len(userDetails)>0 and userDetails[3][0]==1 :
                if userDetails[2][0]=="tutor":
                    response=redirect(curl+'Hdgeub7746h/')
                else:
                    response=redirect(curl+'Stdcbrfjr94j/')
                response.set_cookie('cunm',email,3600)
                return response
            else:
                return render(request,'login.html',{'curl':curl,'output':'Invalid Email or Password/Please Verify Your Account'})
        except:
            return render(request,'login.html',{'curl':curl,'output':'Invalid Email or Password'})
 
 
def signups(request):
    if request.method=="GET":
        return render(request,'signups.html',{'curl':curl,'output':''})
    else:
        userDetails=None
        userDetails1=None
        sub=None
        key=None
        email=request.POST.get('email')	
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        try:
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'email': 1,
                    'password': 1, 'role': 1 ,'status':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            if (len(userDetails)>0) :
                return render(request,'signups.html',{'curl':curl,'output':"Email Already exists"})
            else:
                if (password==password1):
                    col.insert_one({"email":email,"password":password,"role":"student","status":0})
                    me = "burhanuddin.argalon@gmail.com"
                    you = email
                    subs.insert_one({'email':email,'status':"Free",'courseopt':[],'amountpaid':"0"})
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = "Verification Mail Student Asisted E-Learning"
                    msg['From'] = me
                    msg['To'] = you

                    html = """<html>
                                <head></head>
                                <body>
                                    <h1>Welcome to Student Assisted E-Learning</h1>
                                    <p>You have successfully registered , please click on the link below to verify your account</p>
                                    <h2>Email : """+email+"""</h2>
                                    <h2>Password : """+str(password)+"""</h2>
                                    <br>
                                    <a href='http://localhost:8000/verify?vemail="""+email+"""' >Click here to verify account</a>		
                                </body>
                            </html>
                            """
                
                    s = smtplib.SMTP('smtp.gmail.com', 587) 
                    s.starttls() 
                    s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
                
                    part2 = MIMEText(html, 'html')

                    msg.attach(part2)
                
                    s.sendmail(me,you, str(msg)) 
                    s.quit() 
                    print("mail send successfully....")
                    return render(request,'signups.html',{'curl':curl,'output1':'Registration successfully done- Check Your Email For Verification'})
                else:
                    return render(request,'signups.html',{'curl':curl,'output':'Passwords Do Not Match'})
        except:
            if (len(userDetails)!=None) :
                return render(request,'signups.html',{'curl':curl,'output':"Email already exists"})
            else:
                if (password==password1):
                    col.insert_one({"email":email,"password":password,"role":"student","status":0})
                    me = "burhanuddin.argalon@gmail.com"
                    you = email

                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = "Verification Mail Student Asisted E-Learning"
                    msg['From'] = me
                    msg['To'] = you

                    html = """<html>
                                <head></head>
                                <body>
                                    <h1>Welcome to Student Assisted E-Learning</h1>
                                    <p>You have successfully registered , please click on the link below to verify your account</p>
                                    <h2>Email : """+email+"""</h2>
                                    <h2>Password : """+str(password)+"""</h2>
                                    <br>
                                    <a href='http://localhost:8000/verify?vemail="""+email+"""' >Click here to verify account</a>		
                                </body>
                            </html>
                            """
                
                    s = smtplib.SMTP('smtp.gmail.com', 587) 
                    s.starttls() 
                    s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
                
                    part2 = MIMEText(html, 'html')

                    msg.attach(part2)
                
                    s.sendmail(me,you, str(msg)) 
                    s.quit() 
                    print("Mail Sent Successfully... ")
                    
                    return render(request,'signups.html',{'curl':curl,'output1':'Registration successfully done- Check Your Email For Verification'})
                else:
                    return render(request,'signups.html',{'curl':curl,'output':'Passwords Do Not Match'})

def verify(request):
    vemail=request.GET.get('vemail')
    col.update_many(
        {"email":vemail},
        {
                "$set":{
                        "status": 1
                        }
                
                  
                }
        )
    return redirect(curl+'login/')	

def signupt(request):
    if request.method=="GET":
        return render(request,'signupt.html',{'curl':curl,'output':''})
    else:
        userDetails=None
        userDetails1=None
        sub=None
        key=None
        email=request.POST.get('email')	
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        try:
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'email': 1,
                    'password': 1, 'role': 1 ,'status':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            if (len(userDetails)>0) :
                return render(request,'signupt.html',{'curl':curl,'output':"Email Already exists"})
            else:
                if (password==password1):
                    col.insert_one({"email":email,"password":password,"role":"tutor","status":0})
                    me = "burhanuddin.argalon@gmail.com"
                    you = email

                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = "Verification Mail Student Asisted E-Learning"
                    msg['From'] = me
                    msg['To'] = you

                    html = """<html>
                                <head></head>
                                <body>
                                    <h1>Welcome to Student Assisted E-Learning</h1>
                                    <p>You have successfully registered , please click on the link below to verify your account</p>
                                    <h2>Email : """+email+"""</h2>
                                    <h2>Password : """+str(password)+"""</h2>
                                    <br>
                                    <a href='http://localhost:8000/verify?vemail="""+email+"""' >Click here to verify account</a>		
                                </body>
                            </html>
                            """
                
                    s = smtplib.SMTP('smtp.gmail.com', 587) 
                    s.starttls() 
                    s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
                
                    part2 = MIMEText(html, 'html')

                    msg.attach(part2)
                
                    s.sendmail(me,you, str(msg)) 
                    s.quit() 
                    print("mail send successfully....")
                    
                    return render(request,'signupt.html',{'curl':curl,'output1':'Registration successfully done- Check Your Email For Verification'})
                else:
                    return render(request,'signupt.html',{'curl':curl,'output':'Passwords Do Not Match'})
        except:
            if (len(userDetails)!=None) :
                return render(request,'signupt.html',{'curl':curl,'output':"Email already exists"})
            else:
                if (password==password1):
                    col.insert_one({"email":email,"password":password,"role":"tutor","status":0})
                    me = "burhanuddin.argalon@gmail.com"
                    you = email

                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = "Verification Mail Student Asisted E-Learning"
                    msg['From'] = me
                    msg['To'] = you

                    html = """<html>
                                <head></head>
                                <body>
                                    <h1>Welcome to Student Assisted E-Learning</h1>
                                    <p>You have successfully registered , please click on the link below to verify your account</p>
                                    <h2>Email : """+email+"""</h2>
                                    <h2>Password : """+str(password)+"""</h2>
                                    <br>
                                    <a href='http://localhost:8000/verify?vemail="""+email+"""' >Click here to verify account</a>		
                                </body>
                            </html>
                            """
                
                    s = smtplib.SMTP('smtp.gmail.com', 587) 
                    s.starttls() 
                    s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
                
                    part2 = MIMEText(html, 'html')

                    msg.attach(part2)
                
                    s.sendmail(me,you, str(msg)) 
                    s.quit() 
                    print("Mail Sent Successfully... ")
                    
                    return render(request,'signupt.html',{'curl':curl,'output1':'Registration successfully done- Check Your Email For Verification'})
                else:
                    return render(request,'signupt.html',{'curl':curl,'output':'Passwords Do Not Match'})

def forget(request):
    if request.method=="GET":
        return render(request,'forget.html',{'curl':curl,'output':''})
    else:
        userDetails=None
        userDetails1=None
        sub=None
        key=None
        email=request.POST.get('email')	
        try:
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'email': 1,
                    'password': 1, 'role': 1 ,'status':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            if (len(userDetails)>0) :
                me = "burhanuddin.argalon@gmail.com"
                you = email

                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Change Password: Student Asisted E-Learning"
                msg['From'] = me
                msg['To'] = you

                html = """<html>
                            <head></head>
                            <body>
                                <h1>Welcome to Student Assisted E-Learning</h1>
                                <p>hello, please click on the link below to change your password</p>
                                <h2>Email : """+email+"""</h2>
                                <br>
                                <h2><a href='http://localhost:8000/changepassword?vemail="""+email+"""' >Click here</a></h2>		
                            </body>
                        </html>
                        """
            
                s = smtplib.SMTP('smtp.gmail.com', 587) 
                s.starttls() 
                s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
            
                part2 = MIMEText(html, 'html')

                msg.attach(part2)
            
                s.sendmail(me,you, str(msg)) 
                s.quit() 
                print("mail sent successfully....")
                response=render(request,'forget.html',{'curl':curl,'output':'Check Your Email'})
                response.set_cookie('email',email,3600)
                return response
                 
            else:
                return render(request,'forget.html',{'curl':curl,'output1':'Please Enter Registered Email'})
        except:
            return render(request,'forget.html',{'curl':curl,'output1':'Please Enter Registered Email'})
        
def changepassword(request):
    vemail=request.GET.get('vemail')
    vemail1=request.COOKIES.get('email')
    
    if request.method=="GET":
        return render(request,'changepassword.html',{'curl':curl,'output1':"Enter New Password For "+str(vemail)})
    else:
        
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        if(password==password1):
            col.update_many(
                {"email":vemail1},
                {
                        "$set":{
                                "password": password
                                }
                        
                        
                        }
                )
            me = "burhanuddin.argalon@gmail.com"
            you = vemail1

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Password Changed: Student Asisted E-Learning"
            msg['From'] = me
            msg['To'] = you

            html = """<html>
                        <head></head>
                        <body>
                            <h1>Welcome to Student Assisted E-Learning</h1>
                            <p>Your Password Was Changed Recently</p>
                            <h2>Email : """+str(vemail1)+"""</h2>
                            <h2>Click Below To Login</h2>
                            <br>
                            <a href='http://localhost:8000/login/ >Click here</a>		
                        </body>
                    </html>
                    """
        
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            s.starttls() 
            s.login('burhanuddin.argalon@gmail.com','oouuushpqytkttok') 
        
            part2 = MIMEText(html, 'html')

            msg.attach(part2)
        
            s.sendmail(me,you, str(msg)) 
            s.quit() 
            print("mail sent successfully....")
            return render(request,'login.html',{'curl':curl,'output1':"Password Changed Successfully: Please Login"})
        else:
            return render(request,'changepassword.html',{'curl':curl,'output':"Passwords Do Not Match"})

def coursecat(request):
    cat=request.GET.get('cat')
    
    courseDetails= list(cor.find({'category':cat},{'_id':0,'name':1,'content':1,'coverfilename':1}))
    course=defaultdict(list)
    t=len(courseDetails)
    for sub in courseDetails:
        for key in sub:
            course[key].append(sub[key]) 
    datad=list()
    data=list()
    for i in range(t):
        data=[]            
        data.append(course['coverfilename'][i])
        data.append(course['name'][i])
        data.append(course['content'][i])
        datad.append(data)
    return render(request,'coursecat.html',{'curl':curl,'cat':cat,'data':datad,'media_url':media_url})
    

