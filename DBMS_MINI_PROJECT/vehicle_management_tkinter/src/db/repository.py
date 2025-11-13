from .connection import connect_db

def fetch_all(query, params=None):
    conn = connect_db()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    cursor.close()
    conn.close()
    return columns, rows

def execute_sql(sql, params=None, multi=False):
    conn = connect_db()
    if not conn:
        return False, "No connection"
    cursor = conn.cursor()
    try:
        if multi:
            for result in cursor.execute(sql, multi=True):
                pass
        else:
            cursor.execute(sql, params or ())
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        cursor.close()
        conn.close()
        return False, str(e)

def get_all_vehicles():
    return fetch_all("SELECT * FROM Vehicles")

def get_vehicle_by_id(vehicle_id):
    return fetch_all("SELECT * FROM Vehicles WHERE Vehicle_ID = %s", (vehicle_id,))

def add_vehicle(vehicle_data):
    sql = "INSERT INTO Vehicles (Brand, Model, Year, Price) VALUES (%s, %s, %s, %s)"
    return execute_sql(sql, vehicle_data)

def update_vehicle(vehicle_id, vehicle_data):
    sql = "UPDATE Vehicles SET Brand = %s, Model = %s, Year = %s, Price = %s WHERE Vehicle_ID = %s"
    return execute_sql(sql, vehicle_data + (vehicle_id,))

def delete_vehicle(vehicle_id):
    sql = "DELETE FROM Vehicles WHERE Vehicle_ID = %s"
    return execute_sql(sql, (vehicle_id,))