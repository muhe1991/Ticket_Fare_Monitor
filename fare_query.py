import json
import db
import os
import time
from googleapiclient.discovery import build


def fetch_api_key(file_name):
    """
    Fetch the API key from the key file, which is not supposed to be public
    :param file_name:
    :return:
    """
    if os.path.isfile(file_name):
        f = open(file_name)
        api_key = f.read()
        f.close()
        return api_key
    else:
        print "ERROR: Path file is missing."
        return None


def build_request_body(origin, destination, depart_date, return_date, solutions):
    body = {
      "request": {
        "slice": [
          {
            "origin": origin,
            "destination": destination,
            "date": depart_date,
            "maxStops": 0,
            "preferredCabin": "COACH"
          },
          {
            "origin": destination,
            "destination": origin,
            "date": return_date,
            "maxStops": 0,
            "preferredCabin": "COACH"
          }
        ],
        "passengers": {
          "adultCount": 1,
          "infantInLapCount": 0,
          "infantInSeatCount": 0,
          "childCount": 0,
          "seniorCount": 0
        },
        "solutions": solutions,
        "refundable": False
      }
    }
    return body


def perform_a_query(origin, destination, date_depart, date_return, solutions=5):
    body = build_request_body(origin, destination, date_depart, date_return, solutions)
    api_key = fetch_api_key(file_name='qpxExpress.key')
    service = build('qpxExpress', 'v1', developerKey=api_key)

    request = service.trips().search(body=body)
    response_string = request.execute()

    js = response_string
    num_entries = len(js['trips']['tripOption'])

    choice_list = []
    for entry_id in range(num_entries):
        choice = dict()
        entry = js['trips']['tripOption'][entry_id]
        choice['price'] = float(entry['saleTotal'][3:])
        flight_depart = entry['slice'][0]['segment'][0]['flight']
        flight_return = entry['slice'][1]['segment'][0]['flight']
        choice['depart'] = flight_depart['carrier'] + flight_depart['number']
        choice['return'] = flight_return['carrier'] + flight_return['number']
        choice_list.append(choice)

    ticket_fare_db = db.TicketFareDatabase()
    ticket_fare_db.db_connect()
    # Fetch current day as the query date, formatted output of time
    date_query = time.strftime('%Y-%m-%d')

    for choice in choice_list:
        print choice['depart'], choice['return'], choice['price']
        ticket_fare_db.insert_an_entry(city_from=origin,
                                       city_to=destination,
                                       code_depart=choice['depart'],
                                       code_return=choice['return'],
                                       date_depart=date_depart,
                                       date_return=date_return,
                                       date_query=date_query,
                                       fare=choice['price'])

    ticket_fare_db.db_close()


if __name__ == "__main__":
    date_depart = "2017-09-15"
    date_return = "2017-10-03"
    print "Shanghai"
    print date_depart, date_return
    perform_a_query('MUC', 'PVG', date_depart, date_return, solutions=5)

    print "Beijing"
    print date_depart, date_return
    perform_a_query('MUC', 'PEK', date_depart, date_return, solutions=5)

