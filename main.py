# pylint: disable=global-statement,redefined-outer-name
import argparse
import csv
import glob
import json
import os

import yaml
from flask import Flask, jsonify, redirect, render_template, send_from_directory, send_file, url_for
from flask_frozen import Freezer
from flaskext.markdown import Markdown
# from flaskext.cache import Cache
import pytz
from pytz import timezone
import tzlocal
import datetime
from dateutil import tz

site_data = {}
by_uid = {}


def paper_check(row):
    return "paper" in row['type']


def jobs_check(row):
    return "jobs" in row['type']

def industry_check(row):
    return "industry" in row['type']

def music_check(row):
    return "music" in row['type']

def lbd_check(row):
    return "lbd" in row['type']

def main(site_data_path):
    global site_data, extra_files
    extra_files = ["README.md"]
    # Load all for your sitedata one time.
    for f in glob.glob(site_data_path + "/*"):
        extra_files.append(f)
        name, typ = f.split("/")[-1].split(".")
        if typ == "json":
            site_data[name] = json.load(open(f))
        elif typ in {"csv", "tsv"}:
            site_data[name] = list(csv.DictReader(open(f)))
        elif typ == "yml":
            site_data[name] = yaml.load(open(f).read(), Loader=yaml.SafeLoader)
    for typ in ["papers", "industry", "music", "lbds", "events", "jobs"]:
        by_uid[typ] = {}
        for p in site_data[typ]:
            by_uid[typ][p["uid"]] = p
    print("Data Successfully Loaded")
    by_uid["days"] = {}
    site_data["days"] = []
    for day in ['1', '2', '3', '4', '5']:
        speakers = [s for s in site_data["events"] if s["day"] == day and s["category"] == "All Meeting"]
        posters = [p for p in site_data["events"] if p["day"] == day and p["category"] == "Poster session"]
        lbd = [l for l in site_data["events"] if l["day"] == day and l["category"] == "LBD"]
        music = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Music"]
        industry = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Industry"]
        meetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Meetup"]
        vmeetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "VMeetup"]
        master = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Masterclass"]
        wimir = [w for w in site_data["events"] if w["day"] == day and w["category"] == "WiMIR Meetup"]
        special = [s for s in site_data["events"] if s["day"] == day and s["category"] == "Meetup-Special"]
        opening = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Opening"]
        business = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Awards"]
        social = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Social"]
        tutorials = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Tutorials"]

        by_uid["days"][day] = {
            "uid": day,
            "speakers": speakers,
            "all": all,
            "meetup": meetup,
            "special": special,
            "master": master,
            "wimir": wimir,
            "posters": posters,
            "lbd": lbd,
            "music": music,
            "industry": industry,
            "day": day,
            "opening": opening,
            "business": business,
            "social": social,
            "vmeetup":vmeetup,
            "tutorials":tutorials
        }
        site_data["days"].append(by_uid["days"][day])
    return extra_files


# ------------- SERVER CODE -------------------->

app = Flask(__name__)
# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.config.from_object(__name__)
freezer = Freezer(app)
markdown = Markdown(app)

# MAIN PAGES


def _data():
    data = {}
    data["config"] = site_data["config"]
    return data


@app.route("/")
def index():
    return redirect("/calendar.html")


# TOP LEVEL PAGES


@app.route("/index.html")
def home():
    return redirect("/calendar.html")


@app.route("/papers.html")
def papers():
    data = _data()
    data["papers"] = site_data["papers"]
    return render_template("papers.html", **data)


@app.route("/paper_vis.html")
def paper_vis():
    data = _data()
    return render_template("papers_vis.html", **data)


@app.route("/calendar.html")
def schedule():
    data = _data()
    data["days"] = []
    # data = _data()
    for day in ['1', '2', '3', '4', '5']:
        speakers = [s for s in site_data["events"] if s["day"] == day and s["category"] == "All Meeting"]
        posters = [p for p in site_data["events"] if p["day"] == day and p["category"] == "Poster session"]
        lbd = [l for l in site_data["events"] if l["day"] == day and l["category"] == "LBD"]
        music = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Music"]
        industry = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Industry"]
        meetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Meetup"]
        vmeetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "VMeetup"]
        master = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Masterclass"]
        wimir = [w for w in site_data["events"] if w["day"] == day and w["category"] == "WiMIR Meetup"]
        special = [s for s in site_data["events"] if s["day"] == day and s["category"] == "Meetup-Special"]
        opening = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Opening"]
        business = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Awards"]
        social = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Social"]
        tutorials = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Tutorials"]

        out = {
            "speakers": speakers,
            "all": all,
            "meetup": meetup,
            "special": special,
            "master": master,
            "wimir": wimir,
            "posters": posters,
            "lbd": lbd,
            "music": music,
            "industry": industry,
            "day": day,
            "opening": opening,
            "business": business,
            "social": social,
            "vmeetup": vmeetup,
            "tutorials": tutorials

        }
        data["days"].append(out)
    return render_template("schedule.html", **data)


