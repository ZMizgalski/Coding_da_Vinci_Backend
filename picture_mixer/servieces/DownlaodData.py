import requests
from bs4 import BeautifulSoup
import json

# imagesGalleryList = []
ObjectsList = []
finalObjects = []

language = 'en'

cookies = {'__Host-lang': language}
paramData = '?navlang=' + language + '&navlang=' + language + '&navlang=' + language
session = requests.Session()
response = session.get('https://sachsen.museum-digital.de/series/309')
soup = BeautifulSoup(response.content, "html.parser")
mydivs = soup.find_all("span", {"class": "newToolTip"})

for div in mydivs:
    strData = str(div)
    objectId = strData.split("id=")[1].split(">")[0].replace("\"", '').split("_")[1]
    objectSnippet = strData.split("<p>")[1].replace('</p></span>', '')
    objectName = strData.split("data-title=")[1].split("\"")[1]
    objectHref = "/object/" + objectId
    object = {'id': objectId, 'name': objectName, 'next_link': objectHref, 'data': objectSnippet}
    ObjectsList.append(object)

for obj_tmp in ObjectsList:
    response2 = session.get('https://sachsen.museum-digital.de/object/' + obj_tmp['id'] + "?" + paramData,
                            cookies=cookies)
    soup2 = BeautifulSoup(response2.content, "html.parser")
    header = soup2.find('header', {'id': 'pageTitle'})
    mainTitle = str(header.find("h2")).replace('<h2>', '').replace('</h2>', '')
    top_images = soup2.find('div', {'class': 'objektimage_overview'})

    # try:
    #     imgs = top_images.find_all('img')
    #     for img in imgs:
    #         src = str(img).split("src=")[1].split("\"")[1]
    #         link = src.split("/")[6]
    #         small = src.replace(link, '') + "100h_" + link.split("_")[1]
    #         medium = src.replace(link, '') + "200w_" + link.split("_")[1]
    #         large = src.replace(link, '') + "500w_" + link.split("_")[1]
    #         sizes = {'small': small, 'medium': medium, 'large': large}
    #         alt = str(img).split("alt=")[1].split("height=")[0].replace('\'', "").replace("\n", ' ').replace('/',
    #                                                                                                          ' ').replace(
    #             '\"', '').split("src=")[0]
    #         dataImg = {'src': sizes, 'alt': alt}
    #         imagesGalleryList.append(dataImg)
    # except AttributeError:
    #     imagesGalleryList = []

    section1 = soup2.find('section', {'id': 'objectInfo'})

    mainImage = str(soup2.find('meta', {'property': 'image'})).split('content=')[1].split("\"")[1]

    smallImageList = str(soup2.find('meta', {'property': 'image'})).split('content=')[1].split("\"")[1].split("/")
    link = mainImage.replace(smallImageList[7], '')
    image = "200w_" + smallImageList[7]
    smallImage = link + image

    objectTitle = str(soup2.find('h3', {'id': 'objectInfoTitle'})).split('>')[1].split('<')[0]

    exp_strings = ['span', '=', '/p', '/a']
    desc = ''
    temp_desc = []
    for data in str(soup2.find('p', {'property': "description"})).split('property="description">')[1].split('>'):
        for item in data.split("<"):
            res = [ele for ele in exp_strings if (ele in item)]
            if not res:
                temp_desc.append(item)
    final_desc = desc.join(temp_desc)
    section2 = soup2.find('section', {'id': 'objectFurtherInfo'})

    mainTechnique_title = str(section2.find('div', {'id': 'object_material_technique'}).find('h3')).replace('<h3>',
                                                                                                            '').replace(
        '</h3>', '')
    mainTechnique_content = str(section2.find('div', {'id': 'object_material_technique'}).find('p')).replace('<p>',
                                                                                                             '').replace(
        '</p>', '')

    try:
        measurements_title = str(section2.find('div', {'id': 'object_measurements'}).find('h3')).replace('<h3>',
                                                                                                         '').replace(
            '</h3>', '')
    except AttributeError:
        measurements_title = 'Not Defined'
    try:
        measurements_content = str(section2.find('div', {'id': 'object_measurements'}).find('p')).replace('<p>',
                                                                                                          '').replace(
            '</p>', '')
    except AttributeError:
        measurements_content = 'Not Defined'

    section3 = soup2.find('section', {'id': 'objNoda'})
    objEvent = section3.find_all('div', {'class': 'objevent'})

    events = []
    for obj in objEvent:
        title = str(obj.find('h5')).replace('<h5>', '').replace('</h5>', '')
        tables = obj.find_all('table')
        for table in tables:
            ths_count = 0
            tds_count = 0
            ths_tmp = []
            tds_tmp = []
            table_tr = table.find_all('tr')
            for tr in table_tr:
                table_ths = table.find_all('th')
                table_tds = table.find_all('td')
                for th in table_ths:
                    if ths_count < len(table_ths):
                        ths_tmp.append(str(th).replace("<th>", '').replace('</th>', '').replace('\n', ''))
                        ths_count += 1
                for td in table_tds:
                    if tds_count < len(table_tds):
                        tds_tmp.append(str(td.find('a')).split('>')[1].split('<')[0].replace('\n', ''))
                        tds_count += 1
            for index in enumerate(ths_tmp):
                data = {'title': title, 'header': ths_tmp[index[0]], 'data': tds_tmp[index[0]]}
                events.append(data)

    section4 = soup2.find('div', {'id': 'object_series'})
    mainFooterTitle = str(section4.find('h3')).replace('<h3>', '').replace("</h3>", '')
    mainFooterContent = str(section4.find('a')).split('>')[1].split('<')[0]

    # objectData = {
    #     'mainTitle': mainTitle,
    #     'imagesGalleryList': imagesGalleryList,
    #     'mainImage': mainImage,
    #     'objectTitle': objectTitle,
    #     'description': final_desc,
    #     'mainTechnique_title': mainTechnique_title,
    #     'mainTechnique_content': mainTechnique_content,
    #     'measurements_title': measurements_title,
    #     'measurements_content': measurements_content,
    #     'events': events
    # }
    objectData = {
        'mainTitle': mainTitle,
        'smallImage': smallImage,
        'mainImage': mainImage,
        'objectTitle': objectTitle,
        'description': final_desc,
        'mainTechnique_title': mainTechnique_title,
        'mainTechnique_content': mainTechnique_content,
        'measurements_title': measurements_title,
        'measurements_content': measurements_content,
        'events': events
    }


    finalObjects.append(objectData)

with open('data.json', 'w') as f:
    json.dump(finalObjects, f)
# print(finalObjects)
