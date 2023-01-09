from email import message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
import re

def register(request):
    message = []
    context = {
        'messages' : message
    }
    if request.method == 'POST' :
        newusername = request.POST['newusername']
        mobile = request.POST['Mobile']
        emai_l = request.POST['Email']
        pas = request.POST['Password']
        confirmPassword = request.POST['ConfirmPassword']
        if User.objects.filter(username = newusername).exists() :
            message.append("Username already  Exists")
        elif mobile.isnumeric() == False or len(mobile) != 10 :
            message.append("Enter a valid Mobile number")
        elif  User.objects.filter(email = emai_l).exists():
            message.append("Email is already register")
        elif pas != confirmPassword :
            message.append("Confirmed Password did not match the entered Password")
        elif (len(pas) < 8):
            message.append("Password should contain atleast 8 characters")
        elif not re.search("[a-z]", pas):
            message.append("Password should contain atleast one Lowercase letter")
        elif not re.search("[A-Z]", pas):
            message.append("Password should contain atleast one Uppercase letter")
        elif not re.search("[0-9]", pas):
            message.append("Password should contain atleast one Number")
        elif not re.search("[_@!#%$]", pas):
            message.append("Password should contain atleast one Special character")
        else :
            message.append("New User created Succesfully")
            User.objects.create_user(username=newusername,password=pas,email=emai_l)
    return render(request, 'myapp/register.html', context)


def login(request):
    message=[]
    context = {
        'messages' : message
    }  
    if request.method == 'POST' :
        newusername = request.POST['newusernameL']
        pas = request.POST['PasswordL']
        if authenticate(request,username=newusername,password=pas) != None :
            message.append("Logged in successfully")
            return render(request, 'myapp/mainpage.html', context)
        else:
            message.append("Invalid Credentials")
    return render(request, 'myapp/login.html', context)


def mainpage(request):
    message=[]
    context = {
        'messages' : message
    }
    if request.method == 'POST' :
        code = str(request.POST['ipstr'])
        cip = str(request.POST['cipher'])
        meth = 1
        if "enc" in request.POST:
            meth = 1
        if "dec" in request.POST:
            meth = 2
        if cip == "Wrong":
            message.append("Select a valid Cipher")
        elif cip == "CaesarCipher":
            inpt = int(request.POST['inpc'])
            message.append(caesarcipher(code,inpt,meth))
        elif cip == "Base64":
            import base64
            if meth==1:
                a=base64.b64encode(bytes(code, 'utf-8'))
                message.append(a.decode('utf-8'))
            if meth==2:
                a=base64.b64decode(code)
                message.append(a.decode("ascii"))
        elif cip == "MorseCode":
            code=code.upper()
            message.append(morse(code,meth))
        elif cip == "InverseCasing":
            message.append(code.swapcase())
        elif cip == "VigenereCipher":
            inpt = str(request.POST['inpc'])
            inpt=inpt.upper()
            code=code.upper()
            message.append(vincipher(code,inpt,meth))
        elif cip == "CameltoSnake":
            message.append(cameltosnake(code,meth))
    return render(request, 'myapp/mainpage.html', context)

def caesarcipher(code,inpt,meth):
    ans=""
    if meth==1 :
        for i in range(len(code)):
            ch = code[i]
            if ch==" ":
                ans+=" "
            elif (ch.isupper()):
                ans += chr((ord(ch) + inpt-65) % 26 + 65)
            else:
                ans += chr((ord(ch) + inpt-97) % 26 + 97)
    elif meth==2 :
        letters="abcdefghijklmnopqrstuvwxyz"
        for ch in code:
            if ch in letters:
                position = letters.find(ch)
                new_pos = (position - inpt) % 26
                new_char = letters[new_pos]
                ans += new_char
            else:
                ans += ch
    return ans

def morse(code,meth):
    MORSE_CODE_DICT = { 'A':'.-', 'B':'-...','C':'-.-.', 'D':'-..', 'E':'.','F':'..-.', 'G':'--.', 'H':'....',
					'I':'..', 'J':'.---', 'K':'-.-','L':'.-..', 'M':'--', 'N':'-.','O':'---', 'P':'.--.', 
                    'Q':'--.-','R':'.-.', 'S':'...', 'T':'-','U':'..-', 'V':'...-', 'W':'.--','X':'-..-', 
                    'Y':'-.--', 'Z':'--..','1':'.----', '2':'..---', '3':'...--','4':'....-', '5':'.....', 
                    '6':'-....','7':'--...', '8':'---..', '9':'----.','0':'-----', ', ':'--..--', '.':'.-.-.-',
					'?':'..--..', '/':'-..-.', '-':'-....-','(':'-.--.', ')':'-.--.-'}
    ans = ''
    if meth == 1:
        for letter in code:
            if letter != ' ':
                ans += MORSE_CODE_DICT[letter] + ' '
            else:
                ans += ' '
    if meth == 2:
        citext = ''
        for letter in code:
            if (letter != ' '):
                i = 0
                citext += letter
            else:
                i += 1
                if i == 2 :
                    ans += ' '
                else:
                    ans += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                    citext = ''
    return ans

def vincipher(code,inpt,meth):
    ans = []
    inpt = list(inpt)
    if len(code) == len(inpt):
        key=inpt
    else:
        for i in range(len(code) - len(inpt)):
            inpt.append(inpt[i % len(inpt)])
        key = ("" . join(inpt))
    if meth == 1:
        for i in range(len(code)):
            x = (ord(code[i]) + ord(key[i])) % 26
            x += ord('A')
            ans.append(chr(x))
    elif meth == 2:
        for i in range(len(code)):
            x = (ord(code[i]) -
            ord(key[i]) + 26) % 26
            x += ord('A')
            ans.append(chr(x))
    return("" . join(ans))

def cameltosnake(code,meth):
    if meth == 1:
        ans = [code[0].lower()]
        for c in code[1:]:
            if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                ans.append('_')
                ans.append(c.lower())
            else:
                ans.append(c)
    if meth == 2:
        temp = code.split('_')
        ans = temp[0] + ''.join(ele.title() for ele in temp[1:])
    return ''.join(ans)