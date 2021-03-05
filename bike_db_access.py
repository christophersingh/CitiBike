import mysql.connector
import warnings
warnings.filterwarnings("ignore") 

from DBConnect import DBConnect

from collections import namedtuple
import datetime
 
def retrieve_by_kiosk(kiosk_id, bike_id):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "UPDATE bike, bikekiosk SET bike.atKiosk='n', bikekiosk.capacity = bikekiosk.capacity - 1  WHERE bikekiosk.kioskID = bike.currentKioskID and kioskID= "+ str(kiosk_id)+" and bikeID ="+ str(bike_id)
      cursor.execute(query)
      #print(cursor.statement)
      conn.commit()
      bikes = []
      for row in cursor:
        student = build_bike(row)
        bikes.append(student)
      cursor.close()
      conn.close()
      return True
    except mysql.connector.Error as e:
      print(e)
      return None

def retrieve_by_id(bikeID):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "SELECT * from bike where bikeID = "+ str(bikeID)
      cursor.execute(query)  
      row = cursor.fetchone()
      if row is None:
        student = None
      else:
        student = build_bike(row)
      cursor.close()
      conn.close()
      return student
    except mysql.connector.Error as e:
      print(e)
      return None

def num_bikes_at_kiosk(bikeID):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "Select kioskID, capacity from bikekiosk where kioskID = "+ str(bikeID)
      cursor.execute(query)  
      #print(cursor.statement)
      row = cursor.fetchone()
      if row is None:
        bike = None
      else:
        bike = get_bike(row)
      cursor.close()
      conn.close()
      return bike.capacity
    except mysql.connector.Error as e:
      print(e)
      return None

def build_bike(row):
    Bike = namedtuple('Bike', ['bikeID', 'model', 'currentKioskID', 'timeArrived', 'atKiosk'])
    curr_Bike = Bike(row['bikeID'], row['model'], row['currentKioskID'],
                          row['timeArrived'], row['atKiosk'])
    return curr_Bike

def get_bike(row):
    Bike = namedtuple('Bike', ['kioskID', 'capacity'])
    curr_Bike = Bike(row['kioskID'], row['capacity'])
    return curr_Bike

def update(bikeID, model, kioskID, date, availability):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "UPDATE bike, bikekiosk SET bike.atKiosk='y', bike.timeArrived = NOW(), bikekiosk.capacity = bikekiosk.capacity + 1, bike.currentKioskID = "+ str(kioskID) +" WHERE bikeID = "+ str(bikeID) +  " and bike.currentKioskID = bikekiosk.kioskID;"
      cursor.execute(query)
      conn.commit()
      bikes = []
      for row in cursor:
        student = build_bike(row)
        bikes.append(student)
      cursor.close()
      conn.close()
      return True
    except mysql.connector.Error as e:
      print(e)
      return None
    return True

def get_bike_location(row):
    Bike = namedtuple('Bike', ['bikeID', 'model', 'currentKioskID', 'atKiosk', 'addr1', 'addr2','city','stat','zip'])
    curr_Bike = Bike(row['bikeID'], row['model'], row['currentKioskID'],
                          row['atKiosk'], row['addr1'], row['addr2'], row['city'], row['stat'], row['zip'])
    return curr_Bike

def getBikeLocation(bikeID):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "select bikeID, model, currentKioskID, atKiosk, addr1, addr2, city, stat, zip from bike inner join bikekiosk on bike.currentKioskID = bikekiosk.kioskID where bikeID = "+ str(bikeID)
      cursor.execute(query)  
      row = cursor.fetchone()
      if row is None:
        bike = None
      else:
        bike = get_bike_location(row)
      cursor.close()
      conn.close()
      return bike
    except mysql.connector.Error as e:
      print(e)
      return None

def build_report(row):
    Bike = namedtuple('Bike', ['bikeID', 'model', 'timeArrived', 'addr1', 'addr2','city','stat','zip'])
    curr_Bike = Bike(row['bikeID'], row['model'], row['timeArrived'],
                           row['addr1'], row['addr2'], row['city'], row['stat'], row['zip'])
    return curr_Bike

def showReport(kioskID):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "select bikeID, model, timeArrived, addr1, addr2, city, stat, zip from bikekiosk inner join bike on bikekiosk.kioskID = bike.currentKioskID where kioskID = " + str(kioskID) +" order by bikeID"
      cursor.execute(query)  
      #row = cursor.fetchone()
      bike = []
      for row in cursor:
        entry = build_report(row)
        bike.append(entry)
      cursor.close()
      conn.close()
      return bike
    except mysql.connector.Error as e:
      print(e)
      return None

def build_checkout(row):
    Bike = namedtuple('Bike', ['bikeID', 'model', 'currentKioskID', 'timeArrived'])
    curr_Bike = Bike(row['bikeID'], row['model'], row['currentKioskID'], row['timeArrived'],)
    return curr_Bike

def bike_checkout(kioskID):
    try:
      dbconnect = DBConnect("bikedb")
      conn = dbconnect.connect()
      cursor = conn.cursor(dictionary=True)
      query = "select bikeID, model, currentKioskID, timeArrived from bike where atKiosk = 'y' and currentKioskID = " + str(kioskID)
      cursor.execute(query)  
      print(cursor.statement)
      #row = cursor.fetchone()
      bike = []
      for row in cursor:
        entry = build_checkout(row)
        bike.append(entry)
      cursor.close()
      conn.close()
      return bike
    except mysql.connector.Error as e:
      print(e)
      return None