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

curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL
# Create your views here.
client = pymongo.MongoClient("mongodb+srv://analytics:analytics-password@mfix.m0l9v.mongodb.net/mflix?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client["mflix"]
login=db['logins']
col = db["profile"]
cor = db["course"]
bog=db["blog"]
feed=db["feedback"]
com=db['comments']
pay=db['payment_id']

def home(request):
    try:
        email=request.COOKIES.get('cunm')
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
        countstudent=len(list(login.find({'role':"student"})))
        countteacher=len(list(login.find({'role':"tutor"})))
        countcourse=len(list(cor.find({})))
        countpayment=len(list(pay.find({})))
        if(request.method=="GET"):
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            filename=userDetails[0][0]
            return render(request,'base.html',{'curl':curl,'filename':filename,'media_url':media_url,'blog':bloglist2,'totals':countstudent,'totalt':countteacher,'totalc':countcourse,'totalp':countpayment})
    except:
        return render(request,'base.html',{'curl':curl,'media_url':media_url})

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
                return render(request,'profile1.html',{'curl':curl,'media_url':media_url})
            else:
                return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'name':name,'lastname':lastname,'mobileno':mobileno,'dobday':dobday,'dobmon':dobmon,'doby':doby,'filename':filename})
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
                    
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output':'Please Fill Entire Form'})
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
                    
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output':'Invalid Input'})
    except:
    

        if(request.method=="GET"):
            if(name==""):
                return render(request,'profile1.html',{'curl':curl,'media_url':media_url})
            else:
                return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'name':name,'lastname':lastname,'mobileno':mobileno,'dobday':dobday,'dobmon':dobmon,'doby':doby,'filename':filename})
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
                    
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output':'Please Fill Entire Form'})
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
                    
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output1':'Successfully Changed','filename':filename1,'name':name1,'lastname':lastname1,'mobileno':mobileno1,'dobday':dobday1,'dobmon':dobmon1,'doby':doby1,})
                except:
                    return render(request,'profile1.html',{'curl':curl,'media_url':media_url,'output':'Invalid Input'})

