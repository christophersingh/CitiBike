import mysql.connector
import warnings
warnings.filterwarnings("ignore") 

from DBConnect import DBConnect

from collections import namedtuple

def retrieve_by_kiosk(kioskID):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "SELECT * from bikekiosk where kioskID = "+ str(kioskID)
      cursor.execute(query)  
      #print(cursor.statement)
      row = cursor.fetchone()
      if row is None:
        kiosk = None
      else:
        kiosk = build_kiosk(row)
      cursor.close()
      conn.close()
      return kiosk
    except mysql.connector.Error as e:
      print(e)
      return None

def getBikeCountByKiosk(kioskID):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "Select count(*) from bike where atKiosk = 'y' and currentKioskID = "+ str(kioskID)
      cursor.execute(query)  
      #print(cursor.statement)
      row = cursor.fetchone()
      result = (row['count(*)'])
      cursor.close()
      conn.close()
      return result
    except mysql.connector.Error as e:
      print(e)
      return None

def build_kiosk(row):
    Kiosk = namedtuple('Kiosk', ['kisokID', 'addr1', 'addr2', 'city', 'stat', 'zip', 'capacity', 'maxcapacity'])
    curr_Bike = Kiosk(row['kioskID'], row['addr1'], row['addr2'],
                          row['city'], row['stat'], row['zip'], row['capacity'], row['maxcapacity'])
    return curr_Bike




