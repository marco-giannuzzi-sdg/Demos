
from bs4 import BeautifulSoup
import requests
import time

prefix_webSite = "https://brickset.com"

for year in range(2022,2023):
    year_string = str(year)
    with open('legoDataset_'+year_string+'.csv', 'w') as file:

        url = "https://brickset.com/sets/year-"+year_string+"/page-1"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        numeroPagine_link = soup.find("li", {"class": "last"}).a['href']
        numeroPagine_index = numeroPagine_link.index('page-') + 5
        numeroPagine = int(numeroPagine_link[numeroPagine_index:])

        for pagina_i in range(1, numeroPagine + 1):
            pagina_i_string = str(pagina_i)
            print("*** parsing page #" + str(pagina_i))
            url_pagina_i = "https://brickset.com/sets/year-"+year_string+"/page-" + pagina_i_string

            response = requests.get(url_pagina_i)
            soup = BeautifulSoup(response.content, "html.parser")

            tabella = soup.find("section", {"class": "setlist"})

            for risultato in tabella.findAll("article", {"class": "set"}):
                linkImmagine = risultato.a['href']
                # print(linkImmagine)
                metaRisultato = risultato.find("div", {"class": "meta"})
                linkArticolo = prefix_webSite + metaRisultato.a['href']
                descrizioneArticolo = linkArticolo.split("/")[5]
                # print(linkArticolo)
                # print(descrizioneArticolo)
                tags = metaRisultato.find("div", {"class": "tags"})
                tags_data = tags.find_all("a")

                codiceArticolo = tags_data[0].get_text()
                theme = tags_data[1].get_text()

                subtheme = "ND"
                # print(tags_data[2]['class'])
                if tags_data[2]['class'] == ['subtheme']:
                    subtheme = tags_data[2].get_text()

                row = [year_string,pagina_i_string, linkImmagine, linkArticolo, codiceArticolo, descrizioneArticolo, theme,
                       subtheme]
                file.writelines('\t'.join(row) + "\n")
                print(row)

                time.sleep(0.3)

    file.close()