def mycourse(request):
    try:
        k=0
        grt=[]
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        courseDetails= list(cor.find({'email':email},{'_id': 1, 'name': 1,
                        'content': 1, 'coverfilename': 1 ,}))
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
            grt.append(str(course['_id'][i]))
            k+=1
            datad.append(data)
        if(request.method=="GET"):
            return render(request,'mycourse.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad})
        else:
            for d in range(k):
                try:
                    c=request.POST.get(grt[d])
                    if(c!=None):
                        f=ObjectId(c)
                        cor.delete_one({'_id':f})
                    else:
                        continue
                except: 
                    continue
            return render(request,'mycourse.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,"output1":"Deleted Course Successfully, Please Refresh."})
    except:
        return render(request,'mycourse.html',{'curl':curl,'media_url':media_url})

def addcourse(request):
    try:
        email=request.COOKIES.get('cunm')
        if(request.method=="GET"):
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            filename=userDetails[0][0]
            return render(request,'addcourse.html',{'curl':curl,'filename':filename,'media_url':media_url})
        else:
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            filename=userDetails[0][0]
            cname=request.POST.get('cname')
            message=request.POST.get('message')
            cat=request.POST.get('cat')
            subcat=request.POST.get('subcat')
            question=request.POST.get('ques')
            o1=request.POST.get('o1')
            o2=request.POST.get('o2')
            o3=request.POST.get('o3')
            o4=request.POST.get('o4')
            answer=request.POST.get('answer')
            picon=request.FILES['picon']
            fs = FileSystemStorage()
            cover = fs.save(picon.name,picon)
            
            video=request.FILES['video']
            fv = FileSystemStorage()
            filev = fv.save(video.name,video)
            cor.insert_one({"email":email,"name":cname,"content":message,"category":cat,"subcategory":subcat,"quiz":{ "question":{ "question":question,"option1":o1,"option2":o2,"option3":o3,"option4":o4,"answer":answer}},"filename":filev,"coverfilename":cover})  
            return render(request,'addcourse.html',{'curl':curl,'media_url':media_url,'filename':filename,"output1":"Successfully Added!"})      
    except:
        return render(request,'addcourse.html',{'curl':curl,'media_url':media_url,"output":"Please Check Your Entries Again."})

def editcourse(request):
    try:
        
        email=request.COOKIES.get('cunm')
        userDetails2= list(cor.find({'email':email},{'_id': 0, 'name':1}))
        user1=defaultdict(list)
        l=len(userDetails2)
        for i in range(l):
            for sub in userDetails2:
                for key in sub:
                    user1[key].append(sub[key])
        datad=list()
        data=list()
        for i in range(l):
            data=[]            
            data.append(user1['name'][i])
            datad.append(data)
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        uid=request.GET.get('uid')
        cor_id=ObjectId(uid)
        corDetails1 = list(cor.find({'_id':cor_id},{'_id': 0, 'name':1}))
        core=defaultdict(list)
        for sub in corDetails1:
            for key in sub:
                core[key].append(sub[key])  
        corname=core['name'][0]
        if(request.method=="GET"):
            return render(request,'editcourse.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,'uid':uid,'name':corname})
        else:
            coursedetails = list(cor.find({'name':corname,'email':email},{'_id': 0,'name':1,'content':1,'category':1,'subcategory':1,'coverfilename':1,'filename':1,'quiz':1}))
            course=defaultdict(list)
            for sub in coursedetails:
                for key in sub:
                    course[key].append(sub[key])  
            course1=defaultdict(list)
            for sub in course['quiz']:
                for key in sub:
                    course1[key].append(sub[key])
            course2=defaultdict(list)
            for sub in course1['question']:
                for key in sub:
                    course2[key].append(sub[key])
            
            
            if(request.POST.get('cname')==""):
                name=course['name'][0]
            else:
                name=request.POST.get('cname')
            if(request.POST.get('message')==""):
                message=course['content'][0]
            else:
                message=request.POST.get('message')
            if(request.POST.get('cat')==""):
                cat=course['category'][0]
            else:
                cat=request.POST.get('cat')
            if(request.POST.get('subcat')==""):
                subcat=course['subcategory'][0]
            else:
                subcat=request.POST.get('subcat')
            if(request.POST.get('ques')==""):
                ques=course2['question'][0]
            else:
                ques=request.POST.get('ques')
            if(request.POST.get('o1')==""):
                option1=course2['option1'][0]
            else:
                option1=request.POST.get('o1')
            if(request.POST.get('o2')==""):
                option2=course2['option2'][0]
            else:
                option2=request.POST.get('o2')
            if(request.POST.get('o3')==""):
                option3=course2['option3'][0]
            else:
                option3=request.POST.get('o3')
            if(request.POST.get('o4')==""):
                option4=course2['option4'][0]
            else:
                option4=request.POST.get('o4')
            if(request.POST.get('answer')==""):
                answer=course2['answer'][0]
            else:
                answer=request.POST.get('answer')
            try:
                picon=request.FILES['picon']
                fs = FileSystemStorage()
                cover = fs.save(picon.name,picon)
            except:
                cover=course['coverfilename'][0]
            
            try:
                video=request.FILES['video']
                fv = FileSystemStorage()
                filev = fv.save(video.name,video)
            except:
                filev=course['filename'][0]
            cor.update_many(
                        {"email":email,'name':corname},
                        {
                                "$set":{
                                        "name": name,
                                        "content":message,
                                        "category":cat,
                                        "subcategory":subcat,
                                        "quiz":{ "question":
                                            {
                                            "question":ques,
                                            "option1":option1,
                                            "option2":option2,
                                            "option3":option3,
                                            "option4":option4,
                                            "answer":answer
                                        } },
                                        "filename":filev,
                                        "coverfilename":cover
                                        }
                                
                                
                                }
                        )
            return render(request,'editcourse.html',{'curl':curl,'media_url':media_url,'filename':filename,"output1":"Successfully Updated!",'data':datad})
    except:
        return render(request,'editcourse.html',{'curl':curl,'media_url':media_url,"output":"Select Your Entries!"})
    
def blogs(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        blogDetails= list(bog.find({'email':email},{'_id': 1, 'title': 1,
                        'content': 1, 'filename': 1 ,}))
        blog=defaultdict(list)
        t=len(blogDetails)
        for i in range(t):
            for sub in blogDetails:
                for key in sub:
                    blog[key].append(sub[key]) 
        datad=list()
        data=list()
        grt=[]
        k=0
        for i in range(t):
            data=[]            
            data.append(blog['filename'][i])
            data.append(blog['title'][i])
            data.append(blog['content'][i])
            data.append(str(blog['_id'][i]))
            grt.append(str(blog['_id'][i]))
            k+=1
            datad.append(data)
        if(request.method=="GET"):
            return render(request,'blogtu.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad})
        else:
            for d in range(k):
                try:
                    c=request.POST.get(grt[d])
                    if(c!=None):
                        f=ObjectId(c)
                        bog.delete_one({'_id':f})
                    else:
                        continue
                except: 
                    continue
            return render(request,'blogtu.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,"output1":"Deleted Blog(s) Successfully"})
    except:
        return render(request,'blogtu.html',{'curl':curl,'media_url':media_url})

def addblog(request):
    try:
        email=request.COOKIES.get('cunm')
        if(request.method=="GET"):
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            filename=userDetails[0][0]
            return render(request,'addblog.html',{'curl':curl,'filename':filename,'media_url':media_url})
        else:
            userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
            user=defaultdict(list)
            for sub in userDetails1:
                for key in sub:
                    user[key].append(sub[key])  
            userDetails=list(user.values())
            filename=userDetails[0][0]
            cname=request.POST.get('cname')
            message=request.POST.get('message')
            cat=request.POST.get('cat')
            picon=request.FILES['picon']
            fs = FileSystemStorage()
            cover = fs.save(picon.name,picon)
            bog.insert_one({"email":email,"title":cname,"content":message,"category":cat,"filename":cover})  
            return render(request,'addblog.html',{'curl':curl,'media_url':media_url,'filename':filename,"output1":"Successfully Added!"})      
    except:
        return render(request,'addblog.html',{'curl':curl,'media_url':media_url,"output":"Please Check Your Entries Again."})
    
def editblog(request):
    try:
        email=request.COOKIES.get('cunm')
        userDetails2= list(bog.find({'email':email},{'_id': 0, 'title':1}))
        user1=defaultdict(list)
        l=len(userDetails2)
        for i in range(l):
            for sub in userDetails2:
                for key in sub:
                    user1[key].append(sub[key])
        datad=list()
        data=list()
        for i in range(l):
            data=[]            
            data.append(user1['title'][i])
            datad.append(data)
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        if(request.method=="GET"):
            return render(request,'editblog.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad})
        else:
            bogname=request.POST.get('bogname')
            coursedetails = list(bog.find({'title':bogname,'email':email},{'_id': 0,'title':1,'content':1,'category':1,'filename':1,}))
            course=defaultdict(list)
            for sub in coursedetails:
                for key in sub:
                    course[key].append(sub[key])
            if(request.POST.get('cname')==""):
                name=course['title'][0]
            else:
                name=request.POST.get('cname')
            if(request.POST.get('message')==""):
                message=course['content'][0]
            else:
                message=request.POST.get('message')
            if(request.POST.get('cat')==""):
                cat=course['category'][0]
            else:
                cat=request.POST.get('cat')
            try:
                picon=request.FILES['picon']
                fs = FileSystemStorage()
                cover = fs.save(picon.name,picon)
            except:
                cover=course['filename'][0]
        
            bog.update_many(
                        {"email":email,'title':bogname},
                        {
                                "$set":{
                                        "title": name,
                                        "content":message,
                                        "category":cat,
                                        "filename":cover,
                                        }
                                
                                
                                }
                        )
            return render(request,'editblog.html',{'curl':curl,'media_url':media_url,'filename':filename,"output1":"Successfully Updated!",'data':datad})
    except:
        return render(request,'editblog.html',{'curl':curl,'media_url':media_url,'filename':filename,"output":"Select Your Entries!"})

def feedback(request):
    try:
        k=0
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        courseDetails=list(cor.find({'email':email},{'_id':1}))
        course=defaultdict(list)
        for sub in courseDetails:
            for key in sub:
                course[key].append(sub[key])
        datad=list()
        data=list()
        grt=list()
        t=len(courseDetails)
        for i in range(t):
            data=[]
            idf=str(course['_id'][i])
            try:
                feedDetails= list(feed.find({'course_id':idf},{'_id': 1,'review':1,'rating':1,'email':1,'course_id':1}))
                r=len(feedDetails)
                feedback=defaultdict(list)
                for sub in feedDetails:
                    for key in sub:
                        feedback[key].append(sub[key])
                for j in range(r):
                    data=[]
                    data.append(feedback['review'][j])
                    data.append(feedback['rating'][j])
                    userd=list(col.find({'email':feedback['email'][j]},{'_id':0,'filename':1,'name':1,'lastname':1}))
                    userdd=defaultdict(list)
                    for sub in userd:
                        for key in sub:
                            userdd[key].append(sub[key])
                    data.append(userdd['filename'][0])
                    data.append(userdd['name'][0])
                    data.append(userdd['lastname'][0])
                    coid=ObjectId(feedback['course_id'][j])
                    coursed=list(cor.find({'_id':coid},{'_id':0,'name':1}))
                    coursedd=defaultdict(list)
                    for sub in coursed:
                        for key in sub:
                            coursedd[key].append(sub[key])
                    data.append(coursedd['name'][0])
                    data.append(str(feedback['_id'][j]))
                    datad.append(data)
                grt.append(str(feedback['_id'][0]))
                k+=1
            except:
                continue        
        if(request.method=="GET"):
            return render(request,'feedback.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad})
        else:
            for d in range(k):
                try:
                    c=request.POST.get(grt[d])
                    if(c!=None):
                        f=ObjectId(c)
                        feed.delete_one({'_id':f})
                    else:
                        continue
                except: 
                    continue
            return render(request,'feedback.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,"output1":"Deleted Feedback Successfully"})
    except:
        return render(request,'feedback.html',{'curl':curl,'media_url':media_url,"output":"No Feedbacks Found"})
    
def comments(request):
    try:
        
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        courseDetails= list(cor.find({'email':email},{'_id': 1, 'name': 1,
                        'content': 1, 'coverfilename': 1 ,}))
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
        if(request.method=="GET"):
            return render(request,'comments.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad})
        else:
            o=request.POST.get('close')
            response=redirect(curl+'Hdgeub7746h/coursepage')
            response.set_cookie('cunm',email,3600)
            response.set_cookie('cor_id',o,3600)
            return response
    except:
        return render(request,'comments.html',{'curl':curl,'media_url':media_url})
    
def coursepage(request):
    try:
        k=0
        grt=list()
        email=request.COOKIES.get('cunm')
        userDetails1 = list(col.find({'email':email},{'_id': 0, 'filename':1}))
        user=defaultdict(list)
        for sub in userDetails1:
            for key in sub:
                user[key].append(sub[key])  
        userDetails=list(user.values())
        filename=userDetails[0][0]
        cor_id=request.GET.get('uid')
       # cor_id=request.POST.get('uid')
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
                grt.append(str(come['_id'][k]))
                k+=1
                commentsd.append(comments)
            output=''
        except:
            output="No Comments Found"
        if(request.method=="GET"):
            return render(request,'coursepage.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,'comments':commentsd,'output':output,'uid':cor_id})
        else:
            for d in range(k):
                try:
                    c=request.POST.get(grt[d])
                    if(c!=None):
                        f=ObjectId(c)
                        com.delete_one({'_id':f})
                    else:
                        continue
                except: 
                    continue
            return render(request,'coursepage.html',{'curl':curl,'filename':filename,'media_url':media_url,'data':datad,'comments':commentsd,'output1':"Deleted Successfully- Please Refresh"})
    except:
        return render(request,'coursepage.html',{'curl':curl,'media_url':media_url})