import pyodbc
from ClassLib.buses import Buses
from ClassLib.clients import Clients


class DbContext:
    def __init__(self):
        self.conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-TSMTSMN;DATABASE=avtovokzal;Trusted_Connection=yes")
        self.cursor = self.conn.cursor()

    def get_items(self, other_class_instance):
        array_items = list(other_class_instance.__dict__.keys())
        table = other_class_instance.__class__.__name__
        query = f"SELECT {', '.join(array_items)} FROM {table}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            bus_instance = Buses()
            for idx, item in enumerate(array_items):
                value = row[idx]
                setattr(bus_instance, item, value if value is not None else "")
            result.append(bus_instance)
        return result

    def get_item_by_id(self, other_class_instance, item_id):
        array_items = list(other_class_instance.__dict__.keys())
        table = other_class_instance.__class__.__name__

        for item in array_items:
            if item.startswith("id"):
                id_class_name = item
                break

        query = f"SELECT {', '.join(array_items)} FROM {table} WHERE {id_class_name} = ?"

        self.cursor.execute(query, (item_id,))

        row = self.cursor.fetchone()

        if row:
            bus_instance = Buses()
            for idx, item in enumerate(array_items):
                value = row[idx]
                setattr(bus_instance, item, value if value is not None else "")
            other_class_instance=bus_instance

        return other_class_instance

    def add_item(self,obj):

        db_context=DbContext()
        db_context.select_last_index(obj)

        array_items = list(obj.__dict__.keys())
        non_id_items = [item for item in array_items if not item.startswith("id")]
        values = ', '.join([f"'{obj.__dict__[item]}'" for item in non_id_items])
        query = f"INSERT INTO {obj.__class__.__name__} ({', '.join(non_id_items)}) VALUES ({values})"

        try:
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Item added successfully to {obj.__class__.__name__} table.")
            return True
        except Exception as e:
            print(f"Error adding item to {obj.__class__.__name__} table: {str(e)}")
            return False

    def select_last_index(self,obj):
        array_items = list(obj.__dict__.keys())
        for item in array_items:
            if item.startswith("id"):
                id_class_name = item
                break

        query = f"SELECT MAX({str(id_class_name)}) FROM {obj.__class__.__name__}"

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()[0]
            return result if result is not None else 0
        except Exception as e:
            print(f"Error getting last index from {obj.__class__.__name__}: {str(e)}")
            return 0







db_context = DbContext()

bus=Buses()
buses=db_context.get_items(bus)



#clientx= db_context.get_item_by_id(clientx,4)
#bus =db_context.get_item_by_id(bus,3)

#for idx, client in enumerate(clients_list):
    #print(f"ID: {client.id_client}, Name: {client.name}, phone: {client.phone},  email: {client.email}")
#print(f"IDX: {clientx.id_client}, Name: {clientx.name}, phone: {clientx.phone},  email: {clientx.email}")


for idx, bus in enumerate(buses):
    print(f"ID: {bus.id_bus}, Name: {bus.name}, Seats: {bus.seats}, Bus Number: {bus.bus_number}")


