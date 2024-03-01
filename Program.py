import os
from flask import Flask, render_template,request,session,redirect,abort,url_for
from dbcontext import DbContext
from ClassLib.buses import Buses
from ClassLib.cities import Cities
from ClassLib.clients import Clients
from ClassLib.tickets import Tickets
from ClassLib.timetable import Timetable
from ClassLib.orders import Orders
from ClassLib.journeystable import JourneysTable
from ClassLib.non_autorized_users import Non_autorized_users
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

db_context = DbContext()


@app.route('/buyticket/', methods=['GET','POST'])
def buyticket():
    if request.method == "POST":
        return redirect("/home")
    return redirect("/formbuyticket")

@app.route('/formbuyticket', methods=['GET','POST'])
def formbuyticket():
    if request.method=="GET":
        if (request.args.get('citystart') and request.args.get('cityfinish')
                and request.args.get('starttime') and request.args.get('finishtime')):
            query = (
            f"SELECT timetable.id_journey,buses.name AS bus_name, start_city.name AS start_city, finish_city.name AS finish_city, timetable.time_start, timetable.time_finish ,timetable.cost FROM timetable "
            f"JOIN cities AS start_city ON timetable.city_start_id = start_city.id_city "
            f"JOIN cities AS finish_city ON timetable.city_finish_id = finish_city.id_city "
            f"JOIN buses ON timetable.bus_id = buses.id_bus ")
            if request.args.get('citystart') == "Відправляємся з":
                pass
            elif request.args.get('citystart'):
                citystart = request.args.get('citystart')
                query += f" WHERE start_city.name LIKE '{citystart}'"
            if request.args.get('cityfinish') == "Їдем в":
                pass
            elif request.args.get('cityfinish'):
                cityfinish = request.args.get('cityfinish')
                query += f" AND finish_city.name LIKE '{cityfinish}'"
            if request.args.get('starttime') and request.args.get('finishtime'):
                starttime = request.args.get('starttime')
                finishtime = request.args.get('finishtime')
                starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M')
                finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M')
                query += f" AND timetable.time_start BETWEEN '{starttime}' AND '{finishtime}'"
            table = db_context.get_items(JourneysTable(), newquery=query)
            if table is not None:
                if request.args.get('name') and request.args.get('phone'):
                    non_auth_user=Non_autorized_users()
                    non_auth_user.name=request.args.get('name')
                    non_auth_user.phone=request.args.get('phone')
                    return render_template("tablejourneys.html", user=GetFromDict(), table=table,non_auth_user=non_auth_user)
                else:
                    return render_template("tablejourneys.html", user=GetFromDict(), table=table,non_auth_user=None)
        else:
            cities = db_context.get_items(Cities())
            return render_template("formbuyticket.html", user=GetFromDict(), cities=cities)


    cities = db_context.get_items(Cities())
    return render_template("formbuyticket.html", user=GetFromDict(), cities=cities)


@app.route("/tablejourneys",methods=['GET','POST'])
def tablejourneys():
    pass


@app.route('/selectplace/', methods=['POST'])
def selectplace():
    if request.method == "POST":
        non_auth_user = None
        if request.form.get('phone') and request.form.get('name'):
            non_auth_user = Non_autorized_users()
            non_auth_user.phone = request.form.get('phone')
            non_auth_user.name = request.form.get('name')
        id_journey = request.form.get('id_journey')
        bus_name = request.form.get('bus_name')
        start_city = request.form.get('start_city')
        finish_city = request.form.get('finish_city')
        bus=Buses()
        bus = db_context.get_item_by_other_value(bus,'name',bus_name)
        journey=Timetable()
        journey=db_context.get_item_by_id(journey,id_journey)
        tickets=None
        query=f"SELECT * FROM tickets WHERE tickets.journey_id Like {id_journey}"
        if db_context.get_items(Tickets(),newquery=query)is not None:
            tickets=db_context.get_items(Tickets(),newquery=query)
        countstickets=0
        greyseats=None
        if tickets is not None:
            countstickets=len(tickets)
            greyseats=[]
            for ticket in tickets:
                for seat in range(bus.seats):
                    if ticket.seat == seat:
                        greyseats.append(seat)

        if non_auth_user is not None:
            return render_template("selectplace.html",user=GetFromDict(), non_auth_user=non_auth_user, bus=bus, journey = journey,
                               start_city=start_city, finish_city=finish_city, tickets=tickets,countstickets=countstickets,greyseats=greyseats)
        else:
            return render_template("selectplace.html",user=GetFromDict(), non_auth_user=None, bus=bus, journey = journey,
                               start_city=start_city, finish_city=finish_city, tickets=tickets,countstickets=countstickets,greyseats=greyseats)

    return redirect('/formbuyticket')

