import mysql.connector
import warnings
warnings.filterwarnings("ignore")
 
# manages a database connection
class DBConnect:
    # create a DBConnect object for the specified database
    def __init__(self, dbname):
        self.dbname = dbname

    # creates a database connection and returns it
    def connect(self):
        cnx = None

        cnx = mysql.connector.connect(user='', password='',
                                          host='',
                                          database=self.dbname)
        if cnx.is_connected:
            pass


        return cnx

