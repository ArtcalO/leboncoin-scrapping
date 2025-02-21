from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import locale
import random

def set_proxy(proxy_address):
  options = webdriver.ChromeOptions()
  options.add_argument('--proxy-server=%s' % proxy_address)
  driver = webdriver.Chrome(options=options)
  return driver

with open("valid_proxies.txt", "r") as f:
    proxies = f.read().split("\n")

def analyse_site(html_content):

    # Utiliser BeautifulSoup pour parser le code HTML
    soup = BeautifulSoup(html_content, 'html.parser')


    #Extraire les informations souhaitées du site
    div_img = soup.find("div", class_="shrink-0 grow-0 basis-1/2 pr-sm")
    img = div_img.find("img")
    url_img = img["src"]

    p_adresse = soup.find("p", class_="inline-flex w-full flex-wrap mb-md")
    adresse = p_adresse.find("a").text.strip()

    h1_title = soup.find("h1", class_="text-headline-1-expanded u-break-word")
    title = h1_title.text.strip()

    prix_str = soup.find("p", class_="text-headline-2").text.strip().split("€")[0]

    #avoid using set_locale
    #locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    prix = prix_str #locale.atoi(prix_str)

    info_list = []

    elements = soup.find_all("div", id="ad_param_truncate_text")

    for elt in elements : 
       p_elt = elt.find("p").text.strip()
       info_list.append(p_elt)

    type_habitat = info_list[0]

    surface_habitable = int(info_list[1].split('m²')[0])

    print(info_list)

    if type_habitat == 'Appartement':
        pieces = int(info_list[2]) 
    else:
        if type_habitat == 'Maison':
            pieces = int(info_list[3]) 
        else:
            pieces = None
    

    div_energy = soup.find_all("div", class_="drop-shadow")

    if(len(div_energy) > 1):
        dpe = div_energy[0].text.strip()
        ges = div_energy[1].text.strip()
    else:
        dpe = None
        ges = None

    p_description = soup.find("p", class_="whitespace-pre-line text-body-1 [overflow-wrap:anywhere] line-clamp-6").text.strip().replace("\n", " ")


    # Construire la réponse JSON
    response = {
        'adresse':adresse,
        'title': title,
        'prix':prix,
        'type_habitat':type_habitat,
        'surface_habitable':surface_habitable,
        'nbr_pieces':pieces,
        "ges": ges,
        "dpe": dpe,
        'description': p_description
        
    }

    return response

info = analyse_site()

print(info)
    