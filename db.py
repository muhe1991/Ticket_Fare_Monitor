import sqlite3
import os
import pandas as pd
import time

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
        QUERY_TIME  CHAR(20)                NOT NULL,
        FARE        REAL                    NOT NULL);''')

        self.db_conn.execute('''CREATE TABLE LOWESTTICKETFARE
        (FROM_CITY       CHAR(10)                NOT NULL,
        TO_CITY         CHAR(10)                NOT NULL,
        DEPART_CODE CHAR(15)                NOT NULL,
        RETURN_CODE CHAR(15)                NOT NULL,
        DEPART_DATE CHAR(20)                NOT NULL,
        RETURN_DATE CHAR(20)                NOT NULL,
        QUERY_TIME  CHAR(20)                NOT NULL,
        FARE        REAL                    NOT NULL);''')

    def db_connect(self):
        if os.path.isfile('%s.db' % self.db_name):
            self.db_conn = sqlite3.connect('%s.db' % self.db_name)
        else:
            self.db_conn = sqlite3.connect('%s.db' % self.db_name)
            self.db_init()

    def insert_an_entry(self, table_name, from_city, to_city, depart_code, return_code,
                        depart_date, return_date, query_time, fare):
        # Check if a query exists
        df = pd.read_sql_query('''SELECT * FROM %s WHERE
                                  FROM_CITY = '%s' AND
                                  TO_CITY = '%s' AND
                                  DEPART_CODE = '%s' AND
                                  RETURN_CODE = '%s' AND
                                  DEPART_DATE = '%s' AND
                                  RETURN_DATE = '%s' AND
                                  QUERY_TIME = '%s' AND
                                  FARE = %s
                                ''' % (table_name, from_city, to_city, depart_code, return_code,
                                       depart_date, return_date, query_time, fare), self.db_conn)
        if len(df) == 0:
            self.db_conn.execute("INSERT INTO %s (FROM_CITY, TO_CITY, DEPART_CODE, RETURN_CODE, DEPART_DATE, RETURN_DATE, QUERY_TIME, FARE) \
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)" % table_name,
                                 (from_city, to_city, depart_code, return_code, depart_date, return_date, query_time, fare))
            print "Records created successfully"
        else:
            print "WARNING: Entry exists, abandon insert."

        self.db_conn.commit()

    def db_close(self):
        self.db_conn.close()

    def db_output(self):
        cursor = self.db_conn.execute("SELECT FROM_CITY, TO_CITY, DEPART_CODE, RETURN_CODE, QUERY_TIME, FARE from TICKETFARE")
        for row in cursor:
            print "FROM = ", row[0]
            print "TO = ", row[1]
            print "DEPART = ", row[2]
            print "RETURN = ", row[3]
            print "FARE = ", row[5], "\n"

    def insert_lowest_fare(self, from_city, to_city, depart_date, return_date):
        cursor = self.db_conn.execute("SELECT * FROM TICKETFARE WHERE FROM_CITY=%s AND TO_CITY=%s AND DEPART_DATE=%s AND RETURN_DATE=%s"
                                      % (from_city, to_city, depart_date, return_date))
        df = pd.read_sql_query("select * from TICKETFARE where FROM_CITY=%s AND TO_CITY=%s AND DEPART_DATE=%s AND RETURN_DATE=%s"
                               % (from_city, to_city, depart_date, return_date), self.db_conn)

        lowest_fare_entry = df.loc[df['FARE'].idxmax()]

        self.insert_an_entry(table_name='LOWESTTICKETFARE',
                             city_from=lowest_fare_entry['FROM_CITY'],
                             city_to=lowest_fare_entry['TO_CITY'],
                             code_depart=lowest_fare_entry['DEPART_CODE'],
                             code_return=lowest_fare_entry['RETURN_CODE'],
                             depart_date=lowest_fare_entry['DEPART_DATE'],
                             return_date=lowest_fare_entry['RETURN_DATE'],
                             query_time=lowest_fare_entry['QUERY_TIME'],
                             fare=lowest_fare_entry['FARE'])

    def is_lowest_fare(self, from_city, to_city, depart_date, return_date):

        df = pd.read_sql_query('''SELECT * FROM LOWESTTICKETFARE WHERE
                                  from_city = '%s' AND
                                  to_city = '%s' AND
                                  depart_date = '%s' AND
                                  return_date = '%s'
                                ''' % (from_city, to_city, depart_date, return_date), self.db_conn)

        lowest = df.loc[df['FARE'].idxmin()]

        if 8 <= int(time.strftime('%H')) < 20:
            query_time = time.strftime('%Y-%m-%d (morning)')
        else:
            query_time = time.strftime('%Y-%m-%d (night)')

        if lowest['QUERY_TIME'] == query_time:
            return True
        else:
            df = pd.read_sql_query('''SELECT * FROM LOWESTTICKETFARE WHERE
                                              from_city = '%s' AND
                                              to_city = '%s' AND
                                              depart_date = '%s' AND
                                              return_date = '%s' AND
                                              query_time = '%s'
                                            ''' % (from_city, to_city, depart_date, return_date, query_time), self.db_conn)
            newest = df.ix[0]
            if lowest['FARE'] == newest['FARE']:
                return True

            else:
                return False


if __name__ == "__main__":
    ticket_fare_db = TicketFareDatabase()
    ticket_fare_db.db_connect()
    ticket_fare_db.db_output()
    ticket_fare_db.db_close()


