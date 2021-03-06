import db
import utilities
import time
from googleapiclient.discovery import build


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


def perform_a_query(from_city, to_city, date_depart, date_return, solutions=5):
    body = build_request_body(from_city, to_city, date_depart, date_return, solutions)
    api_key = utilities.fetch_api_key(file_name='qpxExpress.key')
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
    # Fetch current day as the query date, formatted output of time, e.g. 2017-02-01:08
    if 8 <= int(time.strftime('%H')) < 20:
        query_time = time.strftime('%Y-%m-%d (morning)')
    else:
        query_time = time.strftime('%Y-%m-%d (night)')

    ticket_fare_db.insert_an_entry(table_name='LOWESTTICKETFARE',
                                   from_city=from_city,
                                   to_city=to_city,
                                   depart_code=choice_list[0]['depart'],
                                   return_code=choice_list[0]['return'],
                                   depart_date=date_depart,
                                   return_date=date_return,
                                   query_time=query_time,
                                   fare=choice_list[0]['price'])

    for choice in choice_list:
        # print choice['depart'], choice['return'], choice['price']
        ticket_fare_db.insert_an_entry(table_name='TICKETFARE',
                                       from_city=from_city,
                                       to_city=to_city,
                                       depart_code=choice['depart'],
                                       return_code=choice['return'],
                                       depart_date=date_depart,
                                       return_date=date_return,
                                       query_time=query_time,
                                       fare=choice['price'])

    is_lowest = ticket_fare_db.is_lowest_fare(from_city=from_city,
                                  to_city=to_city,
                                  depart_date=date_depart,
                                  return_date=date_return)
    ticket_fare_db.db_close()
    return [query_time, choice_list[0]['depart'], choice_list[0]['return'], choice_list[0]['price'], is_lowest]


if __name__ == "__main__":
    date_depart = "2017-09-15"
    date_return = "2017-10-03"
    print "Shanghai"
    print date_depart, date_return
    perform_a_query('MUC', 'PVG', date_depart, date_return, solutions=5)

    print "Beijing"
    print date_depart, date_return
    perform_a_query('MUC', 'PEK', date_depart, date_return, solutions=5)

