
#from typing import OrderedDict
from werkzeug.wrappers.base_request import _assert_not_shallow
import pyrebase


config={
  "apiKey" : "AIzaSyAsMe1T2wsrZTdSit5GlM-J9TwdSX5J3qo",
  "authDomain": "pawfect-pets.firebaseapp.com",
  "databaseURL": "https://pawfect-pets-default-rtdb.firebaseio.com",
  "projectId": "pawfect-pets",
  "storageBucket": "pawfect-pets.appspot.com",
  "messagingSenderId": "901246246332",
  "appId": "1:901246246332:web:9b39d9ec3e4fcbf5d4dfb9",
  "measurementId": "G-D13X1KVGRC"
}

# config = {
#   "apiKey": "AIzaSyBblyeiyNq3IUN3jVWXuh-WpZeRnzoF7co",
#   "authDomain": "petstoredemo-1c29e.firebaseapp.com",
#   "databaseURL": "https://petstoredemo-1c29e-default-rtdb.firebaseio.com",
#   "projectId": "petstoredemo-1c29e",
#   "storageBucket": "petstoredemo-1c29e.appspot.com",
#   "messagingSenderId": "611067598544",
#   "appId": "1:611067598544:web:9bd0803eb64bb56461f0d5",
#   "measurementId": "G-LBDHW2W3JR"
# }


firebase = pyrebase.initialize_app(config)
db=firebase.database()
auth = firebase.auth()
storage=firebase.storage()
#storage.child("Images/new.img").get_url(None)
#db.child("animals").child("dog").child("1").update({"name":"bi"})
#user=db.child("").child("dog").child("1").get()
#print(user.val())


from flask import render_template,request,Flask,session,redirect



app=Flask(__name__)
app.secret_key = b'abc'

@app.route('/',methods=['GET','POST'])
def login():
    unsuccessful = 'Please check your credentials'
    successful = 'Login successful'
    if request.method == 'POST':
            email = request.form.get('E-mail')
            session['username']=email
            password = request.form.get('pw')
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                #register = db.child("login").child("users").get()
                #registerList = register.val()
                print(successful)
                return render_template('mainpage.html')
            except:
                print(unsuccessful)


    return render_template('coverpage.html')

@app.route('/register',methods=['GET','POST'])
def register():
   if request.method == 'POST':
            email = request.form.get('E-mail')
            password = request.form.get('pw')
            cpass=request.form.get('cpw')
            if password==cpass:
               auth.create_user_with_email_and_password(email,password)
               print("success")
               return render_template('coverpage.html')

   return render_template('register.html') 
   
@app.route('/home',methods=['GET','POST'])
def home():
   return render_template('mainpage.html') 

   
@app.route('/sellpets',methods=['GET','POST'])
def sellpets():
   if request.method=='POST':
        pet=request.form['sell']
        breed=request.form['breed']
        photo=request.files['photo']
        age=request.form['age']
        weight=request.form['weight']
        height=request.form['height']
        price=request.form['price']
        birthday=request.form['birthday']
        owner=request.form['owner']
        contact=request.form['contact']
        email=request.form['email']
        storage.child("Images/"+owner+".png").put(photo)
        if True:
            link=storage.child("Images/"+owner+".png").get_url(None)
        petInfo=dict({"Breed":breed, "Age":age, "Height":height, "Weight":weight,"Price":price,"Birthday":birthday,"Owner's Name":owner,"Contact Number":contact,"E-mail Id":email,"Pet Photo":link})
        db.child(pet).push(petInfo)
   return render_template('SellPets.html')
    


@app.route('/purchasePets',methods=['GET','POST'])
def purchase():

   return render_template('purchasePets.html')   


# @app.route('/purchasePets/Dog',methods=['GET','POST'])
# def purchasepets():
   
#    return redirect(url_for('dispAnimals'))     

@app.route('/purchasePets/<petname>',methods=['GET','POST'])
def dispAnimals(petname):
  all_details=db.child(petname).get().val()
  #print(all_details)
  l=[]

  
  for i in all_details.values():
     for k,v in i.items():
        #print(k,v)
        if k=="Pet Photo":
           l.append(v)



          
  #print(all_details[2]['owner name'])
  email=session['username']
  return render_template('dispDogs.html',data=all_details,url=l,email=email,pet=petname)

@app.route('/removePet/<pet>',methods=['GET','POST'])
def remv(pet):

   return render_template('greet.html')

@app.route('/consult-a-vet',methods=['GET','POST'])
def vet():

   return render_template('vet.html')   

if __name__ == "__main__":
     app.run(debug=True,port=5024)
    
