from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth import authenticate, login as Login, logout as Logout
from django.contrib.auth.models import User
from .models import Card as CARDS , Contact, Product as PRODDUCT, View as VIEW, Membership as MEMBERSHIP, ContactMessage, Bug
import razorpay
import re
import uuid
from datetime import date, datetime

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
##########################################################################################
##########################################################################################
###################################### Users Views #######################################
##########################################################################################
##########################################################################################

# Dashboard View
def Dashboard(request):
    if request.user.is_authenticated:
        products = 0
        messages = 0
        for card in CARDS.objects.filter(username=request.user.username):
            products += len(PRODDUCT.objects.filter(cardname=card.cardname))
            messages += len(Contact.objects.filter(cardname=card.cardname))
        context = {
            "title": "Dashboard",
            "logo": request.user.username.upper()[:1],
            "cards": CARDS.objects.filter(username=request.user.username),
            "cardsMade": len(CARDS.objects.filter(username=request.user.username)),
            "products": products,
            "messages": messages,
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email
            }
        }
        return render(request, "user/dashboard.html", context)
    else:
        return redirect("/")

# Analytics View
def Analytics(request):
    if request.user.is_authenticated:
        cardAnalytics = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0}
        for card in CARDS.objects.filter(username=request.user.username):
            for view in VIEW.objects.filter(cardname=card.cardname):
                if(view.date[:4] == str(datetime.now().year)):
                    cardAnalytics[view.date[5:7]]+=1
        context = {
            "title": "Analytics",
            "logo": request.user.username.upper()[:1],
            "year": datetime.now().year,
            "cardAnalytics": cardAnalytics,
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email
            }
        }
        return render(request, "user/analytics.html", context)
    else:
        return redirect("/")

# Cards View
def Cards(request):
    if request.user.is_authenticated:
        context = {
            "title": "Cards",
            "logo": request.user.username.upper()[:1],
            "cards": CARDS.objects.filter(username=request.user.username),
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email
            }
        }
        return render(request, "user/cards.html", context)
    else:
        return redirect("/")

# Membership View
def Membership(request):
    if request.user.is_authenticated:
        context = {
            "title": "Membership",
            "logo": request.user.username.upper()[:1],
            "memebership": MEMBERSHIP.objects.filter(username=request.user.username)[0].membership,
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email
            }
        }
        return render(request, "user/membership.html", context)
    else:
        return redirect("/")

# Settings View
def Settings(request):
    if request.user.is_authenticated:
        context = {
            "title": "Settings",
            "error": "",
            "logo": request.user.username.upper()[:1],
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email
            }
        }
        if request.method == "POST":
            firstName = str(request.POST.get("firstname"))
            lastName = str(request.POST.get("lastname"))
            email = str(request.POST.get("email"))
            if (firstName == "" or lastName == "" or email == ""):
                context["error"] = "Please fill details."
            else:
                user = User.objects.get(username=request.user.username)
                user.first_name = firstName
                user.last_name = lastName
                user.email = email
                user.save()
                return redirect("/settings")
        return render(request, "user/settings.html", context)
    else:
        return redirect("/")

# CloseAccount View
def CloseAccount(request):
    if request.user.is_authenticated:
        context = {
            "title": "Close Account",
            "error": "",
            "logo": request.user.username.upper()[:1],
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email
            }
        }
        # Delete user and its card code....
        if request.method == "POST":
            if(str(request.POST.get("checkbox")) == "on"):
                VIEW.objects.filter(cardname=CARDS.objects.filter(username=request.user.username)[0].cardname).delete()
                PRODDUCT.objects.filter(cardname=CARDS.objects.filter(username=request.user.username)[0].cardname).delete()
                Contact.objects.filter(cardname=CARDS.objects.filter(username=request.user.username)[0].cardname).delete()
                CARDS.objects.filter(username=request.user.username).delete()
                User.objects.filter(username=request.user.username).delete()
                return redirect("/")
            else:
                context["error"] = "Select the checkbox to close account."
        return render(request, "user/closeaccount.html", context)
    else:
        return redirect("/")

