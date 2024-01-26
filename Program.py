import os
from flask import Flask, render_template,request,session,redirect,abort
from dbcontext import DbContext
from ClassLib.buses import Buses
from ClassLib.cities import Cities
from ClassLib.clients import Clients
from ClassLib.tickets import Tickets
from ClassLib.timetable import Timetable


app = Flask(__name__)
app.secret_key = os.urandom(24)

db_context = DbContext()




@app.route('/journeys')
def journeys():
    buses = db_context.get_items(Buses())
    return render_template("journeys.html", buses=buses,user=GetFromDict())

@app.route('/')
def firstroute():
    return render_template("home.html",user=GetFromDict())

@app.route('/home')
def home():
    return render_template("home.html", user=GetFromDict())


@app.route('/About')
def about():
    return render_template("about.html",user=GetFromDict())


@app.route('/loginselect')
def loginselect():
    return render_template("loginselect.html",user=None)

@app.route('/login/<data>',methods=['GET','POST'])
def login(data):
    if request.method == "POST":
        item=str(data)
        password= request.form['floatingPassword']
        if data == "email":
            value = request.form['floatingInputEmail']
            if CreateUser(password, item, value)=="Пароль не співпадає":
                return render_template('login.html', data=data, user=None, info="Не вірний пароль")
            elif CreateUser(password, item, value):
                return redirect("/home")
            else:
                return render_template('login.html', data=data, user=None, info="")
        elif data == "phone":
            value = request.form['floatingInputPhone']
            if CreateUser(password,item, value):
                return redirect("/home")
            else :
                return render_template('login.html', data=data, user=None,info="")
    if request.method == "GET":
        return render_template('login.html', data=data, user=None,info="")
    else:
        return redirect("/home")

@app.route('/register' ,methods=['POST','GET'])
def register():
    if request.method =="POST":
        if GetFromDict() is None:
            name = str(request.form['floatingInputName'])
            email=str(request.form['floatingInputEmail'])
            phone=str(request.form['floatingInputPhone'])
            password=str(request.form['floatingInputPassTwo'])
            role_client='user'
            user=Clients()
            if name:
                user.name = name
            if email:
                user.email = email
            if phone:
                user.phone = phone
            if password:
                user.password = password
            if role_client:
                user.role_client=role_client
            if(db_context.add_item(user)):
                AddToDict(user)
                return redirect("/home")
            else:
                return render_template("register.html", user=None,info="Account not register")
        else:
            return redirect("/home")
    if request.method == "GET":
        return render_template("register.html",user=None,info=None)

@app.route('/accountview')
def accountview():

    if GetFromDict() is not None:
        return render_template("accountview.html", user=GetFromDict())
    else:
        return redirect("/home")


@app.route('/adminpanel')
def adminpanel():
    if GetFromDict():
        user=GetFromDict()
        if user.role_client=="admin":
            return render_template("adminpanel.html",user=user)
    return redirect("/home")

def CreateUser(password,item, value):
    if db_context.get_user(password, item, value)=="Пароль не співпадає":
        return "Пароль не співпадає"
    elif db_context.get_user(password,item,value):
        user = db_context.get_user(password,item,value)
        AddToDict(user)
        return True
    else:
        return False

def AddToDict(user=Clients()):
    user_dict = user.to_dict()
    session['user'] = user_dict


def GetFromDict():
    if session.get('user', {}):
        user_dict = session.get('user', {})
        user = Clients.from_dict(user_dict)
        return user
    else:
        return None

def DeleteFromDict():
    if 'user' in session:
        del session['user']
        AddToDict()



if __name__ == "__main__":
    app.run(debug=True)
