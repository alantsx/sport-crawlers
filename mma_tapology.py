from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

WEIGHT_MAP = {
    'BantamW': 'Bantamweight',
    'FeatherW': 'Featherweight',
    'FlyW': 'Flyweight',
    'HeavyW': 'Heavyweight',
    'Light HW': 'Light Heavyweight',
    'LightW': 'Lightweight',
    'MiddleW': 'Middleweight',
    'StrawW': 'Strawweight',
    'WelterW': 'Welterweight'
}

fighters = []

def getFightersTapology(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

    headers = { 'User-Agent' : user_agent }
    req = Request(url, None, headers)

    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    fight_card = soup.find('ul', {'class': 'fightCard'})

    for li in fight_card.find_all('li'):
        fightCardDiv = li.find('div', {'class': 'fightCardBout'})
        fightersImagesDiv = fightCardDiv.find_all('div', {'class': 'fightCardFighterImage'})

        fighters.append(buildFighter(fightCardDiv, fightersImagesDiv, 0))
        fighters.append(buildFighter(fightCardDiv, fightersImagesDiv, 1))
    
    return fighters

def buildFighter(fightCard, fightersImages, fighterPosition):
    fightCardPosition = 'left';

    if fighterPosition == 1:
        fightCardPosition = 'right'

    fighterDiv = fightCard.find('div', {'class': 'fightCardFighterBout ' + fightCardPosition})
    fighterName = fighterDiv.find('a').text.strip()
    fighterExternalId = fighterName.replace(' ', '_').lower().replace(".", "")

    try:
        fighterImage = fightersImages[fighterPosition].find('img', {'alt': fighterName})['src']
    except:
        fighterImage = ''

    fighterWeightDiv = fighterDiv.find('div', {'class': 'fightCardFighterRank'})
    try:
        fighterWeightUnformatted = fighterWeightDiv.find('a').text.strip()
    except:
        fighterWeightUnformatted = ''
    fighterWeightFormatted = ''
    for key in WEIGHT_MAP:
        if key in fighterWeightUnformatted:
            fighterWeightFormatted = WEIGHT_MAP[key]
            break

    fighter = {
        'externalId': fighterExternalId,
        'countryCode': 'DUMMY VALUE',
        'name': fighterName,
        'nationality': 'DUMMY VALUE',
        'sport': 'mma',
        'teams': ['ufc'],
        'tournaments': ['ufc'],
        'type': fighterWeightFormatted,
        'image': fighterImage,
        'originalUfcImage': fighterImage
    }

    return fighter
