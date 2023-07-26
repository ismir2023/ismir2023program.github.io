import pandas as pd
import pytz
from icalendar import Calendar, Event
from datetime import datetime


def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()


def calendar_csv2ics(in_csv='../miniconf-data/sitedata/events.csv', out_ics='static/calendar/ISMIR_2022.ics'):
    orig_csv = pd.read_csv(in_csv)
    orig_csv = orig_csv.sort_values(by=['uid'])

    color_dict = {
        "Tutorials": "tut",
        "Opening":'open',
        "All Meeting": "all",
        "Poster session": "pos",
        "Meetup": "meet",
        "VMeetup": "vmeet",
        "WiMIR Meetup": "wimir",
        "Music": "mus",
        "Social": "social",
        "Satellite": "sat",
        "Lunch": "lunch",
        "Registration": "registration",
        "Industry": "industry",
        "LBD": "lbd",
        "Awards":'awards',
        }

    cal = Calendar()
    cal.add('prodid', 'ISMIR 2022 calendar')
    cal.add('version', '2.0')
    cal['dtstart'] = datetime(2022,12,4,8,0,0,tzinfo=pytz.timezone('Asia/Kolkata'))

    tut_csv = orig_csv.copy()[orig_csv['category'].isin(["Tutorials"])]
    tut_csv = tut_csv.sort_values(by=['title'])

    for index, event in orig_csv.iterrows():
        e_cal = Event()
        e_date = [int(x) for x in event['start_date'].split('-')]
        e_start_time = [int(x) for x in event['start_time'].split(':')]
        e_end_time = [int(x) for x in event['end_time'].split(':')]
        e_cal.add('uid', int(event['uid']) + 10)
        e_cal.add('dtstamp', datetime(2022,12,4,0,0,0,tzinfo=pytz.timezone('Asia/Kolkata')))

        if event['category'] == "Poster session":
            session_num = event['title'].split()[3]
            e_cal['location'] = f'papers.html?session={session_num}'

        if event['category'] == "LBD":
            session_num = event['title'].replace('(', '').replace(')', '').split()[-1]
            e_cal['location'] = f'lbds.html?session={session_num}'

        if event['category'] == "Industry":
            e_cal['location'] = f'industry.html?session=Platinum'

        elif event['category'] == "Tutorials":
            e_cal['location'] = f'tutorials.html#{event["title"][:2]}'

        elif event['category'] == "Music":
            e_cal['location'] = f'music.html'

        elif event['category'] in ["All Meeting", "Meetup", "VMeetup", "Awards", "WiMIR Meetup", "Social", "Opening"]:
            e_cal['location'] = f'day_{event["day"]}.html#{color_dict[event["category"]]}'

        elif event['category'] == "Satellite":
            e_cal['location'] = event['web_link']

        e_cal.add('summary', "#" + color_dict[event['category']] + ' ' + event['title'])
        e_cal.add('dtstart', datetime(e_date[0], e_date[1], e_date[2],
            e_start_time[0], e_start_time[1], 0, tzinfo=pytz.timezone('Asia/Kolkata')))
        if e_end_time[0] < e_start_time[0]:
            e_cal.add('dtend', datetime(e_date[0], e_date[1], e_date[2] + 1,
                e_end_time[0], e_end_time[1], 0, tzinfo=pytz.timezone('Asia/Kolkata')))
        else:
            e_cal.add('dtend', datetime(e_date[0], e_date[1], e_date[2],
                e_end_time[0], e_end_time[1], 0, tzinfo=pytz.timezone('Asia/Kolkata')))

        cal.add_component(e_cal)

    with open(out_ics, 'wb') as f:
        print('Updated calendar ICS file')
        f.write(cal.to_ical())


if __name__ == "__main__":
    calendar_csv2ics()
