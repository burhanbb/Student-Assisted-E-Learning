from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from . import models
import time
from django.core.mail import send_mail
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymongo
from collections import defaultdict
import time
from django.core.files.storage import FileSystemStorage
from bson import ObjectId
from django.views.decorators.cache import cache_control
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import random
import string


curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL
# Create your views here.
client = pymongo.MongoClient("mongodb+srv://analytics:analytics-password@mfix.m0l9v.mongodb.net/mflix?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["mflix"]
login=db['logins']
col = db["profile"]
cor=db['course']
subs=db['subscription']
res=db['result']
feed=db['feedback']
com=db['comments']
pay=db['payment_id']
bog=db['blog']

def home(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        countstudent=len(list(login.find({'role':"student"})))
        countteacher=len(list(login.find({'role':"tutor"})))
        countcourse=len(list(cor.find({})))
        countpayment=len(list(pay.find({})))
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
        if(request.method=="GET"):
            return render(request,'base1.html',{'curl':curl,'filename':filename,'media_url':media_url,'totals':countstudent,'totalt':countteacher,'totalc':countcourse,'totalp':countpayment,'blog':bloglist2})
    except:
        return render(request,'base1.html',{'curl':curl,'media_url':media_url})

def viewallcat(request):
    cat=request.GET.get('cat')
    email=request.COOKIES.get('cunm')
    userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
    user=defaultdict(list)
    for sub in userDetails1:
        for key in sub:
            user[key].append(sub[key])  
    userDetails=list(user.values())
    filename=userDetails[0][0]
    courseDetails= list(cor.find({'category':cat},{'_id':1,'name':1,'content':1,'coverfilename':1}))
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
        data.append(str(course['_id'][i]))
        datad.append(data)
    return render(request,'viewallcat.html',{'curl':curl,'cat':cat,'data':datad,'media_url':media_url,'filename':filename})

def profile(request):
    email=request.COOKIES.get('cunm')
    name=""
    try:
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'email': 1,
                        'name': 1, 'lastname': 1 ,'mobileno':1,'dob':1,'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        #userDetails=list(user.values())
        name=user['name'][0]
        lastname=user['lastname'][0]
        mobileno=user['mobileno'][0]
        filename=user['filename'][0]
        user1=defaultdict(list)
        for sub in user['dob']:
            for key in sub:
                user1[key].append(sub[key])
        dobday=user1['day'][0]
        dobmon=user1['month'][0]
        doby=user1['year'][0]
        if(request.method=="GET"):
            if(name==""):
                return render(request,'profile.html',{'curl':curl,'media_url':media_url})
            else:
                return render(request,'profile.html',{'curl':curl,'media_url':media_url,'name':name,'lastname':lastname,'mobileno':mobileno,'dobday':dobday,'dobmon':dobmon,'doby':doby,'filename':filename})
        else:
            if(name==""):
                col.insert_one({"email":email})
                try:
                    if(request.POST.get('fname')==""):
                        name1=name
                    else:
                        name1=request.POST.get('fname')
                    if(request.POST.get('lname')==""):
                        lastname1=lastname
                    else:
                        lastname1=request.POST.get('lname')
                    if(request.POST.get('mobile')==""):
                        mobileno1=mobileno
                    else:
                        mobileno1=request.POST.get('mobile')
                    if(request.POST.get('day')==""):
                        dobday1=dobday
                    else:
                        dobday1=request.POST.get('day')
                    if(request.POST.get('mon')==""):
                        dobmon1=dobmon
                    else:
                        dobmon1=request.POST.get('mon')
                    if(request.POST.get('year')==""):
                        doby1=doby
                    else:
                        doby1=request.POST.get('year')
                    
                    
                    try:
                        picon=request.FILES['picon']
                        fs = FileSystemStorage()
                        filename1 = fs.save(picon.name,picon)
                    except:
                        filename1=filename
                    
                    
                    col.update_many(
                        {"email":email},
                        {
                                "$set":{
                                        "name": name1,
                                        "lastname":lastname1,
                                        "mobileno":mobileno1,
                                        "dob":{
                                            "day":dobday1,
                                            "month":dobmon1,
                                            "year":doby1
                                        },
                                        "filename":filename1
                                        }
                                
                                
                                }
                        )
                    
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output':'Please Fill Entire Form'})
            else:
                try:
                    if(request.POST.get('fname')==""):
                        name1=name
                    else:
                        name1=request.POST.get('fname')
                    if(request.POST.get('lname')==""):
                        lastname1=lastname
                    else:
                        lastname1=request.POST.get('lname')
                    if(request.POST.get('mobile')==""):
                        mobileno1=mobileno
                    else:
                        mobileno1=request.POST.get('mobile')
                    if(request.POST.get('day')==""):
                        dobday1=dobday
                    else:
                        dobday1=request.POST.get('day')
                    if(request.POST.get('mon')==""):
                        dobmon1=dobmon
                    else:
                        dobmon1=request.POST.get('mon')
                    if(request.POST.get('year')==""):
                        doby1=doby
                    else:
                        doby1=request.POST.get('year')
                    
                    
                    try:
                        picon=request.FILES['picon']
                        fs = FileSystemStorage()
                        filename1 = fs.save(picon.name,picon)
                    except:
                        filename1=filename
                    
                    
                    col.update_many(
                        {"email":email},
                        {
                                "$set":{
                                        "name": name1,
                                        "lastname":lastname1,
                                        "mobileno":mobileno1,
                                        "dob":{
                                            "day":dobday1,
                                            "month":dobmon1,
                                            "year":doby1
                                        },
                                        "filename":filename1
                                        }
                                
                                
                                }
                        )
                    
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output':'Invalid Input'})
    except:
    

        if(request.method=="GET"):
            if(name==""):
                return render(request,'profile.html',{'curl':curl,'media_url':media_url})
            else:
                return render(request,'profile.html',{'curl':curl,'media_url':media_url,'name':name,'lastname':lastname,'mobileno':mobileno,'dobday':dobday,'dobmon':dobmon,'doby':doby,'filename':filename})
        else:
            if(name==""):
                col.insert_one({"email":email})
                try:
                    if(request.POST.get('fname')==""):
                        name1=name
                    else:
                        name1=request.POST.get('fname')
                    if(request.POST.get('lname')==""):
                        lastname1=lastname
                    else:
                        lastname1=request.POST.get('lname')
                    if(request.POST.get('mobile')==""):
                        mobileno1=mobileno
                    else:
                        mobileno1=request.POST.get('mobile')
                    if(request.POST.get('day')==""):
                        dobday1=dobday
                    else:
                        dobday1=request.POST.get('day')
                    if(request.POST.get('mon')==""):
                        dobmon1=dobmon
                    else:
                        dobmon1=request.POST.get('mon')
                    if(request.POST.get('year')==""):
                        doby1=doby
                    else:
                        doby1=request.POST.get('year')
                    
                    
                    try:
                        picon=request.FILES['picon']
                        fs = FileSystemStorage()
                        filename1 = fs.save(picon.name,picon)
                    except:
                        filename1=filename
                    
                    
                    col.update_many(
                        {"email":email},
                        {
                                "$set":{
                                        "name": name1,
                                        "lastname":lastname1,
                                        "mobileno":mobileno1,
                                        "dob":{
                                            "day":dobday1,
                                            "month":dobmon1,
                                            "year":doby1
                                        },
                                        "filename":filename1
                                        }
                                
                                
                                }
                        )
                    
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output':'Please Fill Entire Form'})
            else:
                try:
                    if(request.POST.get('fname')==""):
                        name1=name
                    else:
                        name1=request.POST.get('fname')
                    if(request.POST.get('lname')==""):
                        lastname1=lastname
                    else:
                        lastname1=request.POST.get('lname')
                    if(request.POST.get('mobile')==""):
                        mobileno1=mobileno
                    else:
                        mobileno1=request.POST.get('mobile')
                    if(request.POST.get('day')==""):
                        dobday1=dobday
                    else:
                        dobday1=request.POST.get('day')
                    if(request.POST.get('mon')==""):
                        dobmon1=dobmon
                    else:
                        dobmon1=request.POST.get('mon')
                    if(request.POST.get('year')==""):
                        doby1=doby
                    else:
                        doby1=request.POST.get('year')
                    
                    
                    try:
                        picon=request.FILES['picon']
                        fs = FileSystemStorage()
                        filename1 = fs.save(picon.name,picon)
                    except:
                        filename1=filename
                    
                    
                    col.update_many(
                        {"email":email},
                        {
                                "$set":{
                                        "name": name1,
                                        "lastname":lastname1,
                                        "mobileno":mobileno1,
                                        "dob":{
                                            "day":dobday1,
                                            "month":dobmon1,
                                            "year":doby1
                                        },
                                        "filename":filename1
                                        }
                                
                                
                                }
                        )
                    
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile.html',{'curl':curl,'media_url':media_url,'output':'Invalid Input'})

def viewall(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        corDetails=list(cor.find({},{'_id':1,'name':1,'content':1,'coverfilename':1}))
        core=defaultdict(list)
        for sub in corDetails:
            for key in sub:
                core[key].append(sub[key])
        l=len(corDetails)
        data=list()
        datad=list()
        for i in range(l):
            data=[]
            data.append(core['_id'][i])
            data.append(core['name'][i])
            data.append(core['content'][i])
            data.append(core['coverfilename'][i])
            datad.append(data)
        return render(request,'viewall.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad})
    except:
        return render(request,'viewall.html',{'curl':curl,'media_url':media_url})

def checkenroll(request):
    uid=request.GET.get('uid')
    email=request.COOKIES.get('cunm')
    subDetails=list(subs.find({'email':email},{'_id':0,'status':1,'courseopt':1}))
    subb=defaultdict(list)
    for sub in subDetails:
        for key in sub:
            subb[key].append(sub[key])
    copt=subb['courseopt'][0]
    l=len(copt)
    if(subb['status'][0]=="Free"):
        response=redirect(curl+'Stdcbrfjr94j/subscribe?output=Please+Select+A+Plan+First')
        return response
    elif(subb['status'][0]=="Silver" and l>=5):
        response=redirect(curl+'Stdcbrfjr94j/subscribe?output=Please+Upgrade+Your+Plan')
        return response
    elif(subb['status'][0]=="Gold" and l>=20):
        response=redirect(curl+'Stdcbrfjr94j/subscribe?output=Please+Upgrade+Your+Plan')
        return response
    else:
        flag=0
        for dat in copt:
            if(dat==uid):
                flag=1
        if flag==1:
            response=redirect(curl+'Stdcbrfjr94j/viewcourse?uid='+uid)
            return response
        else:
            subs.update_many({'email':email},{
                "$push":{ "courseopt": uid }
                })
            res.insert_one({"email":email,"course_id":uid,"result":[] })
            corDetails=list(cor.find({'_id':ObjectId(uid)}))
            core=defaultdict(list)
            for sub in corDetails:
                for key in sub:
                    core[key].append(sub[key])
            me = "burhanuddin.argalon@gmail.com"
            you = email

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Course Enrolled Successfully: Student Assisted E-Learning"
            msg['From'] = me
            msg['To'] = you

            html = """<html>
                        <head></head>
                        <body>
                            <h1>Welcome to Student Assisted E-Learning</h1>
                            <p>---------------------------------------------</p>
                            <h2>Thanks for subscribing : """+core['name'][0]+""" </h2>
                            <h2> Click below to login and start learning the course! </h2>
                            <br>
                            <h2><a href='http://localhost:8000/login/ >Click here</a></h2>		
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
            print("payment mail sent successfully....")
            response=redirect(curl+'Stdcbrfjr94j/viewdet?uid='+uid)
            return response

def subscribe(request):
    try:
        email=request.COOKIES.get('cunm')
        output=request.GET.get('output')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        PAYPAL_ID='sb-mj98r6348768@business.example.com'
        PAYPAL_URL='https://www.sandbox.paypal.com/cgi-bin/webscr'
        subDetails=list(subs.find({'email':email},{'_id':0,'status':1}))
        subc=defaultdict(list)
        for sub in subDetails:
            for key in sub:
                subc[key].append(sub[key])
        if(request.method=="GET"):
            return render(request,'subscribe.html',{'curl':curl,'filename':filename,'media_url':media_url,'output':output,"PAYPAL_ID":PAYPAL_ID,'PAYPAL_URL':PAYPAL_URL,'plan':subc['status'][0]})
            
    except:
        return render(request,'subscribe.html',{'curl':curl,'media_url':media_url})

def payment(request):
    poid=request.GET.get('pid')
    price=request.GET.get('price')
    email=request.COOKIES.get('cunm')
    dt=time.asctime(time.localtime(time.time()))
    pay.insert_one({"email":email,"product_id":poid,"price":price,"date":dt })
    stat="Free"
    if poid=="1":
        stat="Silver"
    elif poid=="2":
        stat="Gold"
    elif poid=="3":
        stat="Platinum"
    else:
        stat="Free"
    subs.update_many({'email':email},{
                "$set":{ "amountpaid": price , "status": stat }
                })
    me = "burhanuddin.argalon@gmail.com"
    you = email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Payment Successful: Student Assisted E-Learning"
    msg['From'] = me
    msg['To'] = you

    html = """<html>
                <head></head>
                <body>
                    <h1>Welcome to Student Assisted E-Learning</h1>
                    <p>---------------------------------------------</p>
                    <h2>Thanks for subscribing : """+stat+""" Plan </h2>
                    <h2>Amount Paid : &#x20B9;"""+price+""" </h2>
                    <h2> Click below to login and start exploring our courses! </h2>
                    <br>
                    <h2><a href='http://localhost:8000/login/ >Click here</a></h2>		
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
    print("payment mail sent successfully....")
    
    response=redirect(curl+"Stdcbrfjr94j/success?pid="+poid+"&&price="+price)
    return response

def success(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        pid=str(request.GET.get('pid'))
        price=request.GET.get('price')
        if pid=="1":
            plan="Silver"
        elif pid=="2":
            plan="Gold"
        elif pid=="3":
            plan="Platinum"
        else:
            plan="Free"
        if(request.method=="GET"):
            return render(request,'success.html',{'curl':curl,'filename':filename,'media_url':media_url,'plan':plan,'price':price})
    except:
        return render(request,'success.html',{'curl':curl,'media_url':media_url})

def cancel(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        if(request.method=="GET"):
            return render(request,'cancel.html',{'curl':curl,'filename':filename,'media_url':media_url})
    except:
        return render(request,'cancel.html',{'curl':curl,'media_url':media_url})
    
def viewdet(request):
    try:
        email=request.COOKIES.get('cunm')
        uid=request.GET.get('uid')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        cor_id=ObjectId(uid)
        corDetails1 = list(cor.find({'_id':cor_id},{'_id': 1,'name':1,'content':1,'category':1,'subcategory':1,'filename':1}))
        core=defaultdict(list)
        for sub in corDetails1:
            for key in sub:
                core[key].append(sub[key])
        data=list()
        datad=list()
        data.append(core['_id'][0])
        data.append(core['name'][0])
        data.append(core['content'][0])
        data.append(core['category'][0])
        data.append(core['subcategory'][0])
        data.append(core['filename'][0])
        datad.append(data)
        if(request.method=="GET"):
            return render(request,'viewdet.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,'uid':uid})
    except:
        return render(request,'viewdet.html',{'curl':curl,'media_url':media_url})

def quizpage(request):
    try:
        try:
            output=request.GET.get('output')
        except:
            output="Select The Answer"
        uid=request.GET.get('uid')
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        cor_id=ObjectId(uid)
        corDetails1 = list(cor.find({'_id':cor_id},{'_id': 0, 'quiz':1}))
        core=defaultdict(list)
        for sub in corDetails1:
            for key in sub:
                core[key].append(sub[key])
        data=list()
        datad=list()
        ques=core['quiz'][0]['question']['question']
        for i in range(4):
            data=[]
            d='option'+str(i+1)
            data.append(core['quiz'][0]['question'][d])
            data.append(d)
            datad.append(data)
        if(request.method=="GET"):
            return render(request,'quizpage.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,'uid':uid,'ques':ques,'output':output})
    except:
        return render(request,'quizpage.html',{'curl':curl,'media_url':media_url})

def checkanswer(request):
    uid=request.GET.get('uid')
    selection=request.GET.get('selection')
    
    email=request.COOKIES.get('cunm')
    cor_id=ObjectId(uid)
    corDetails1 = list(cor.find({'_id':cor_id},{'_id': 0, 'quiz':1}))
    core=defaultdict(list)
    for sub in corDetails1:
        for key in sub:
            core[key].append(sub[key])
    if core['quiz'][0]['question']['answer']==selection:
        res.update_many({'email':email,'course_id':uid},{
                "$push":{ "result": 1 }
                })
        response=redirect(curl+'Stdcbrfjr94j/giveFeedback?uid='+uid)
        return response
    else:
        res.update_many({'email':email,'course_id':uid},{
                "$push":{ "result": 0 }
                })
        response=redirect(curl+'Stdcbrfjr94j/quizpage?uid='+uid+'&&output=Wrong Answer, Please Try Again')
        return response

def giveFeedback(request):
    try:
        uid=request.GET.get('uid')
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        if(request.method=="GET"):
            return render(request,'giveFeedback.html',{'curl':curl,'filename':filename,'media_url':media_url,'uid':uid})
        else:
            review=request.POST.get('cname')
            rating=request.POST.get('cat')
            feed.insert_one({"email":email,"course_id":uid,"review":review,"rating":str(rating) })
            response=redirect(curl+'Stdcbrfjr94j/mycor')
            return response
    except:
        return render(request,'giveFeedback.html',{'curl':curl,'media_url':media_url})

def mycor(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        try:
            subDetails1 = list(subs.find({'email':email},{'_id': 0, 'courseopt':1}))
            subc=defaultdict(list)
            for sub in subDetails1:
                for key in sub:
                    subc[key].append(sub[key])
            r=len(subc['courseopt'][0])
            datad=list()
            for i in range(r):
                uid=subc['courseopt'][0][i]
                cor_id=ObjectId(uid)
                corDetails1 = list(cor.find({'_id':cor_id},{'_id': 0, 'name': 1,
                            'content': 1,'coverfilename':1}))
                core=defaultdict(list)
                for sub in corDetails1:
                    for key in sub:
                        core[key].append(sub[key])
                data=list()  
                data.append(uid)         
                data.append(core['name'][0])
                data.append(core['content'][0])
                data.append(core['coverfilename'][0])
                datad.append(data)
        except:
                datad=[]
            
        if(request.method=="GET"):
            return render(request,'mycor.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad})
    except:
        return render(request,'mycor.html',{'curl':curl,'media_url':media_url})
    
def viewcourse(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        cor_id=request.GET.get('uid')
        cors=ObjectId(cor_id)
        courseDetails= list(cor.find({'_id':cors},{'_id': 0, 'name': 1,
                        'content': 1, 'category': 1,'subcategory':1 ,'filename':1}))
        course=defaultdict(list)
        t=len(courseDetails)
        
        for sub in courseDetails:
            for key in sub:
                course[key].append(sub[key]) 
        datad=list()
        data=list()
        for i in range(t):
            data=[]            
            data.append(course['filename'][i])
            data.append(course['name'][i])
            data.append(course['content'][i])
            data.append(course['category'][i])
            data.append(course['subcategory'][i])
            datad.append(data)
        try:
            comDetails=list(com.find({'course_id':cor_id},{'_id': 1, 'email': 1,
                        'comment': 1, 'filename': 1}))
            come=defaultdict(list)
            l=len(comDetails)
            output1=""
            if l==0:
                output1="No Comments Found"
        
            for sub in comDetails:
                for key in sub:
                    come[key].append(sub[key])
            
            comments=list()
            commentsd=list()
            for i in range(l): 
                comments=list()           
                comments.append(come['_id'][i])
                comments.append(come['email'][i])
                comments.append(come['comment'][i])
                comments.append(come['filename'][i])
                commentsd.append(comments)
            output=request.GET.get('output')
            if output==None:
                output=""
        except:
            output="No Comments Found"
        if(request.method=="GET"):
            return render(request,'viewcourse.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,'comments':commentsd,'output':output,'uid':cor_id,'output1':output1})
        else:
            comm=request.POST.get('cname')
            try:
                video=request.FILES['video']
                fv = FileSystemStorage()
                filev = fv.save(video.name,video)
            except:
                filev=''
            com.insert_one({'email':email,'course_id':cor_id,'comment':comm,'filename':filev})
            response=redirect(curl+'Stdcbrfjr94j/viewcourse?uid='+cor_id+'&&output=SUCCESS')
            return response
    except:
        return render(request,'viewcourse.html',{'curl':curl,'media_url':media_url})
    
def checkquiz(request):
    uid=request.GET.get('uid')
    email=request.COOKIES.get('cunm')
    resDetails=list(res.find({'email':email,'course_id':uid},{'_id':0,'result':1}))
    resl=defaultdict(list)
    for sub in resDetails:
        for key in sub:
            resl[key].append(sub[key])
    arr=resl['result'][0]
    l=len(arr)
    for i in range(l):
        if(arr[i]==1):
            response=redirect(curl+'Stdcbrfjr94j/landingquizpage?uid='+uid)
            return response
    response=redirect(curl+'Stdcbrfjr94j/quizpage?uid='+uid)
    return response

def landingquizpage(request):     
    try:
        uid=request.GET.get('uid')
        email=request.COOKIES.get('cunm')
        if(request.method=="GET"):
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            filename=userDetails[0][0]
            return render(request,'landingquizpage.html',{'curl':curl,'filename':filename,'media_url':media_url,'uid':uid})
    except:
        return render(request,'landingquizpage.html',{'curl':curl,'media_url':media_url}) 

def piechart(arr1):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    a=0
    b=0
    c=0
    f=0
    for i in arr1:
        if i[3]=='A':
            a+=1
        elif i[3]=='B':
            b+=1
        elif i[3]=='C':
            c+=1
        else:
            f+=1
        
    labels = 'A','B','C','F'
    sizes = [a,b,c,f]
    explode = (0.1, 0,0.1,0) 
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ran = ''.join(random.choices(string.digits + string.ascii_letters, k = 15)) 
    plt.savefig('media/'+ran+'.png',dpi=100)
    return ran
    
def performance(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        resDetails=list(res.find({'email':email},{'_id':0,'result':1,'course_id':1}))
        resl=defaultdict(list)
        for sub in resDetails:
            for key in sub:
                resl[key].append(sub[key])
        p=len(resDetails)
        data=list()
        datad=list()
        for m in range(p):
            data=[]
            grade=""
            r=len(resl['result'][m])
            if(r==1):
                grade="A"
            elif(r==2):
                grade="B"
            elif(r==3):
                grade="C"
            else:
                grade="F"
            
            cors=ObjectId(resl['course_id'][m])
            courseDetails= list(cor.find({'_id':cors},{'_id': 0, 'name': 1,'coverfilename':1}))
            course=defaultdict(list)
            for sub in courseDetails:
                for key in sub:
                    course[key].append(sub[key])
            data.append(resl['course_id'][m])
            data.append(course['name'][0])
            data.append(course['coverfilename'][0])
            data.append(grade)
            datad.append(data)
            
        pic=piechart(datad)
        pic1=pic+'.png'
        if(request.method=="GET"):
            return render(request,'performance.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,'pic':pic1})
    except:
        return render(request,'performance.html',{'curl':curl,'media_url':media_url})

    