# ChangePassword View
def ChangePassword(request):
    if request.user.is_authenticated:
        context = {
            "title": "Settings" ,
            "error": "",
            "logo": request.user.username.upper()[:1],
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email
            }
        }
        if request.method == "POST":
            password = str(request.POST.get("password"))
            CKpassword = str(request.POST.get("confirmpassword"))
            if (password == "" or CKpassword == ""):
                context["error"] = "Please fill fields."
            elif (password != CKpassword):
                context["error"] = "Password and Confirm Password do not match."
            else:
                user = User.objects.get(username=request.user.username)
                user.set_password(password)
                user.save()
        return render(request, "user/changepassword.html", context)
    else:
        return redirect("/")

# Get MemberShip View
def GetMemberShip(request, tp):
    if request.user.is_authenticated:
        if(tp == "business" or tp == "enterprise"):
            if (tp == "business"):
                price = 199
                li = "Upto Make 10cards free"
            elif(tp == "enterprise"):
                price = 499
                li = "Make endless free cards"
            razorpay_order = razorpay_client.order.create(dict(amount=price, currency="INR", payment_capture='0'))
            context = {
                "title": "Membership" ,
                "logo": request.user.username.upper()[:1],
                "type" : tp.capitalize(),
                "price": price,
                "li": li,
                "user": {
                    "username": request.user.username,
                    "firstName": request.user.first_name,
                    "lastName": request.user.last_name,
                    "email": request.user.email,
                },
                "razorpay_order_id": razorpay_order['id'],
                "razorpay_merchant_key": settings.RAZOR_KEY_ID,
                "razorpay_amount": price,
                "currency": "INR",
                "callback_url": 'paymenthandler/',
            }
            return render(request, "user/getmembership.html", context)
        else:
            return redirect("/membership")
    else:
        return redirect("/")

# Add New Card View
def AddNewCard(request):
    if request.user.is_authenticated:
        if ((MEMBERSHIP.objects.filter(username=request.user.username)[0].membership == "Personal") and (len(CARDS.objects.filter(username=request.user.username)) >= 4)):
            return redirect("/")
        elif ((MEMBERSHIP.objects.filter(username=request.user.username)[0].membership == "Business") and (len(CARDS.objects.filter(username=request.user.username)) >= 49)):
            return redirect("/")
        context = {
            "title": "Cards" ,
            "logo": request.user.username.upper()[:1],
            "error": "",
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email,
            }
        }
        if request.method == "POST":
            cardname = str(request.POST.get("cardname"))
            name = str(request.POST.get("name"))
            position = str(request.POST.get("position"))
            about = str(request.POST.get("about"))
            phone = str(request.POST.get("phone"))
            whatsaspp = str(request.POST.get("whatsaspp"))
            email = str(request.POST.get("email"))
            website = str(request.POST.get("website"))
            address = str(request.POST.get("address"))
            facebook = str(request.POST.get("facebook"))
            instagram = str(request.POST.get("instagram"))
            linkedin = str(request.POST.get("linkedin"))
            twitter = str(request.POST.get("twitter"))
            youtube = str(request.POST.get("youtube"))
            if (len(CARDS.objects.filter(cardname=cardname)) > 0):
                context["error"] = "Cardname already exists."
            elif (len(cardname)>100):
                context["error"] = "Cardname must be less than 100 characters."
            elif (len(name)>20):
                context["error"] = "Name must be less than 20 characters."
            elif (len(position)>100):
                context["error"] = "Position must be less than 100 characters."
            elif (len(about)>1000):
                context["error"] = "About must be less than 1000 characters."
            elif (len(phone)>15):
                context["error"] = "Phone must be less than 15 characters."
            elif (len(whatsaspp)>15):
                context["error"] = "Whatsaspp must be less than 15 characters."
            elif (len(email)>50):
                context["error"] = "Email must be less than 50 characters."
            elif (len(website)>50):
                context["error"] = "Website must be less than 50 characters."
            elif (len(address)>100):
                context["error"] = "Address must be less than 100 characters."
            elif ((len(facebook)>100) or (len(instagram)>100) or (len(twitter)>100) or (len(linkedin)>100) or (len(youtube)>100)):
                context["error"] = "Socials must be less than 100 characters."
            else:
                try:
                    card = CARDS(cardname=cardname, name=name, position=position, about=about, phone=phone, whatsaspp=whatsaspp, email=email, website=website, address=address, facebook=facebook, instagram=instagram, linkedin=linkedin, twitter=twitter, youtube=youtube, username=request.user.username)
                    card.save()
                    return redirect("/cards")
                except:
                    context["error"] = "Cardname already exists."
        return render(request, "user/addcards.html", context)
    else:
        return redirect("/")

