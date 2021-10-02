#!/usr/bin/env python3
# NOTE: tried using selenium originally but found the api call directly which was easier.
# Info found here: https://medium.com/ml-book/web-scraping-using-selenium-python-3be7b8762747
import requests
import sys
import time
from datetime import datetime

from send_message import send_msg

def parse_date(date):
    if len(date) != 9:
        raise Exception("can't parse this date")

    return (date[:4], date[4:6], date[6:8])

def get_staff_ids():
    staff_ids = {}

    response = requests.get('https://www.genbook.com/bookings/api/serviceproviders/30050910/services/272408692/resources?=&size=100&page=1')
    json = response.json()
    staff_info = json['resources']
    for staff in staff_info:
        staff_ids[str(staff['id'])] = staff['name']

    return staff_ids

def get_earliest_opening(staff_id):
    response = requests.get(f'https://www.genbook.com/bookings/api/serviceproviders/30050910/services/272408692/resources/{staff_id}')
    json = response.json()
    open_dates = json['bookingdates']
    
    earliest_opening = open_dates[0]
    
    return earliest_opening

def main():
    if len(sys.argv) < 2:
        raise Exception('You must run this program like this: python3 alert.py YYYYMMDD, where YYYYMMDD is your current appointment.')
    
    current_appt = parse_date(sys.argv[1]+'L')

    while True:
        staff_ids = get_staff_ids()

        openings = []
        for id in staff_ids:
            date = parse_date(get_earliest_opening(id))
            openings.append((date, id))
        
        sorted_openings = sorted(openings)
        earliest_opening = sorted_openings[0]
        date = earliest_opening[0]
        id = earliest_opening[1]

        if date < current_appt:
            message = \
f"""There is an available GT HR appointment on {date[1]}/{date[2]}/{date[0]} with {staff_ids[id]}.
Your current appointment is {current_appt[1]}/{current_appt[2]}/{current_appt[0]}.
https://www.genbook.com/bookings/slot/reservation/30050910/272408692/{id}/{date[0]}{date[1]}{date[2]}?bookingSourceId=1000&ds=1"""
            send_msg(message)
            
            with open('/home/justin/Documents/gatech-hr-alerts/log.txt', 'a') as out:
                out.write(f'{datetime.now()}: Sent text message with message: {message}\n\n')
        time.sleep(60)

if __name__ == '__main__':
    main()
