#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
from lxml import html

import utils

class Klefki:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Windows NT x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

    # Perform login
    def login(self, username, password):
        self.session.post("https://cotizasso.com/Authentication/login", {
            "email": username, 
            "password": password, 
        })

    def __get_seasons(self, page):
        return html.fromstring(self.session.get("https://cotizasso.com/season?page=%i" % page).content)

    def get_saisons(self):
        page = 1
        tree = self.__get_seasons(page);
        snumber = utils.clean_float(tree.xpath("string(//*[@id=\"content \"]/section/section/section/section/header/text())"))
        seasons = []

        while(len(seasons) < snumber):
            rows = tree.xpath("//*[@id=\"content \"]/section/section/section/section/div/table/tbody/tr")
            for row in rows:
                cells = row.xpath("td")
                if(len(cells) == 4):
                    season = {}
                    season["name"] = utils.clean_spaces(cells[0].xpath("string(a/text())"))
                    season["id"] = utils.clean_int(cells[0].xpath("string(a/@href)"))
                    season["current"] = utils.clean_spaces(cells[0].xpath("string(a/span/text())")) == "en cours"
                    season["start"] = utils.clean_date(cells[1].text)
                    season["end"] = utils.clean_date(cells[2].text)
                    seasons.append(season)
            
            page += 1
            tree = self.__get_seasons(page)
        
        return seasons

    def switch_saison(self, season_id):
        self.session.get("https://cotizasso.com/season/switch/%i" % season_id)
        try:
            current_saison = [x for x in self.get_saisons() if x["current"]][0]
        except IndexError:
            return False

        return current_saison["id"] == season_id
        
    def __get_operations(self, page):
        return html.fromstring(self.session.get("https://cotizasso.com/Operation?page=%i" % page).content)

    def get_operations(self):
        page = 1
        tree = self.__get_operations(page);
        opnumber = utils.clean_float(tree.xpath("string(//*[@id=\"content \"]/section/section/section/div[3]/div/div/section/header/text())"))
        operations = []

        while(len(operations) < opnumber):
            rows = tree.xpath("//*[@id=\"content \"]/section/section/section/div[3]/div/div/section/div/table/tbody/tr")
            for row in rows:
                cells = row.getchildren()
                if(len(cells) == 10):
                    date = utils.clean_datetime(cells[2].xpath("string(a/text())"))
                    nom = utils.clean_spaces(cells[3].xpath("string(strong/text())"))
                    mail = utils.clean_spaces(cells[3].xpath("string(a/text())"))
                    event = utils.clean_spaces(cells[5].xpath("string(a/text())"))
                    state = utils.clean_spaces(utils.get_deep_text(cells[6]))
                    payed = str(utils.clean_float(cells[7].text))
                    operations.append([date, nom, mail, event, state, payed])
            
            page += 1
            tree = self.__get_operations(page)
        
        return operations