@app.route('/pay/', methods=['POST', 'GET'])
def pay():
    if request.method == "POST":
        id_journey = request.form.get('id_journey')
        seat = request.form.get('seat')
        non_auth_user = None
        if request.form.get('phone') and request.form.get('name'):
            non_auth_user = Non_autorized_users()
            non_auth_user.phone = request.form.get('phone')
            non_auth_user.name = request.form.get('name')
        else:
            user = GetFromDict()

        journey = Timetable()
        journey = db_context.get_item_by_id(journey, id_journey)

        bus = Buses()
        bus = db_context.get_item_by_id(bus, journey.bus_id)

        start_city = Cities()
        finish_city = Cities()
        start_city = db_context.get_item_by_id(start_city, journey.city_start_id)
        finish_city = db_context.get_item_by_id(finish_city, journey.city_finish_id)


        return render_template('pay.html',user=GetFromDict(), journey=journey, bus=bus, seat=seat, start_city=start_city,
                               finish_city=finish_city, non_auth_user=non_auth_user)
    else:
        return redirect('/formbuyticket')


@app.route('/succesorder/', methods=['POST'])
def succesorder():
    if request.method == 'POST':
        non_auth_user = None
        if request.form.get('phone') and request.form.get('name'):
            non_auth_user = Non_autorized_users()
            non_auth_user.phone = request.form.get('phone')
            non_auth_user.name = request.form.get('name')
            if db_context.add_item(non_auth_user):
                non_auth_user.id_user=db_context.select_last_index(non_auth_user)

        id_journey = request.form.get('id_journey')
        seat = request.form.get('seat')

        journey = Timetable()
        journey = db_context.get_item_by_id(journey, id_journey)
    #створення нового ордеру
        neworder=Orders()
    #заповнення данних
        if non_auth_user is None:
            user = GetFromDict()
            user=db_context.get_item_by_other_value(user,'email',user.email)
            print(user.id_client)
            neworder.client_id = user.id_client
        else:
            neworder.non_authorized_users_id = non_auth_user.id_user
        neworder.date_buying = neworder.date_buying = datetime.strptime(str(datetime.utcnow().replace(microsecond=0)), '%Y-%m-%d %H:%M:%S')
        neworder.cost = journey.cost

        db_context.add_item(neworder)
    #дістаєм id останнього ордеру
        indexLastOrder = db_context.select_last_index(neworder)
    #створення нового екзепляру ордера та діставання данних з БД
        order = Orders()
        order = db_context.get_item_by_id(order, indexLastOrder)
    #перевірка ордерів між собою
        if (order.client_id == neworder.client_id  and \
                order.non_authorized_users_id == neworder.non_authorized_users_id and \
                str(order.date_buying) == str(neworder.date_buying) and \
                order.cost == neworder.cost):
        #зміна статусу оплати
            whetherpaid = db_context.update_item(order.id_order, 'whether_paid', 1, order)
            if whetherpaid:
                # заповнення данних квитка
                newticket = Tickets()
                newticket.journey_id = journey.id_journey
                newticket.bus_id = journey.bus_id
                newticket.order_id = order.id_order
                newticket.client_id = order.client_id
                newticket.date_buying = datetime.strptime(str(datetime.utcnow().replace(microsecond=0)), '%Y-%m-%d %H:%M:%S')
                if non_auth_user is None:
                    newticket.client_id = user.id_client
                else:
                    newticket.non_autorized_users_id = non_auth_user.id_user
                newticket.seat=seat
                iffer = db_context.add_item(newticket)
                if iffer:
                    bus = Buses()
                    bus = db_context.get_item_by_id(bus, journey.bus_id)
                    start_city = Cities()
                    finish_city = Cities()
                    start_city = db_context.get_item_by_id(start_city, journey.city_start_id)
                    finish_city = db_context.get_item_by_id(finish_city, journey.city_finish_id)
                    if iffer is None:
                        return render_template('succesorder.html', title="Succes", user=GetFromDict(), non_auth_user=non_auth_user,
                                               start_city=start_city,finish_city=finish_city,journey=journey, bus=bus, seat=seat, ticket=newticket)
                    else:
                        return render_template('succesorder.html', title="Succes",user=GetFromDict(), non_auth_user=non_auth_user,
                                               start_city=start_city,finish_city=finish_city,journey=journey, bus=bus, seat=seat, ticket=newticket)
                else:
                    return render_template('succesorder.html', title=None,user=GetFromDict())
            else:
                pass
        else:
            return redirect('/formbuyticket')
    return render_template('succesorder.html', title=None)


