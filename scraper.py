import requests, sys, csv, re
from bs4 import BeautifulSoup

def create():
    print("creating new  file")
    name=input ("enter the name of file:")
    extension=input ("enter extension of file:")
    try:
        name=name+"."+extension
        file=open(name,'a')

        file.close()
    except:
            print("error occured")
            sys.exit(0)

####
## Lets get an array of cities
####
cities = []
url = 'http://www.unitestudents.com'
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
citiesmenu = soup.find('li', {'class': 'cities-menu'})
citiesmenuul = citiesmenu.find('ul', {'class':'first-lvl__list'})
cmli = citiesmenuul.find_all('li', {'class':'second-lvl'})
for city in cmli:
    cities.append(city.find('h5').contents[0])
    print(city.find('h5').contents[0])

print('Number of cities: '+str(len(cities)))
##################

file = open("dbs.csv", "w" , newline='')
writer = csv.writer(file)
attrlist = [] # Array for list of attributes associated with propertylist

# Write the column headers in csv# Write the list of attributes to csv file as a new row
header = ['City', 'Type', 'Nominated Uni', 'Name', 'Dist from city centre', 'Dist from uni', 'Beds']
writer.writerow(header)

propcount = 0 # A counter for number of properties

for city in cities:
    url = 'http://www.unitestudents.com/'+str(city.lower())
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    propertylist = soup.find('ul', class_='property-list').find_all('li', {'class': ['property-list__item', 'property-list__header']})

    # Now lets get properties per city
    for prop in propertylist:
        # Get the uni accommodation is nominated to
        if prop['class'][0] == 'property-list__header':
            nominateduni = prop.find('h3').contents[0]
        else:
            propcount += 1 # increase property counter by 1
            attrlist.append(city) # Append city name in first column

            # to check whether you can book directly, we check if the orange button
            # exists, because the orange button only exists for this

            bookroom = prop.find('div', {'class':'property-body__buttons'}).find('a', {'class':'btn--orange'})
            if bookroom:
                attrlist.append('Direct')
                attrlist.append('No Nomination')
            else:
                attrlist.append('Nominated')
                attrlist.append(nominateduni)

            # Find and append the name of property to list of attributes
            name = prop.find('h3', {'class' : 'property-header__title'}).find('a').contents[0]
            attrlist.append(name)

            # Distance from centre, distance from uni, #beds
            infobite = prop.find_all('li', class_='info-bite')
            for info in infobite:
                try:
                    infos = info.find('p', {'class' : 'info-bite__text'}).contents[0]
                    # Find bed number and split it into the integer of beds
                    if 'beds' in infos:
                        beds = infos.split()
                        attrlist.append(beds[0])
                    else:
                        attrlist.append(infos)
                except:
                    attrlist.append("Error")

            # Write the list of attributes to csv file as a new row
            writer.writerow(attrlist)

            # empty list of attributes for next property
            del attrlist [:]
file.close()
