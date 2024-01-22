
from flask import Flask, render_template,request
from dbcontext import DbContext
from ClassLib.buses import Buses
from ClassLib.cities import Cities
from ClassLib.clients import Clients
from ClassLib.tickets import Tickets
from ClassLib.timetable import Timetable

db_context = DbContext()

app = Flask(__name__)

buses=[Buses()]
cities=[Cities()]
tickets=[Tickets()]
user=Clients()
timetable=[Timetable()]


@app.route('/journeys')
def journeys():
    buses = db_context.get_items(Buses())

    return render_template("journeys.html", buses=buses ,user=user)

@app.route('/home')
@app.route('/')
def home():
    return render_template("home.html",user=user)


@app.route('/About')
def about():
    return render_template("about.html",user=user)


@app.route('/loginselect')
def loginselect():
    return render_template("loginselect.html",user=user)


@app.route('/login/<data>',methods=['GET','POST'])
def login(data):
    if request.method == "POST":
        request.form['floatingInputName']
    return render_template('login.html', data=data,user=user)


@app.route('/register' ,methods=['POST','GET'])
def register():
    if request.method =="POST":
        name = str(request.form['floatingInputName'])
        email=str(request.form['floatingInputEmail'])
        phone=str(request.form['floatingInputPhone'])
        password=str(request.form['floatingInputPassTwo'])
        role_client='user'
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        if password:
            user.password = password
            print()
        if role_client:
            user.role_client=role_client
        db=DbContext()
        if(db.add_item(user)):
            return render_template("home.html",user=user)
        else:
            return render_template("register.html", user=user)
    else:
        return render_template("register.html",user=user)


if __name__ == "__main__":
    app.run(debug=True)
