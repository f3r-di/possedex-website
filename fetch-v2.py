import requests
import csv
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    import re
    value = unicode(value.decode("utf-8"))
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return str(value)

# @TODO: use original decodex to consolidate datas
# decodex = requests.get('http://www.lemonde.fr/webservice/decodex/updates');
response = requests.get('https://docs.google.com/spreadsheets/export?id=1po3WjKX15T766GYOYV8fHtve4RdlyLF6XEXBlUICib0&exportFormat=csv&gid=0')
response.encoding = 'UTF-8'

assert response.status_code == 200, 'failed to download csv file'

text_file = open('tmp.csv', 'w')
text_file.write(response.content)
text_file.close()

database = {'sites': {}, 'urls': {}}

id = 0

col_nom           = 0
col_desc          = 1
col_possedex      = 2

col_updated       = 3

col_proprietaire1 = 4
col_fortune1      = 5
col_marque1       = 6
col_influence1    = 7

col_proprietaire2 = 8
col_fortune2      = 9
col_marque2       =10
col_influence2    =11

col_proprietaire3 =12
col_fortune3      =13
col_marque3       =14
col_influence3    =15

col_subventions  = 16
col_pub          = 17
col_sources      = 18

col_urls         = 19 # colonne de la 1ere url




with open('tmp.csv', 'rb') as csvfile:
    url_count = 0;
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) < 4:
            continue

        id = id + 1

        if id == 1:
            continue

        entry = []
        classement_possedex = 'zzz'

        try:

            if row[col_possedex] == 'inconnu':
                classement_possedex = ''
                print bcolors.OKBLUE+"[  inconnu   ] "+bcolors.ENDC+" "+row[col_nom]
            elif row[col_possedex] == 'capital':
                classement_possedex = 'capital'
                print bcolors.OKGREEN+"[  capital  ] "+bcolors.ENDC+" "+row[col_nom]
            elif row[col_possedex] == 'etat':
                classement_possedex = 'etat'
                print bcolors.OKBLUE +"[    etat   ] "+bcolors.ENDC+" "+row[col_nom]
            elif row[col_possedex] == 'independant':
                classement_possedex = 'independant'
                print bcolors.OKGREEN+"[   indep   ] "+bcolors.ENDC+" "+row[col_nom]
                # TODO: ajouter reseaux sociaux ?
            else:
                print bcolors.FAIL+"[classement possedex manquant] "+bcolors.ENDC+" "+row[col_nom]+" (on met 0)"
                continue
        except:
            pass

        #try:
        #    note_decodex = int(row[col_decodex])
        #except:
        #    #print "               "+bcolors.WARNING+" [note decodex manquante] "+bcolors.ENDC+" "+row[col_nom]+" (on met 0)"
        #    note_decodex = 0
        #    pass
        #entry.append(note_decodex)                   #   - note originale decodex

        entry.append(row[col_nom])                    # 0  - Nom
        entry.append(row[col_desc])                   # 1  - Description
        entry.append(slugify(row[col_nom]))           # 2  - Nom normalise
        entry.append(classement_possedex)             # 3  - Notre note
        entry.append(row[col_updated])                # 4  - updated

        entry.append(row[col_pub])                    # 5  - Pub ?
        entry.append(row[col_subventions])            # 6  - subventions

        entry.append(row[col_sources])                # 7 - Sources

        entry.append(row[col_proprietaire1])          # 8
        entry.append(row[col_fortune1])               # 9
        entry.append(row[col_marque1])                # 10
        entry.append(row[col_influence1])             # 11

        entry.append(row[col_proprietaire2])          # 12
        entry.append(row[col_fortune2])               # 13
        entry.append(row[col_marque2])                # 14
        entry.append(row[col_influence2])             # 15

        entry.append(row[col_proprietaire3])          # 17
        entry.append(row[col_fortune3])               # 18
        entry.append(row[col_marque3])                # 19
        entry.append(row[col_influence3])             # 20


        database['sites'][id] = entry

        for i in range(col_urls, len(row)-1):
            url_count = url_count+1;
            url = row[i]
            url = url.rstrip('/')
            url = url.rstrip('\n')
            url = url.rstrip(' ')

            if url:
                database['urls'][url] = id

print bcolors.OKGREEN+"Nombre d'url trouvees : "+bcolors.ENDC+" ", url_count
with open('database.json', 'wb') as outfile:
    json.dump(database, outfile, indent=4)

