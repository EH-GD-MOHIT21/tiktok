from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from vidshower.models import usermodellikedvideoslist as umlv
from random import choice
import smtplib
from email.message import EmailMessage
from django.contrib import messages
# Create your views here.

def loginPage(request):
    return render(request,'login.html')


@csrf_exempt
def canlog(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(username=username,password=password)
        if user is None:
            messages.info(request,'Invalid Credentials...')
            return redirect('/login')    #### throw error

        else:
            login(request,user)
            return redirect('/')
    else:
        return redirect('/login')


def generateStrongPassword():
    digits = [i for i in range(10)]
    chars = [chr(i) for i in range(65,91)]
    CHARS = [chr(i) for i in range(97,123)]
    passlength = choice([12,13,15,17,16,18])
    password = ''
    for i in range(passlength):
        field = choice([digits,chars,CHARS])
        password += str(choice(field))
    return password



@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        emailid = request.POST['email']
        if len(username)<3 or len(emailid) < 5 :
            messages.info(request,'Invalid credentials...')
            return redirect('/login')
        password = generateStrongPassword()
        if len(User.objects.filter(username=username)) or len(User.objects.filter(email=emailid)):
            messages.info(request,"Sorry but user already exists")
            return redirect('/login')
        
        ########## verification here
        try:
            user = User(username=username,email=emailid)
            user.set_password(password)
            user.save()
            lmv = umlv(user=user)
            lmv.save()
            send_mail(emailid,password,username)
            messages.info(request,'Your Login Credentials is mailed to you please use them.')

        except Exception as e:
            print(e)
            pass

        return redirect('/login')
    else:
        return redirect('/login')


def send_mail(to, personalcode,username):
    # logic to send mail to user
    sender_mail = "no.reply.python.py@gmail.com"
    password_sender = "qwerty@123"
    message = EmailMessage()
    message['To'] = to
    message['From'] = sender_mail
    message['Subject'] = "Welcome User to NestedTikTok.com"
    message.set_content(f"Hello User welcome to NestedTikTok.com Your Username is {username}\n Your Password is\n {personalcode} \n Please Login using the Password Thanks For support 🙏🙏\n Regards\n NestedTikTok.com")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_mail, password_sender)
        server.send_message(message)
        return True         # success
    except:
        return False        # failure