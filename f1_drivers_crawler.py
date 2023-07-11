import datetime
import logging
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from operations.country_codes import \
    country_name_to_ISO3166_alpha3 as CountryCodeConverter
from operations.upload_images import stage_imgix_host
from operations.upload_images import upload_image_from_url as image_uploader

logger = logging.Logger(__name__)

base_url = "https://www.formula1.com"
_sport = "motor-racing"


def get_drivers_f1():
    drivers = []

    url = base_url + "/en/drivers.html"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

    headers = {'User-Agent': user_agent}
    req = Request(url, None, headers)

    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    drivers_container = soup.find("div", {"class": "container listing-items--wrapper driver during-season"})
    drivers_row = drivers_container.find("div", {"class": "row"})

    for driver_profile in drivers_row.find_all("div", class_=lambda x: x and x.startswith('col-12 col-md-6 col-lg-4')):
        a = driver_profile.find('a', {'class': 'listing-item--link'})
        name = a.get('data-tracking').split('"path": "')[1].split('",')[0]

        driver_url = a.get("href")

        nationality = get_driver_nationality(driver_url)

        team = a.find('p', {'class': 'listing-item--team'}).text.strip()

        picture = a.find('picture', {'class': 'listing-item--photo'})
        img_tag = picture.find('img', {"class": "lazy"})
        if img_tag:
            image = img_tag.get('data-src')

        driver_obj = {
            "name": name,
            "nationality": nationality,
            "team": team,
            "image": image
        }

        drivers.append(build_driver(driver_obj))

    return drivers


def get_driver_nationality(driver_url):
    url = base_url + driver_url
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

    headers = {'User-Agent': user_agent}
    req = Request(url, None, headers)

    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    tag_tr = soup.select_one('tr:has(span:-soup-contains("Country"))')
    tag_td = tag_tr.find('td')
    country = tag_td.text

    return country


def build_driver(driver_stats: dict):
    driver_id = driver_stats.get("name").lower().replace(" ", "-")
    external_id = "gs-motorsport-player-" + driver_id

    country_code = CountryCodeConverter(driver_stats.get("nationality"))

    try:
        uploadImage(driver_stats["image"], external_id)
    except Exception as e:
        logger.error("The upload image for %s failed", external_id)
        logger.error(e)

    driver = {
        'externalId': external_id,
        'countryCode': country_code,
        'name': driver_stats.get("name"),
        'nationality': driver_stats.get("nationality"),
        'sport': _sport,
        'teams': [driver_stats.get("team")],
        'lastUpdate': datetime.datetime.now(),
        'tournaments': ['f1'],
        'image': f"https://{stage_imgix_host}/{__get_player_image_path(external_id)}"
    }

    return driver


def uploadImage(player_image: str, player_id: str):
    image_uploader(
        player_image, __get_player_image_path(player_id)
    )


def __get_player_image_path(player_id: str) -> str:
    return f"players/player-mma-{player_id}.png"