# Edit Card View
def EditCard(request, cardname):
    if request.user.is_authenticated:
        if len(CARDS.objects.filter(cardname=cardname, username=request.user.username)) == 1:
            context = {
                "title": "Cards" ,
                "logo": request.user.username.upper()[:1],
                "errors": "",
                "card": CARDS.objects.filter(cardname=cardname)[0],
                "user": {
                    "username": request.user.username,
                    "firstName": request.user.first_name,
                    "lastName": request.user.last_name,
                    "email": request.user.email,
                }
            }
            if request.method == "POST":
                name = str(request.POST.get("name"))
                position = str(request.POST.get("position"))
                about = str(request.POST.get("about"))
                phone = str(request.POST.get("phone"))
                whatsaspp = str(request.POST.get("whatsaspp"))
                email = str(request.POST.get("email"))
                website = str(request.POST.get("website"))
                address = str(request.POST.get("address"))
                facebook = str(request.POST.get("facebook"))
                instagram = str(request.POST.get("instagram"))
                linkedin = str(request.POST.get("linkedin"))
                twitter = str(request.POST.get("twitter"))
                youtube = str(request.POST.get("youtube"))
                if (len(name)>20):
                    context["error"] = "Name must be less than 20 characters."
                elif (len(position)>100):
                    context["error"] = "Position must be less than 100 characters."
                elif (len(about)>1000):
                    context["error"] = "About must be less than 1000 characters."
                elif (len(phone)>15):
                    context["error"] = "Phone must be less than 15 characters."
                elif (len(whatsaspp)>15):
                    context["error"] = "Whatsaspp must be less than 15 characters."
                elif (len(email)>50):
                    context["error"] = "Email must be less than 50 characters."
                elif (len(website)>50):
                    context["error"] = "Website must be less than 50 characters."
                elif (len(address)>100):
                    context["error"] = "Address must be less than 100 characters."
                elif ((len(facebook)>100) or (len(instagram)>100) or (len(twitter)>100) or (len(linkedin)>100) or (len(youtube)>100)):
                    context["error"] = "Socials must be less than 100 characters."
                else:
                    try:
                        CARDS.objects.filter(cardname=cardname).update(cardname=cardname, name=name, position=position, about=about, phone=phone, whatsaspp=whatsaspp, email=email, website=website, address=address, facebook=facebook, instagram=instagram, linkedin=linkedin, twitter=twitter, youtube=youtube, username=request.user.username)
                        return redirect(f"/editcard/{cardname}")
                    except:
                        context["error"] = "Error in length of data."
            return render(request, "user/editcard.html", context)
        else:
            return redirect("/cards")
    else:
        return redirect("/")

# Delete Card View
def DeleteCard(request, cardname):
    if request.user.is_authenticated:
        if (len(CARDS.objects.filter(cardname=cardname, username=request.user.username)) == 1):
            if request.method == "POST":
                try:
                    CARDS.objects.filter(cardname=cardname, username=request.user.username).delete()
                    VIEW.objects.filter(cardname=cardname).delete()
                    PRODDUCT.objects.filter(cardname=cardname).delete()
                    Contact.objects.filter(cardname=cardname).delete()
                except:
                    pass
                return redirect("/cards")
            context = {
                "title": "Cards" ,
                "logo": request.user.username.upper()[:1],
                "user": {
                    "username": request.user.username,
                    "firstName": request.user.first_name,
                    "lastName": request.user.last_name,
                    "email": request.user.email,
                }
            }
            return render(request, "user/deletecard.html", context)
        else:
            return redirect("/cards")
    else:
        return redirect("/")

# Products View
def Products(request):
    if request.user.is_authenticated:
        products = []
        for card in CARDS.objects.filter(username=request.user.username):
            products.append(PRODDUCT.objects.filter(cardname=card.cardname))
        context = {
            "title": "Products" ,
            "logo": request.user.username.upper()[:1],
            "products": products,
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email,
            }
        }
        return render(request, "user/products.html", context)
    else:
        return redirect("/")

# Add Product View
def Product(request, PID):
    if request.user.is_authenticated:
        if (len(PRODDUCT.objects.filter(PID=PID)) != 1):
            return redirect("/products")
        context = {
            "title": "Products" ,
            "logo": request.user.username.upper()[:1],
            "product": PRODDUCT.objects.filter(PID=PID)[0],
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email,
            }
        }
        return render(request, "user/product.html", context)
    else:
        return redirect("/")

