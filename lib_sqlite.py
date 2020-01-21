#!/usr/bin/python
from lib_logs import PrintMsg
from config import DB_PATH
import sqlite3
import json

def DatabaseInit():
    '''Initialize the database
    it will connect to data.db,
    and try drop CURRENT_DEVICES table,
    then create new one.

    Return:
        return false if error ocurred
    '''

    try:
        conn = sqlite3.connect(DB_PATH)
        PrintMsg("Opened database successfully")
    except:
        PrintMsg("database open failed")
        return False

    try:
        c = conn.cursor()
        c.execute("DROP TABLE CURRENT_DEVICES;")
        PrintMsg("Table CURRENT_DEVICES DROP successfully!")
        conn.commit()
    except:
        PrintMsg("Table CURRENT_DEVICES was not found,creating one now...")
    
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE CURRENT_DEVICES
            (   CID         VARCHAR(50) PRIMARY KEY   NOT NULL,
                IPV4        VARCHAR(50)               NULL,
                MAC         VARCHAR(50)               NULL,
                DEVICE_NAME VARCHAR(50)               NULL,
                OS          VARCHAR(50)               NULL,
                CPU         VARCHAR(50)               NULL,
                MEM         DOUBLE                    NULL,
                CPU_USAGE   DOUBLE                    NULL,
                MEM_REMAIN  DOUBLE                    NULL,
                USER_NAME   VARCHAR(50)               NULL,
                APPS        JSON                      NULL,
                PROCESS     JSON                      NULL
                );''')
        PrintMsg("Table CURRENT_DEVICES created successfully!")
        conn.commit()
    except:
        PrintMsg("Table CURRENT_DEVICES create faild!")
        return False
    conn.close()


def UpdateClientStatus(data):
    '''Update Client's data to MySQLite Table CURRENT_DEVICES
    Args:
        data: json format,parse from srv_cocket.py
    Return:
        retrun False if error occured
    '''

    cid = data["cid"]
    ipv4 = data["ipv4"]
    mac = data["mac"]
    device_name = data["device_name"]
    os = data["os"]
    cpu = data["cpu"]
    mem = data["mem"]
    cpu_usage = data["cpu_usage"]
    mem_remain = data["mem_remain"]
    user_name = data["user_name"]
    apps = json.dumps(data["apps"])
    process = json.dumps(data["process"])

    stored = False

    #connect to DB
    try:
        conn = sqlite3.connect(DB_PATH)
    except:
        PrintMsg("Fail to open database!(UpdateClientStatus)")
        return False
    
    #check if client's data inserted.
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM CURRENT_DEVICES WHERE CID = '{cid}'")
        results = c.fetchall()
        if len(results) > 0: stored = True
    except:
        print("Error: unable to fecth data")
        conn.close()
        return False
    
    #if client's data stored, update it.
    if stored:
        try:
            c = conn.cursor()
            c.execute(f"""UPDATE CURRENT_DEVICES SET
            IPV4 = '{ipv4}',
            MAC = '{mac}',
            DEVICE_NAME = '{device_name}',
            OS = '{os}',
            CPU = '{cpu}',
            MEM = {mem},
            CPU_USAGE = {cpu_usage},
            MEM_REMAIN = {mem_remain},
            USER_NAME = '{user_name}',
            APPS = '{apps}',
            PROCESS = '{process}' WHERE CID = '{cid}'
            ;""")
            PrintMsg(f"updated {cid}'s data to CURRENT_DEVICES.")
            conn.commit()
        except Exception as e:
            PrintMsg(f"update {cid}'s data to CURRENT_DEVICES faild!")
            PrintMsg("ERROR: " + str(e))
            conn.close()
            return False
    
    #if client's data is not stored,insert it.
    if stored is False:
        try:
            c = conn.cursor()
            c.execute(f"""INSERT INTO CURRENT_DEVICES
            (CID,IPV4,MAC,DEVICE_NAME,OS,CPU,MEM,CPU_USAGE,MEM_REMAIN,USER_NAME,APPS,PROCESS) VALUES 
            ('{cid}','{ipv4}','{mac}','{device_name}','{os}','{cpu}',{mem},{cpu_usage},{mem_remain},'{user_name}','{apps}','{process}');
            """)
            PrintMsg(f"Insert {cid}'s data to CURRENT_DEVICES successfully!")
            conn.commit()
        except Exception as e:
            PrintMsg(f"Insert {cid}'s data to CURRENT_DEVICES create faild!")
            PrintMsg("ERROR: " + str(e))
            conn.close()
            return False
    conn.close()

    