@app.route("/tutorials.html")
def tutorials():
    data = _data()
    data["tutorials"] = [t for t in site_data["events"] if t['category'] == "Tutorials"]
    return render_template("tutorials.html", **data)

@app.route("/music.html")
def musics():
    data = _data()
    data["music"] = site_data["music"]
    return render_template("music.html", **data)

@app.route("/jobs.html")
def job_board():
    data = _data()
    data["jobs"] = site_data["jobs"]
    return render_template("jobs.html", **data)

@app.route("/industry.html")
def industries():
    data = _data()
    data["industry"] = site_data["industry"]
    return render_template("industry.html", **data)

@app.route("/lbds.html")
def lbds():
    data = _data()
    data["lbds"] = site_data["lbds"]
    return render_template("lbds.html", **data)

@app.route("/lbds_vis.html")
def lbds_vis():
    data = _data()
    return render_template("lbds_vis.html", **data)

@app.route("/special_meetings.html")
def topics():
    data = _data()
    return render_template("special_meetings.html", **data)

# DOWNLOAD CALENDAR

@app.route("/getCalendar")
def get_calendar():
    filepath = 'static/calendar/'
    filename = 'ISMIR_2022.ics'
    return send_file(os.path.join(filepath, filename), as_attachment=True)

def extract_list_field(v, key):
    value = v.get(key, "")
    if isinstance(value, list):
        return value
    else:
        return value.split(";")


def format_paper(v):
    list_keys = ["authors", "primary_subject", "secondary_subject", "session", "authors_and_affil"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)

    return {
        "id": v["uid"],
        "session": v["session"],
        "position": "{:02d}".format(int(v["position"])+1),
        "forum": v["uid"],
        "pic_id": v['thumbnail'],
        "content": {
            "title": v["title"],
            "paper_presentation": v["paper_presentation"],
            "long_presentation": v["long_presentation"],
            "authors": list_fields["authors"],
            "authors_and_affil": list_fields["authors_and_affil"],
            "keywords": list(set(list_fields["primary_subject"] + list_fields["secondary_subject"])),
            "abstract": v["abstract"] +'<br><br> <b><p align="center">[Direct link to video]({})</b>'.format(v["video"]),
            "TLDR": v["abstract"],
            "poster_pdf": v.get("poster_pdf", ""),
            "session": list_fields["session"],
            "pdf_path": v.get("pdf_path", ""),
            "video": v["video"].replace('/open?id=', '/uc?export=preview&id='),
            "channel_url": v["channel_url"],
            "slack_channel": v["slack_channel"],
            "day": v["day"],
        },
        "poster_pdf": "GLTR_poster.pdf",
    }

def format_lbd(v):
    list_keys = ["authors", "session"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)
    channel_name = v.get("channel_name", "")
    channel_url = v.get("channel_url", "")
    return {
        "id": v["uid"],
        "position": v["position"],
        "forum": v["uid"],
        "content": {
            "title": v["title"],
            "authors": list_fields["authors"],
            "abstract": v["abstract"],
            "TLDR": v["abstract"],
            "session": list_fields["session"],
            "thumbnail_link": v.get("thumbnail_link", ""),
            "poster_link": v.get("poster_link", ""),
            "paper_link": v.get("paper_link", ""),
            "poster_type": v.get("poster_type", ""),
            "bilibili_id": v.get("bilibili_id", ""),
            "youtube_id": v.get("youtube_id", "").replace('/file/d/', '/uc?export=preview&id='),
            "channel_name": channel_name,
            "channel_url": channel_url,
            "day": 4,
        },
    }


def format_workshop(v):
    list_keys = ["authors"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)

    return {
        "id": v["uid"],
        "title": v["title"],
        "organizers": list_fields["authors"],
        "abstract": v["abstract"],
    }

def format_music(v):
    return {
        "id": v["uid"],
        "content": {
            "title": v["title"],
            "authors": v["authors"],
            "affiliation": v["affiliation"],
            "abstract": v["abstract"],
            "bio": v["bio"],
            "web_link": v["web_link"],
            "session": v["session"],
            "yt_id": v["yt_id"],
            "bb_id": v["bb_id"],
        }
    }


def format_jobs(v):
    return {
        "id": v["uid"],
        "content": {
            "title": v["title"],
            "jd": v["jd"],
            "channel_name": v["channel_name"],
            "channel_url": v["channel_url"],
            "company": v["company"],
            "external_web_link": v["external_web_link"]
        }
    }


def format_industry(v):
    return {
        "id": v["uid"],
        "content": {
            "title": v["title"],
            "session": v["session"],
            "channel_name": v["channel_name"],
            "channel_url": v["channel_url"],
            "company": v["company"],
        }
    }

