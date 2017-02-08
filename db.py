import sqlite3
import os

# conn = sqlite3.connect('test.db')
#
# print "successfully"
#
#
# conn.execute('''CREATE TABLE COMPANY
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        AGE            INT     NOT NULL,
#        ADDRESS        CHAR(50),
#        SALARY         REAL);''')
# print "Table created successfully";
# conn.close()
#
#
# def init_database(db_name):
#     db_conn = sqlite3.connect(db_name)


class TicketFareDatabase(object):

    def __init__(self):
        self.db_name = "ticket_fare_database"
        self.db_conn = None

    def db_init(self):
        self.db_conn.execute('''CREATE TABLE TICKETFARE
        (FROM_CITY       CHAR(10)                NOT NULL,
        TO_CITY         CHAR(10)                NOT NULL,
        DEPART_CODE CHAR(15)                NOT NULL,
        RETURN_CODE CHAR(15)                NOT NULL,
        DEPART_DATE CHAR(20)                NOT NULL,
        RETURN_DATE CHAR(20)                NOT NULL,
        QUERY_DATE  CHAR(20)                NOT NULL,
        FARE        REAL                    NOT NULL);''')
        print 'i'

    def db_connect(self):
        if os.path.isfile('%s.db' % self.db_name):
            self.db_conn = sqlite3.connect('%s.db' % self.db_name)
        else:
            self.db_conn = sqlite3.connect('%s.db' % self.db_name)
            self.db_init()

    def insert_an_entry(self, city_from, city_to, code_depart, code_return,
                        date_depart, date_return, date_query, fare):
        self.db_conn.execute("INSERT INTO TICKETFARE (FROM_CITY, TO_CITY, DEPART_CODE, RETURN_CODE, DEPART_DATE, RETURN_DATE, QUERY_DATE, FARE) \
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                             (city_from, city_to, code_depart, code_return, date_depart, date_return, date_query, fare))
        self.db_conn.commit()
        print "Records created successfully";

    def db_close(self):
        self.db_conn.close()

    def db_output(self):
        cursor = self.db_conn.execute("SELECT FROM_CITY, TO_CITY, DEPART_CODE, RETURN_CODE, QUERY_DATE, FARE from TICKETFARE")
        for row in cursor:
            print "FROM = ", row[0]
            print "TO = ", row[1]
            print "DEPART = ", row[2]
            print "RETURN = ", row[3]
            print "FARE = ", row[5], "\n"


if __name__ == "__main__":
    ticket_fare_db = TicketFareDatabase()
    ticket_fare_db.db_connect()
    ticket_fare_db.db_output()
    ticket_fare_db.db_close()
