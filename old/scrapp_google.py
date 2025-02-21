from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import locale
from fake_useragent import UserAgent
import platform
import random
import time



def get_current_os():
    if(platform.system()=="Darwin"):
        return "macos"
    return platform.system().lower()

# headers pour montrer que c'est un navigateur valide
def get_random_headers():
    ua = UserAgent(browsers=['chrome'], os=get_current_os())
    return ua.random
    
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    #     'Referer': 'https://www.google.com/',
    #     'Accept-Language': "",
    #     'Accept-Encoding': "",
    #     'Connection': ""
    # }

def requests_delay():
    sleep_time = random.uniform(1, 10)
    time.sleep(sleep_time)


def analyse_site(url):

    # Configuration de Selenium 
    options = webdriver.ChromeOptions()

    #ajout des headers
    headers = get_random_headers()
    options.add_argument(f'user-agent={headers}')

    # Initialiser le navigateur Chrome avec les options configurées
    driver = webdriver.Chrome(options=options)

    driver.get(url=url)

    # ajout d'un sleep avant de parser le html
    requests_delay()


    # Récupérer le contenu généré par JavaScript
    html_content = driver.page_source

    print(html_content)

    # Fermer le navigateur
    driver.quit()


    # Utiliser BeautifulSoup pour parser le code HTML
    soup = BeautifulSoup(html_content, 'html.parser')



    requests_delay()
    results = soup.find_all("div", class_="Nv2PK THOPZb CpccDe")
    scrapped_items = []
    for result in results:
        header = result.find("div", class_="qBF1Pd fontHeadlineSmall").text.strip()
        etoiles = result.find("span", class_="MW4etd").text.strip()
        nb_avis = result.find("span", class_="UY7F9").text.strip()
        location = result.select("div.W4Efsd > span:nth-child(2) > span:nth-child(2)")
        print([x for x in location])
        data = {
            "header":header,
            "etoiles":etoiles,
            "nb_avis":nb_avis,
            "location":location
        }
        scrapped_items.append(data)

    print(scrapped_items)
    # adresse = p_adresse.find("a").text.strip()

    # h1_title = soup.find("h1", class_="text-headline-1-expanded u-break-word")
    # title = h1_title.text.strip()

    # prix_str = soup.find("p", class_="text-headline-2").text.strip().split("€")[0]
    # locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    # prix = locale.atoi(prix_str)

    # info_list = []

    # elements = soup.find_all("div", id="ad_param_truncate_text")

    # for elt in elements :
    #    p_elt = elt.find("p").text.strip()
    #    info_list.append(p_elt)

    # type_habitat = info_list[0]

    # surface_habitable = int(info_list[1].split('m²')[0])

    # print(info_list)

    # if type_habitat == 'Appartement':
    #     pieces = int(info_list[2]) 
    # else:
    #     if type_habitat == 'Maison':
    #         pieces = int(info_list[3]) 
    #     else:
    #         pieces = None
    

    # div_energy = soup.find_all("div", class_="drop-shadow")

    # if(len(div_energy) > 1):
    #     dpe = div_energy[0].text.strip()
    #     ges = div_energy[1].text.strip()
    # else:
    #     dpe = None
    #     ges = None

    # p_description = soup.find("p", class_="whitespace-pre-line text-body-1 [overflow-wrap:anywhere] line-clamp-6").text.strip().replace("\n", " ")

    # #requests_delay()

    # # Construire la réponse JSON
    # response = {
    #     'adresse':adresse,
    #     'url_img': url_img,
    #     'title': title,
    #     'prix':prix,
    #     'type_habitat':type_habitat,
    #     'surface_habitable':surface_habitable,
    #     'nbr_pieces':pieces,
    #     "ges": ges,
    #     "dpe": dpe,
    #     'description': p_description
        
    # }

    # with open('data.json', 'w') as outfile:
    #     json.dump(response, outfile)
    # return response

info = analyse_site("https://www.google.com/maps/search/restaurants/")