@app.route('/journeys', methods=['GET','POST'])
def journeys():
    try:
        if ((request.args.get('item_sort') and request.args.get('direction') and request.args.get('citystart')) or
                (request.args.get('citystart') and request.args.get('cityfinish')) or
                (request.args.get('item_sort') and request.args.get('direction') and request.args.get('citystart')and request.args.get('cityfinish'))):
            item_sort = request.args.get('item_sort')
            direction = request.args.get('direction')
            query = (
                f"SELECT timetable.id_journey,buses.name AS bus_name, start_city.name AS start_city, finish_city.name AS finish_city, timetable.time_start, timetable.time_finish,timetable.cost FROM timetable "
                f"JOIN cities AS start_city ON timetable.city_start_id = start_city.id_city "
                f"JOIN cities AS finish_city ON timetable.city_finish_id = finish_city.id_city "
                f"JOIN buses ON timetable.bus_id = buses.id_bus ")
            if request.args.get('citystart') == "Відправляємся з":
                pass
            elif request.args.get('citystart'):
                citystart = request.args.get('citystart')
                query += f" WHERE start_city.name LIKE '{citystart}'"
            if request.args.get('cityfinish')=="Їдем в":
                pass
            elif request.args.get('cityfinish'):
                cityfinish = request.args.get('cityfinish')
                query += f" AND finish_city.name LIKE '{cityfinish}'"
            if request.args.get('starttime') and request.args.get('finishtime'):
                starttime = request.args.get('starttime')
                finishtime = request.args.get('finishtime')

                starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M')
                finishtime = datetime.strptime(finishtime, '%Y-%m-%dT%H:%M')

                query += f" AND timetable.time_start BETWEEN '{starttime}' AND '{finishtime}'"

            if item_sort == "Назва автобусу":
                query += " ORDER BY bus_name"
            elif item_sort == "За іменем міста відправлення":
                query += " ORDER BY start_city"
            elif item_sort == "За іменем міста прибуття":
                query += " ORDER BY finish_city"
            elif item_sort == "За часом відправлення":
                query += " ORDER BY time_start"
            elif item_sort == "За часом прибуття":
                query += " ORDER BY time_finish"
            else:
                return render_template('Error', 500)

            if direction == "По спаданню":
                query += " DESC"
            elif direction == "По зростанню":
                query += " ASC"

            table = db_context.get_items(JourneysTable(), newquery=query)
            cities = db_context.get_items(Cities())
            return render_template("journeys.html", user=GetFromDict(), table=table, cities=cities)

    except Exception as e:
       print(f"An error occurred: {str(e)}")

    buses = db_context.get_items(Buses())
    journeys = db_context.get_items(Timetable())
    cities = db_context.get_items(Cities())
    return render_template("journeys.html", user=GetFromDict(), buses=buses, journeys=journeys, cities=cities, table=None)


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
            else:
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


@app.route('/addbus', methods=['POST','GET'])
def addbus():
    if request.method=="GET":
        if GetFromDict() is not None:
            return render_template("addbus.html", info=None)
        else:
            return redirect("/home")
    if request.method=="POST":
        bus=Buses()
        bus.name=str(request.form['nameBus'])
        bus.seats=str(request.form['seats'])
        bus.bus_number=str(request.form['busNumber'])
        if db_context.add_item(bus):
            return render_template("addbus.html", info=None)
        else:
            return render_template("addbus.html", info="Не додано")

@app.route('/addcity', methods=['POST','GET'])
def addcity():
    if request.method=="GET":
        if GetFromDict() is not None:
            return render_template("addcity.html", info=None)
        else:
            return redirect("/home")
    if request.method=="POST":
        city=Cities()
        city.name=str(request.form['nameCity'])
        city.country=str(request.form['country'])
        if db_context.add_item(city):
            return render_template("addcity.html", info=None)
        else:
            return render_template("addcity.html", info="Не додано")


@app.route('/addjourney', methods=['POST', 'GET'])
def addjourney():
    if request.method == "GET":
        if GetFromDict() is not None:
            cities = db_context.get_items(Cities())
            buses = db_context.get_items(Buses())
            return render_template("addjourney.html", info=None, buses=buses, cities=cities)
        else:
            return redirect("/home")

    if request.method == "POST":
        journey = Timetable()
        journey.bus_id = int(request.form['idbus'])
        journey.city_start_id = int(request.form['idcitystart'])
        journey.city_finish_id = int(request.form['idcityfinish'])
        journey.cost = float(request.form['cost'])
        journey.time_start = datetime.strptime(request.form['timestart'], '%Y-%m-%dT%H:%M')
        journey.time_finish = datetime.strptime(request.form['timefinish'], '%Y-%m-%dT%H:%M')
        journey.seats_occupied=int(request.form['seats_occupied'])
        cities = db_context.get_items(Cities())
        buses = db_context.get_items(Buses())
        if db_context.add_item(journey):
            return render_template("addjourney.html", info=None, buses=buses, cities=cities)
        else:
            return render_template("addjourney.html", info="Не додано", buses=buses, cities=cities)


