import time
import sqlite3
import firebase_admin
from firebase_admin import db, credentials 


def connect_firebase(
    crendetial_file: str = "credentials/firebase_config.json", 
    database_reference: str = "/Hasil_Pembacaan",
    database_url: str = "https://aeroponik-e5dd4-default-rtdb.firebaseio.com/"
    ):
    credential = credentials.Certificate(crendetial_file)
    firebase_admin.initialize_app(
        credential, 
        {"databaseURL" : database_url}
    )
    data = db.reference(database_reference)
    return data

def connect_table(
    database_path: str = "db/data_iot.db"
    ):
    connection = sqlite3.connect(database_path)
    return connection

def create_table():
    try:
        connection = connect_table()
        connection.execute(
            """
            CREATE TABLE iot_data
            (
                datetime BLOB NOT NULL,
                tds BLOB NOT NULL, 
                jarak BLOB NOT NULL,
                kelembaban BLOB NOT NULL,
                suhu BLOB NOT NULL
            );
            """
        )
        connection.commit()
        connection.close()
    except Exception as E:
        print(E)
        pass

def insert_table(
    timestamp,
    params: dict = {}
    ):
    connection = connect_table()
    cursor = connection.cursor()
    data_params = (
        timestamp,
        params["TDS"],
        params["jarak"],
        params["kelembaban"],
        params["suhu"],
    )
    cursor.execute(
        "INSERT INTO iot_data VALUES (?, ?, ?, ?, ?)",
        data_params
    )
    connection.commit()
    connection.close()

def get_table():
    connection = connect_table()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM iot_data")
    data = cursor.fetchall()
    return data

def run_ingest():
    create_table()
    data_firebase = connect_firebase()
    print("[*] Waiting Data...")
    counted_data = 1
    while True:
        try:
            data = data_firebase.get()
            insert_table(time.time(), data)
            print(f'[*] Success Insert {counted_data} Data')
            counted_data += 1
            time.sleep(15)
        except Exception as E:
            print(E)
            pass

# if __name__ == "__main__":
#     run_ingest()
    # get_table()