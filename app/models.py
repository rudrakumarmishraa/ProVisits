from django.db import models
from datetime import date, datetime


###############################################
################ Users Models #################
###############################################
# Bugs Model
class Card(models.Model):
    # Basic Details
    cardname = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=100)
    # Links on top
    phone = models.CharField(max_length=15, default="")
    address = models.CharField(max_length=100, default="")
    whatsaspp = models.CharField(max_length=15, default="")
    email = models.CharField(max_length=50, default="")
    website = models.CharField(max_length=50, default="")
    # Social Links
    facebook = models.CharField(max_length=200, default="")
    instagram = models.CharField(max_length=200, default="")
    twitter = models.CharField(max_length=200, default="")
    linkedin = models.CharField(max_length=200, default="")
    youtube = models.CharField(max_length=200, default="")
    about = models.CharField(max_length=1000, default="")
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.cardname

# Contact Us
class Contact(models.Model):
    messageID = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    cardname = models.CharField(max_length=100)
    date = models.CharField(max_length=20, default=date.today())
    time = models.CharField(max_length=20, default=datetime.now().strftime("%H:%M:%S"))
    def __str__(self):
        return self.messageID

# Products
class Product(models.Model):
    PID = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='products/')
    price = models.CharField(max_length=20)
    cardname = models.CharField(max_length=100)
    date = models.CharField(max_length=20, default=date.today())
    time = models.CharField(max_length=20, default=datetime.now().strftime("%H:%M:%S"))
    def __str__(self):
        return self.cardname

# View Model
class View(models.Model):
    cardname = models.CharField(max_length=100)
    date = models.CharField(max_length=12, default=date.today())
    time = models.CharField(max_length=5, default=str(datetime.now().strftime("%H:%M:%S"))[:5])
    host = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.cardname

# Membership Model
class Membership(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    membership = models.CharField(max_length=50, default="Personal")
    def __str__(self):
        return self.username

###############################################
################ Global Models ################
###############################################

# ContactUs Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    date = models.CharField(max_length=20, default=date.today())
    time = models.CharField(max_length=20, default=datetime.now().strftime("%H:%M:%S"))
    def __str__(self):
        return self.name

# Bugs Model
class Bug(models.Model):
    bug = models.CharField(max_length=100)
    details = models.CharField(max_length=1000)
    date = models.CharField(max_length=20, default=date.today())
    time = models.CharField(max_length=20, default=datetime.now().strftime("%H:%M:%S"))
    def __str__(self):
        return self.bug