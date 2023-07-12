# sport-crawlers

These crawlers were built in Python. The goal is to retrieve information about UFC fighters and Formula 1 Drivers.

## UFC Crawler
You just need to pass the tapology link for the event. For example, passing [this Tapology Event link](https://www.tapology.com/fightcenter/events/100718-one-fight-night-12-kai-vs-le-2) to the function will make it retrieve all fighters information for that event.

It will get some informations, such:
- name
- weight category
- image URL

## F1 Crawler

F1 Crawler doesn't need to pass anything. It will automatically access official Formula 1 website and retrieve each driver info.

- name
- nationality
- country code
- image URL

## BeautifulSoup

Used to scrap information on the web pages used

## Request and urlopen

Used to make the requests for the URL set on the crawler
