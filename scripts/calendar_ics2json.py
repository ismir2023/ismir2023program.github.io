import json
import requests
from ics.icalendar import Calendar


def calendar_ics2json(in_ics="static/calendar/ISMIR_2022.ics", out_json="sitedata/main_calendar.json"):
    if not in_ics.startswith("http"):
        with open(in_ics, "r") as f:
            c = Calendar(f.read())
    else:
        c = Calendar(requests.get(in_ics).text)

    collector = []
    for e in c.events:
        title = e.name
        tpe = "---"

        # check for starting hashtag
        parts = title.split(" ")
        if parts[0].startswith("#"):
            tpe = parts[0][1:]
            title = " ".join(parts[1:])

        json_event = {
            "title": title,
            "start": e.begin.for_json(),
            "end": e.end.for_json(),
            "location": e.location,
            "link": e.location,
            "category": "time",
            "calendarId": tpe,
            "scrollKey": e.description,
        }
        collector.append(json_event)

    with (open(out_json, "w")) as f:
        print('Updated calendar JSON file')
        json.dump(collector, f)
    pass


if __name__ == "__main__":
    calendar_ics2json()