# Add Product View
def AddProduct(request):
    if request.user.is_authenticated:
        cards = []
        for card in  CARDS.objects.filter(username=request.user.username):
            cards.append(str(card.cardname))
        context = {
            "title": "Products" ,
            "logo": request.user.username.upper()[:1],
            "error": "",
            "cards": cards,
            "cardslen": len(cards),
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email,
            }
        }
        if request.method == "POST":
                try:
                    image = request.FILES["image"]
                    title = str(request.POST.get("title"))
                    price = str(request.POST.get("price"))
                    cardname = str(request.POST.get("cardname"))
                    if (len(title) > 50):
                        context["error"] = "Title must be less than 50 characters."
                    elif (len(price) > 20):
                        context["error"] = "Price must be less than 20 characters."
                    else:
                        product = PRODDUCT(PID = str(uuid.uuid4()),cardname=cardname, title=title, image=image, price=price)
                        product.save()
                        return redirect("/products")
                except:
                    context["error"] = "Please select an image."
        return render(request, "user/addproduct.html", context)
    else:
        return redirect("/")

# Edit Product View
def EditProduct(request, PID):
    if request.user.is_authenticated:
        if (len(PRODDUCT.objects.filter(PID=PID)) != 1):
            return redirect("/products")
        context = {
            "title": "Products" ,
            "logo": request.user.username.upper()[:1],
            "error": "",
            "p": PRODDUCT.objects.filter(PID=PID)[0],
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email,
            }
        }
        if request.method == "POST":
                title = str(request.POST.get("title"))
                price = str(request.POST.get("price"))
                if (len(title) > 50):
                    context["error"] = "Title must be less than 50 characters."
                elif (len(price) > 20):
                    context["error"] = "Price must be less than 20 characters."
                else:
                    product = PRODDUCT.objects.filter(PID=PID).update(title=title, price=price)
                    return redirect(f"/editproduct/{PID}/")
        return render(request, "user/editproduct.html", context)
    else:
        return redirect("/")

# Delete Product View
def DeleteProduct(request, PID):
    if request.user.is_authenticated:
        try:
           PRODDUCT.objects.filter(PID=PID).delete()
        except:
            pass
        return redirect("/products")
    else:
        return redirect("/")


# Messages View
def Messages(request):
    if request.user.is_authenticated:
        messages = []
        for card in CARDS.objects.filter(username=request.user.username):
            messages.append(Contact.objects.filter(cardname=card.cardname))
        context = {
            "title": "Messages" ,
            "logo": request.user.username.upper()[:1],
            "messages": messages,
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email,
            }
        }
        return render(request, "user/messages.html", context)
    else:
        return redirect("/")

# Message View
def Message(request, messageID):
    if request.user.is_authenticated:
        if (len(Contact.objects.filter(messageID=messageID))!=1):
            return redirect("/messages")
        context = {
            "title": "Messages" ,
            "logo": request.user.username.upper()[:1],
            "message": Contact.objects.filter(messageID=messageID)[0],
            "user": {
                "username": request.user.username,
                "firstName": request.user.first_name,
                "lastName": request.user.last_name,
                "email": request.user.email,
            }
        }
        return render(request, "user/message.html", context)
    else:
        return redirect("/")

##########################################################################################
##########################################################################################
###################################### Global Views ######################################
##########################################################################################
##########################################################################################

# Home View
def HomePage(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "global/homepage.html", {"title": "Home"})

# About View
def AboutPage(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "global/about.html", {"title": "About"})

# Testimonials View
def TestimonialsPage(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "global/testimonials.html", {"title": "Testimonials"})