@app.route('/addadmin', methods=['POST', 'GET'])
def addadmin():
    if request.method == "GET":
        if GetFromDict() is not None:
            return render_template("addadmin.html", info=None)
        else:
            return redirect("/home")

    if request.method == "POST":
        user = Clients()
        user.name=str(request.form['name'])
        user.email=str(request.form['email'])
        user.phone=str(request.form['phone'])
        user.password=str(request.form['password'])
        user.role_client='admin'
        if db_context.add_item(user):
            return render_template("addadmin.html", info=None)
        else:
            return render_template("addadmin.html", info="Не додано")


#@app.route('/killuser', methods=['POST', 'GET'])
#def killuser():
#    if request.method == "GET":
#        if GetFromDict() is not None:
#            return render_template("killuser.html", user=GetFromDict(), info=None)
#        else:
#            return redirect("/home")
#
#    if request.method == "POST":
#
#        if db_context.delete_item():
#            return render_template("killuser.html", user=GetFromDict(), info=None)
#        else:
#            return render_template("killuser.html", user=GetFromDict(), info="Не додано")

@app.route('/update', methods=['POST','GET'])
def update():
    if request.method=="GET":
        if GetFromDict():
            if GetFromDict().role_client == "admin":
                return render_template("update.html")
        else:
            return redirect("/home")
    if request.method=="POST":
        selected_radio = request.form.get('listGroupCheckableRadios')

        if selected_radio == "bus":
            bus=Buses()
            fieldlist=GetClassFields(bus)
            return render_template("updatewhatrecord.html", fieldlist=fieldlist,clas=bus)
        elif selected_radio == "journey":
            journey=Timetable()
            fieldlist = GetClassFields(journey)
            return render_template("updatewhatrecord.html", fieldlist=fieldlist,clas=journey)
        elif selected_radio == "city":
            city=Cities()
            fieldlist = GetClassFields(city)
            return render_template("updatewhatrecord.html", fieldlist=fieldlist,clas=city)
        elif selected_radio == "ticket":
            tick=Tickets()
            fieldlist = GetClassFields(tick)
            return render_template("updatewhatrecord.html", fieldlist=fieldlist,clas=tick)

        return redirect("/adminpanel")


@app.route('/updatewhatrecord', methods=['POST', 'GET'])
def updatewhatrecord():
    if request.method == "GET":
        if GetFromDict() is not None:
            if GetFromDict().role_client == "admin":
                return render_template("updatewhatrecord.html")
        else:
            return redirect("/home")
    elif request.method == "POST":
        clas = request.args.get('clas')
        selected_radio = request.form.get('listGroupCheckableRadios')

        return render_template("updatepost.html" ,dict=dict)


@app.route('/updatepost/<selectedfield>/<clas>', methods=['POST', 'GET'])
def updatepost(selectedfield, clas):
    if request.method == "GET":
        if GetFromDict() is not None:
            if GetFromDict().role_client == "admin":
                ss = selectedfield
                return render_template("updatepost.html", selectedfield=ss, clas=clas, info=None)
        else:
            return redirect("/home")

    if request.method == "POST":
        item = selectedfield
        value = request.form['value']
        type=request.form['type']
        id = request.form['id']

        try:
            obj_class = globals()[clas]
            obj = obj_class()
        except KeyError:
            return render_template("updatepost.html", selectedfield=selectedfield, clas=clas,
                                   info="Не вдалося знайти клас")
        try:
            if type == "datetime":
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M')
        except ValueError:
            return render_template("updatepost.html", selectedfield=selectedfield, clas=clas,
                                   info="Помилка конвертації у формат дати/часу")
        try:
            if type == "int":
                value = int(value)
        except ValueError:
            return render_template("updatepost.html", selectedfield=selectedfield, clas=clas,
                                   info="Помилка конвертації у формат int")

        if db_context.update_item(id, item, value, obj):
            return render_template("adminpanel.html")
        else:
            return render_template("updatepost.html", selectedfield=selectedfield, clas=clas, info="Не оновлено")


@app.route('/adminpanel')
def adminpanel():
    if GetFromDict():
        user = GetFromDict()
        if user.role_client == "admin":
            return render_template("adminpanel.html", user=user)
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


def GetClassFields(obj):
     return list(obj.__dict__.keys())


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