@app.template_filter('localcheck')
def datetimelocalcheck(s):
    return tzlocal.get_localzone()

@app.template_filter('localizetime')
def localizetime(date,time,timezone):
    to_zone = tz.gettz(str(timezone))
    date = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
    ref_date_tz = pytz.timezone('Asia/Kolkata').localize(date) #[TODO] take ref time zone as input
    local_date = ref_date_tz.astimezone(to_zone)
    return local_date.strftime("%Y-%m-%d"), local_date.strftime("%H:%M")


# ITEM PAGES

@app.route("/day_<day>.html")
def day(day):
    uid = day
    v = by_uid["days"][uid]
    data = _data()
    data["day"] = v
    data["daynum"] = uid
    return render_template("day.html", **data)

@app.route("/poster_<poster>.html")
def poster(poster):
    uid = poster
    v = by_uid["papers"][uid]
    data = _data()
    data["paper"] = format_paper(v)
    return render_template("poster.html", **data)


@app.route("/speaker_<speaker>.html")
def speaker(speaker):
    uid = speaker
    v = by_uid["speakers"][uid]
    data = _data()
    data["speaker"] = v
    return render_template("speaker.html", **data)


@app.route("/workshop_<workshop>.html")
def workshop(workshop):
    uid = workshop
    v = by_uid["workshops"][uid]
    data = _data()
    data["workshop"] = format_workshop(v)
    return render_template("workshop.html", **data)

@app.route("/music_<music>.html")
def music(music):
    uid = music
    v = by_uid["music"][uid]
    data = _data()
    data["music"] = v
    return render_template("piece.html", **data)

@app.route("/jobs_<jobs>.html")
def jobs(jobs):
    uid = jobs
    v = by_uid["jobs"][uid]
    data = _data()
    data["jobs"] = v
    return render_template("jobs_template.html", **data)

@app.route("/industry_<industry>.html")
def industry(industry):
    uid = industry
    v = by_uid["industry"][uid]
    data = _data()
    data["industry"] = v
    return render_template("company.html", **data)

@app.route("/lbd_<lbd>.html")
def lbd(lbd):
    uid = lbd
    v = by_uid["lbds"][uid]
    data = _data()
    data["lbd"] = format_lbd(v)
    return render_template("lbd.html", **data)


@app.route("/chat.html")
def chat():
    data = _data()
    return render_template("chat.html", **data)


# FRONT END SERVING


@app.route("/papers.json")
def paper_json():
    json = []
    for v in site_data["papers"]:
        json.append(format_paper(v))
    return jsonify(json)

@app.route("/music.json")
def music_json():
    json = []
    for v in site_data["music"]:
        json.append(v)
    return jsonify(json)

@app.route("/jobs.json")
def jobs_json():
    json = []
    for v in site_data["jobs"]:
        json.append(v)
    return jsonify(json)

@app.route("/industry.json")
def industry_json():
    json = []
    for v in site_data["industry"]:
        json.append(v)
    return jsonify(json)

@app.route("/lbds.json")
def lbds_json():
    json = []
    for v in site_data["lbds"]:
        json.append(format_lbd(v))
    return jsonify(json)


@app.route("/static/<path:path>")
def send_static(path):
    if "wo_num" not in path:
        return send_from_directory("static", path)


@app.route("/serve_<path>.json")
def serve(path):
    return jsonify(site_data[path])


# --------------- DRIVER CODE -------------------------->
# Code to turn it all static


@freezer.register_generator
def generator():

    for paper in site_data["papers"]:
        yield "poster", {"poster": str(paper["uid"])}
    for music in site_data["music"]:
        yield "music", {"music": str(music["uid"])}
    for industry in site_data["industry"]:
        yield "industry", {"industry": str(industry["uid"])}
    for jobs in site_data["jobs"]:
        yield "jobs", {"jobs": str(jobs["uid"])}
    for lbd in site_data["lbds"]:
        yield "lbd", {"lbd": str(lbd["uid"])}
    for day in site_data["days"]:
        yield "day", {"day": str(day["uid"])}

    for key in site_data:
        if key != 'days':
            yield "serve", {"path": key}


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")

    parser.add_argument(
        "--build",
        action="store_true",
        default=False,
        help="Convert the site to static assets",
    )

    parser.add_argument(
        "-b",
        action="store_true",
        default=False,
        dest="build",
        help="Convert the site to static assets",
    )

    
    parser.add_argument(
        "--path",
        help="Pass the JSON data path and run the server",
        required=True)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    data_path = args.path

    if(data_path is None):
        raise Exception("--path for the root directory for data is missing")

    extra_files = main(data_path)
    if args.build:
        freezer.freeze()
    else:
        debug_val = False
        if os.getenv("FLASK_DEBUG") == "True":
            debug_val = True
        app.run(port=5100, debug=debug_val, extra_files=extra_files)


    