# ContactUs View
def ContactUsPage(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        context = {"title": "Contact Us", "error": ""}
        if request.method == "POST":
            name = str(request.POST.get("name"))
            email = str(request.POST.get("email"))
            message = str(request.POST.get("message"))
            if(len(name)<1 or len(email)<1 or len(message)<1):
                context["error"] = "Please fill details."
            else:
                try:
                    message = ContactMessage(name=name,email=email,message=message)
                    message.save()
                    return redirect("/")
                except:
                    context["error"] = "Message to long."
        return render(request, "global/contactus.html", context)

# SignIn View
def SignInPage(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        context = {"title": "Sign In", "error": ""}
        if request.method == "POST":
            username = str(request.POST.get("username"))
            password = str(request.POST.get("password"))
            user = authenticate(username=username, password=password)
            if user:
                Login(request, user)
                return redirect("/dashboard")
            else:
                context["error"] = "Invalid username or password."
        return render(request, "global/signin.html", context)

# LogOut View
def logout(request):
    if request.user.is_authenticated:
        Logout(request)
    return redirect("/")

# SignUp Views
def SignUpPage(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        context = {"title": "Sign Up", "error": ""}
        if request.method == "POST":
            username = str(request.POST.get("username"))
            email = str(request.POST.get("email"))
            password = str(request.POST.get("password"))
            # Checking NameField errors
            if (len(username)<1):
                context["error"] = "Please fill your name."
            elif(len(username)>64):
                context["error"] = "Name must be less than 64characters."
            elif(re.compile(r'[@_!#$%^&*()<>?/\|}{~:]').search(username)):
                context["error"] = "Name cann't contain special characters."
            elif(any(char.isdigit() for char in username)):
                context["error"] = "Name cann't contain numbers."
            # Checking EmailField errors
            elif(len(email)<5):
                context["error"] = "Malformed Email Address."
            elif(len(email)>64):
                context["error"] = "Email must be less than 64characters."
            elif(("@" not in email) or ("." not in email)):
                context["error"] = "Malformed Email Address."
            # Checking PasswordField errors
            elif(len(password)<8):
                context["error"] = "Password must be greater than 8characters."
            elif(len(password)>64):
                context["error"] = "Password must be less than 64characters."
            else:
                # Saving data to backend
                if(User.objects.filter(username=username).exists()):
                    context["error"] = "Username already exists."
                elif(User.objects.filter(email=email).exists()):
                    context["error"] = "Email Address already exists."
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    membership = MEMBERSHIP(username=username)
                    membership.save()
                    return redirect("/signin")
        return render(request, "global/signup.html", context)

# Bugs View
def Bugs(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        context = {"title": "Bugs", "error": ""}
        if request.method == "POST":
            bug = str(request.POST.get("bug"))
            details = str(request.POST.get("details"))
            if(len(bug)<1 or len(bug)>100):
                context["error"] = "Title length is incorrect."
            elif(len(details)<1 or len(details)>1000):
                context["error"] = "Details length is incorrect."
            else:
                try:
                    bug = Bug(bug=bug, details=details)
                    bug.save()
                except:
                    context["error"] = "Message too long."
        return render(request, "global/bugs.html", context)

# Manifesto View
def Manifesto(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "global/manifesto.html", {"title": "Manifesto"})

# Porducts View
def Productt(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "global/product.html", {"title": "Product"})

# Source Code View
def SourceCode(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "global/sourcecode.html", {"title": "Source Code"})

# Profile View
def Profile(request, username):
    if (len(User.objects.filter(username=username)) > 0):
        return render(request, "global/profile.html", {"title": username, "user": User.objects.filter(username=username)[0], "cards":CARDS.objects.filter(username=username)})
    else:
        return redirect("/")


##########################################################################################
##########################################################################################
##################################### ViewCard View ######################################
##########################################################################################
##########################################################################################
def ViewCard(request, cardname):
    card = CARDS.objects.filter(cardname=cardname)
    if len(card) == 1:
        if (len(VIEW.objects.filter(cardname=card[0].cardname, date=date.today(), time=str(datetime.now().strftime("%H:%M:%S"))[:5], host=request.headers['Host'])) == 0):
            views = VIEW(cardname=card[0].cardname, host=request.headers["Host"], time=str(datetime.now().strftime("%H:%M:%S"))[:5])
            views.save()
        if request.method == "POST":
            name = str(request.POST.get("name"))
            email = str(request.POST.get("email"))
            message = str(request.POST.get("message"))
            contact = Contact(messageID=str(uuid.uuid4()),name=name, email=email, message=message, cardname=cardname, date=date.today(), time=str(datetime.now().strftime("%H:%M:%S")))
            contact.save()
        context={
            "cardname": cardname,
            "card": card[0],
            "products": PRODDUCT.objects.filter(cardname=cardname),
            "views": len(VIEW.objects.filter(cardname=card[0].cardname))+1,
        }
        return render(request, "card.html", context)
    else:
        return redirect("/")
    
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    return render(request, 'paymentsuccess.html')
                except:
                    return render(request, 'paymentfail.html')
            else:
                return render(request, 'paymentfail.html')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################