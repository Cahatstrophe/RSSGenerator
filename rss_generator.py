import neocities as neo
import datetime

def read_inputs():
    ret = {}
    for line in open("settings.txt"):
        line = line.strip()
        if len(line) > 0 and line[0] != "#":
            category = line[:line.find(":")].strip()
            value = line[line.find(":") + 1:].strip()

            ret[category] = value

    return ret

def top_RSS_feed(file):
    feed = open(file, "w")

    feed.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    feed.write("<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">\n")
    feed.write("<channel>\n")

    feed.close()

def customize_RSS_feed(file, title, link, desc, name):
    feed = open(file, "a")

    feed.write("\t<title>" + title + "</title>\n")
    feed.write("\t<link>" + link + "</link>\n")
    feed.write("\t<description>" + desc + "</description>\n")
    feed.write("\t<atom:link href=\"" + link + "/" + name + "\" rel=\"self\" type=\"application/rss+xml\"/>")

    feed.close()

def bottom_RSS_feed(file):
    feed = open(file, "a")

    feed.write("</channel>\n")
    feed.write("</rss>\n")

    feed.close()

def add_to_RSS_feed(file, title, link, date, desc):

    feed = open(file, "a")

    feed.write("\t<item>\n")

    feed.write("\t\t<title>" + title + "</title>\n")
    feed.write("\t\t<link>" + link + "</link>\n")
    feed.write("\t\t<guid>" + link + "</guid>\n")

    date = date.strip().split("-")

    year = date[0]
    month = date[1]
    day = date[2]

    date = datetime.date(day=int(day), month=int(month), year=int(year))
    week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    date_str = week_days[date.weekday()] + ", "

    if date.day < 10:
        date_str += "0"
    date_str += str(date.day)
    date_str += " " + months[date.month - 1] + " " + str(date.year) + " "
    date_str += "01:01:00 EDT"

    feed.write("\t\t<pubDate>" + date_str + "</pubDate>\n")
    feed.write("\t\t<description>" + desc + "</description>\n")

    feed.write("\t</item>\n")

    feed.close()

def main():
    inputs = read_inputs()
    top_RSS_feed(inputs["file_name"])
    customize_RSS_feed(inputs["file_name"], inputs["title"], inputs["link"], inputs["desc"], inputs["file_name"])

    post = {}

    for line in open("posts.txt"):
        line = line.strip()
        if line == "!post":
            if post != {}:
                add_to_RSS_feed(inputs["file_name"], post["title"], post["link"], post["date"], post["desc"])

            post = {}

        elif len(line) > 0 and line[0] != "#":
            category = line[:line.find(":")].strip()
            data = line[line.find(":") + 1:].strip()

            post[category] = data

    if post != {}:
        add_to_RSS_feed(inputs["file_name"], post["title"], post["link"], post["date"], post["desc"])

    bottom_RSS_feed(inputs["file_name"])

    truth = ["T", "t", "True", "true", "yes", "do", "please"]
    if inputs["should_post"] in truth:
        nc = neo.NeoCities(api_key=inputs["key"])
        nc.upload((inputs["file_name"], inputs["file_name"]))

main()
