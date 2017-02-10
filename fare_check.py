import db
import matplotlib.pyplot as plt


def find_cheapest_fare(from_city, to_city, depart_date, return_date):
    ticket_fare_db = db.TicketFareDatabase()
    ticket_fare_db.db_connect()
    ticket_fare_db.insert_lowest_fare(from_city, to_city, depart_date, return_date)


def plot_fare_curve():
    pass


def fare_warning_check():
    pass


if __name__ == "__main__":
    pass