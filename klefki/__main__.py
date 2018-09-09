
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from klefki import Klefki

import utils
from myargparser import MyParser
from unicode_csv_writer import UnicodeCSVWriter
from terminaltables import SingleTable

def main():
    parser = MyParser()

    parser.add_argument("username")
    parser.add_argument("password")

    parser.add_argument("--seasons", "-ls", help=u"Récupére, et imprime la liste des saisons puis quitte", action="store_true")
    parser.add_argument("--season", "-s", type=int, help=u"Change la saison pour l'id SEASON avant l'export")
    parser.add_argument("--table", help=u"Force la sortie en tableau", action="store_true")
    parser.add_argument("--csv", help=u"Force la sortie en CSV", action="store_true")

    args = parser.parse_args()

    klef = Klefki()
    klef.login(args.username, args.password)

    if args.seasons:
        seasons = klef.get_saisons()
        data = [["","ID", "Nom", u"Début", "Fin"]]
        for season in seasons:
            data.append([
                "*" if season["current"] else " ", 
                season["id"],
                season["name"], 
                season["start"], 
                season["end"], 
                ])
            print SingleTable(data).table
        exit(0)

    if args.season > 0:
        if not klef.switch_saison(args.season):
            sys.stderr.write("Impossible de changer la saison pour l'ID %i" % args.season)
            exit(404)

    operations = klef.get_operations()

    if not args.table and (args.csv or not sys.stdout.isatty()):
        csvw = UnicodeCSVWriter(sys.stdout)
        csvw.writerows(operations)
    else:
        print SingleTable([["Date", "Nom", "Email", u"Évenement", "Statut", u"Payé"]] + operations).table

if __name__ == '__main__':
    main()
