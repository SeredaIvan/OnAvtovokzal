import pyodbc
from ClassLib.buses import Buses
from ClassLib.clients import Clients
from ClassLib.tickets import Tickets

from ClassLib.timetable import Timetable


class DbContext:
    def __init__(self):
        self.conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-TSMTSMN;DATABASE=avtovokzal;Trusted_Connection=yes")
        self.cursor = self.conn.cursor()

    def get_items(self, other_class_instance, newquery=""):
        array_items = list(other_class_instance.__dict__.keys())
        table = other_class_instance.__class__.__name__
        query = f"SELECT {', '.join(array_items)} FROM {table}"

        if newquery != "":
            query = newquery
        print(query)
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            result = []

            if rows:
                for row in rows:
                    instance = other_class_instance.__class__()
                    for idx, item in enumerate(array_items):
                        value = row[idx]
                        setattr(instance, item, value if value is not None else "")
                    result.append(instance)
                print("Item Get succes")
                return result
            else:
                return None
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None

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
        instance = None
        if row:
            instance = other_class_instance.__class__()
            for idx, item in enumerate(array_items):
                value = row[idx]
                setattr(instance, item, value if value is not None else None)

        return instance

    def add_item(self, obj):
        db_context = DbContext()
        db_context.select_last_index(obj)

        array_items = list(obj.__dict__.keys())
        non_id_items = [item for item in array_items if not item.startswith("id")]

        values = ', '.join(
            [f"'{obj.__dict__[item]}'" if obj.__dict__[item] != None else "NULL" for item in non_id_items])

        query = f"INSERT INTO {obj.__class__.__name__} ({', '.join(non_id_items)}) VALUES ({values})"
        print(query)

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

    def get_item_by_other_value(self, other_class_instance, item, value):
        array_items = list(other_class_instance.__dict__.keys())
        table = other_class_instance.__class__.__name__

        query = f"SELECT * FROM {table} WHERE {item} = ?"
        self.cursor.execute(query, (value,))

        row = self.cursor.fetchone()

        if row:
            new_instance = type(other_class_instance)()
            for idx, attribute in enumerate(array_items):
                setattr(new_instance, attribute, row[idx] if row[idx] is not None else "")

            return new_instance

        return None

    def get_items_by_other_value(self, other_class_instance, item, value):
        try:
            array_items = list(other_class_instance.__dict__.keys())
            table = other_class_instance.__class__.__name__

            query = f"SELECT * FROM {table} WHERE {item} = ?"
            self.cursor.execute(query, (value,))

            rows = self.cursor.fetchall()

            result = []
            if rows:
                for row in rows:
                    instance = other_class_instance.__class__()
                    for idx, item_name in enumerate(array_items):
                        item_value = row[idx]
                        print(item_value)
                        setattr(instance, item_name, item_value if item_value is not None else "")
                    result.append(instance)
                print("Items retrieved successfully")
                return result
            else:
                return None
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None

    def get_user(self, password, item, value):
        query = f"SELECT * FROM clients WHERE {str(item)} = ?"
        self.cursor.execute(query, (str(value),))
        row = self.cursor.fetchone()
        if row:
            user = Clients()
            attributes = list(user.__dict__.keys())
            for attribute, row_value in zip(attributes, row):
                setattr(user, attribute, row_value if row_value is not None else "")
            print(str(user.id_client)+" "+user.name+" "+user.phone+" "+user.password+" "+user.email)
            if user.password == password:
                print("User authorized")
                print("Row values:", row)
                return user
            else :
                print("incorect password")
                return "Пароль не співпадає"

        print("None account")
        return None

    def update_item(self, id, item, value, obj):
        nametable = obj.__class__.__name__

        if nametable=="Buses":
            name_id='id_bus'
        elif nametable=="Clients":
            name_id='id_client'
        elif nametable=="Timetable":
            name_id='id_journey'
        elif nametable == "Cities":
            name_id = 'id_city'
        elif nametable == "Non_autorized_users":
            name_id = 'id_user'
        elif nametable == "Non_autorized_users":
            name_id = 'id_user'
        elif nametable == "Orders":
            name_id = 'id_order'
        elif nametable == "Tickets":
            name_id = 'id_ticket'
        else:
            print("Не підтримуємий клас")
            print("err on DBContext at 158 line")
            return False

        query = f"UPDATE {nametable} SET {item}=? WHERE {name_id}=?"
        values = (value, id)

        try:
            with self.conn:
                with self.cursor.execute(query, values):
                    print(f"Update successful for {item} with value {value} for record with {name_id}={id} in table {nametable}.")
                    return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    def delete_item(self, obj, item, value):
        nametable = obj.__class__.__name__
        query = f"DELETE FROM {nametable} WHERE {item} = ?"
        values = (value,)

        try:
            with self.conn:
                with self.cursor.execute(query, values):
                    print(f"Delete successful from {nametable} where {item} = {value}.")
        except Exception as e:
            print(f"Error deleting record: {e}")



