#!/bin/python3
#Utilities for downloading and parsing Final Fantasy 14 Loadstone content
#Copyright Arthur Moore 2016 BSD 3 clause license
#Updated and revised by Akurosia Kamo in 2018

import requests
from bs4 import BeautifulSoup
import re

#Get a page from the Loadstone
# returns a BeautifulSoup object
def get_loadstone_page(url,session_id):
    #Time format used for cookies
    #import time
    #time.strftime('%a, %d-%b-%Y %H:%M:%S %Z')
    #ldst_is_support_browser=1, ldst_touchstone=1,  ldst_bypass_browser=1", expires=session_expiration
    cookies = dict(ldst_sess=session_id,domain='finalfantasyxiv.com', path='/')
    raw_page = requests.get(url, cookies=cookies)

    if(raw_page.status_code != 200):
        raise Exception("Unable to download web page!")

    return BeautifulSoup(raw_page.text,'html.parser')

# Return charachter id derived from "My charachter" button on lodestone
def get_character_id(session_id):
    char_id = []
    url = 'http://de.finalfantasyxiv.com/lodestone/'
    soup_page = get_loadstone_page(url,session_id)
    my_char_button = soup_page.find("ul", attrs={"class": 'my-menu__colmun'})
    my_char_link = my_char_button.find_all("a")[1].get('href')
    char_id.append(my_char_link.split("/")[3].encode("utf-8"))
    return char_id

# Return fc id derived from the character page, default tab
def get_fc_id(char_id, session_id):
    fc_id = []
    url = 'http://de.finalfantasyxiv.com/lodestone/character/'+ str(char_id) + '/'
    soup_page = get_loadstone_page(url,session_id)
    fc_button = soup_page.find("div", attrs={"class": 'character__freecompany__name'})
    fc_link = fc_button.find("a").get('href')
    fc_id.append(fc_link.split("/")[3].encode("utf-8"))
    return fc_id

# Return retainer ids from character page, retainer tab
def get_retainer_ids(char_id, session_id):
    url = 'http://de.finalfantasyxiv.com/lodestone/character/'+ str(char_id) + '/retainer/'
    soup_page = get_loadstone_page(url,session_id)
    retainer_button = soup_page.find("ul", attrs={"class": 'parts__switch js__toggle_item'})
    retainer_links = retainer_button.find_all("a")
    links = []
    for link in retainer_links:
        links.append(link.get('href').split("/")[5].encode("utf-8"))
    return links

# Get all items in the Free company chest (does not get number of crystals yet)
def get_fc_items(fc_id,session_id):
    url = 'http://de.finalfantasyxiv.com/lodestone/freecompany/'+str(fc_id)+'/chest/'
    soup_page = get_loadstone_page(url,session_id)
    #Get all items
    raw_items=soup_page.find_all("li", attrs={"class": "item-list__list"})
    #Parse the items
    items=[]
    items.append(get_fc_gil(soup_page))
    items += get_crystal(soup_page, 'Company Chest')
    for item in raw_items:
        tmp = {}
        tmp['name']         = item.find("h2", attrs={"class": 'db-tooltip__item__name'}).text.strip().encode("utf-8")
        tmp['quantity']     = int(item['data-stack'])
        tmp['quality']     = "<img src=\"https://img.finalfantasyxiv.com/lds/h/6/200lOroFUbfFkC1Z8JgMxbgGT4.png\" alt=\"HQ\" width=\"16\" height=\"16\"/>" if item.find("h2").find("img") != None else ""
        tmp['image']        = "<img src=\""+item.find("img")['src'].encode("utf-8")+"\" width=\"40\" height=\"40\"/>"
        tmp['location']     = 'Company Chest'
        tmp['sub_location'] = item.find_parent('ul')['id']
        items.append(tmp)
    return items

#get Gil from FC chest (may produce an issue when user cannot see fc chest)
def get_fc_gil(soup_page):
    tmp = {}
    tmp['name']         = "Gil"
    tmp['quantity']     = soup_page.find("div", attrs={"class": 'freecompany__chest__header--gil'}).p.text.strip().encode("utf-8")
    tmp['quality']      = ""
    tmp['image']        = "<img src=\"https://img.finalfantasyxiv.com/lds/h/c/uMCAYmu8y-YJlt4chlkwATrxFo.png\" width=\"40\" height=\"40\"/>"
    tmp['location']     = 'Company Chest'
    tmp['sub_location'] = "Money"
    return tmp

#Get all items in a retainers inventory (does not get number of crystals)
def get_retainer_items(char_id,retainer_id,session_id):
    url = 'http://de.finalfantasyxiv.com/lodestone/character/'+str(char_id)+'/retainer/'+retainer_id+'/baggage/'
    soup_page = get_loadstone_page(url,session_id)
    #Get retainers name
    retainer_name = soup_page.find("h3", attrs={"class": 'retainer__data--name'}).text.strip().encode("utf-8")
    #Get all items
    raw_items=soup_page.find_all("li", attrs={"class": "item-list__list sys_item_row"})
    #Parse the items
    items=[]
    items.append(get_retainer_gil(soup_page, retainer_name))
    items += get_crystal(soup_page, 'Retainer:  ' + retainer_name)
    for item in raw_items:
        tmp = {}
        tmp['name']         = item.find("h2", attrs={"class": 'db-tooltip__item__name'}).text.strip().encode("utf-8")
        tmp['quantity']     = int(item['data-stack'])
        tmp['quality']     = "<img src=\"https://img.finalfantasyxiv.com/lds/h/6/200lOroFUbfFkC1Z8JgMxbgGT4.png\" alt=\"HQ\" width=\"16\" height=\"16\"/>" if item.find("h2").find("img") != None else ""
        tmp['image']        = "<img src=\""+item.find("img")['src'].encode("utf-8")+"\" width=\"40\" height=\"40\"/>"
        tmp['location']     = 'Retainer:  ' + retainer_name
        tmp['sub_location'] = 'Inventory'
        items.append(tmp)
    return items

# Get gil from Retainer
def get_retainer_gil(soup_page, retainer_name):
    tmp = {}
    tmp['name']         = "Gil"
    tmp['quantity']     = soup_page.find("div", attrs={"class": 'heading__toggle'}).p.text.strip().encode("utf-8")
    tmp['quality']      = ""
    tmp['image']        = "<img src=\"https://img.finalfantasyxiv.com/lds/h/c/uMCAYmu8y-YJlt4chlkwATrxFo.png\" width=\"40\" height=\"40\"/>"
    tmp['location']     = 'Retainer:  ' + str(retainer_name)
    tmp['sub_location'] = "Money"
    return tmp

# Get all retainer crystals
def get_crystal(soup_page, location):
    table = soup_page.find("div", attrs={"class": 'table__crystal'})
    crystal_types = table.find("thead").find_all("span")
    crystal_body = table.find("tbody")
    crsytal_lines = crystal_body.find_all("tr")
    items = []
    for crsytal_line in crsytal_lines:
        element = crsytal_line.find("span")['data-tooltip']
        for i in range(3):
            type = crystal_types[i]['data-tooltip']
            name = (element + " " + type).strip().encode("utf-8")
            qty = crsytal_line.find_all("a")[i].text.encode("utf-8")
            image = name.lower().replace(" ", "")
            items.append(create_cristal_item(name,qty,image,location))
    return items

# Gather crystal information and create a "crystal" item
def create_cristal_item(name, quantity, image, location):
    tmp = {}
    tmp['name']         = name
    tmp['quantity']     = quantity
    tmp['quality']      = ""
    tmp['image']        = "<div class=\"crystals " + image + "\"></div>"
    tmp['location']     = location
    tmp['sub_location'] = 'Crystal Inventory'
    return tmp

# Get all items a retainer is selling (does not get number of crystals)
def get_retainer_selling(char_id,retainer_id,session_id):
    url = 'http://de.finalfantasyxiv.com/lodestone/character/'+str(char_id)+'/retainer/'+retainer_id
    soup_page = get_loadstone_page(url,session_id)
    #Get retainers name
    retainer_name = soup_page.find("h3", attrs={"class": 'retainer__data--name'}).text.strip().encode("utf-8")
    #Get all items
    sale_inventory=soup_page.find("div", attrs={"class": 'retainer__content sys_retainer-content'})
    #If no items, just return an empty set
    if not sale_inventory:
        return []
    raw_items=sale_inventory.find_all("li", attrs={"class": 'item-list__list'})
    #Parse the items
    items=[]
    for item in raw_items:
        tmp = {}
        tmp['name']         = item.find("h2", attrs={"class": 'db-tooltip__item__name'}).text.strip().encode("utf-8")
        tmp['quantity']     = int(item.find_all("div", attrs={"class": 'item-list__item item-list__cell--sm'})[1].text.strip())
        tmp['image']        = "<img src=\""+item.find("img")['src'].encode("utf-8")+"\" width=\"40\" height=\"40\"/>"
        tmp['location']     = 'Retainer:  ' + retainer_name
        tmp['sub_location'] = 'Selling'
        tmp['quality']      = "<img src=\"https://img.finalfantasyxiv.com/lds/h/6/200lOroFUbfFkC1Z8JgMxbgGT4.png\" alt=\"HQ\" width=\"16\" height=\"16\"/>" if item.find("h2").find("img") != None else ""
        items.append(tmp)
    return items

# Use this to convert the provided items into something useful
def list_items_table(items):
    item_row_format='<tr><td><span>{name} {quality}</span></td><td><span>{quantity}</span></td><td>{image}</td><td><span>{location}</span></td><td><span>{sub_location}</span><td><input id=\"checkbox\" type=\"checkbox\" name=\"lock\" value=\"\"/></td></td></tr>'
    item_buffer = '<table id="table"><tr><th>Item Name</th><th>Quantity</th><th>Image</th><th>Location</th><th>Sub-Location</th><th>Lock</th></tr>'
    checkf = '{quantity}'
    for i in items:
        check = str(checkf.format(**i))
        if (int(check.replace(".",""))>0):
            item_buffer += item_row_format.format(**i)
    item_buffer += '</table>'
    return item_buffer

# Converts the item table to full html content page
def items2html(table):
    yourdomain = "https://example.com"
    meta = "<meta charset=\"utf-8\"/>"
    css = "<link href=\""+yourdomain+"/ffxiv/itemgenerator/itemgenerator.css\" rel=\"stylesheet\" type=\"text/css\"/>"
    js = "<script type=\"text/javascript\" src=\""+yourdomain+"/resources/js/jquery-3.3.1.min.js\"></script>"
    js += "<script type=\"text/javascript\" src=\""+yourdomain+"/ffxiv/itemgenerator/itemgenerator.js\"></script>"
    inputfield = "<div><input type=\"text\" id=\"search\" placeholder=\"Type to search\">"
    inputfield += "<input type=\"button\" id=\"searchbtn\" value=\"Search\"></div>"
    searchfield = "<div><input id=\"selectbtn\" type=\"button\" value=\"Select\"/>"
    searchfield += "<input id=\"unselectbtn\" type=\"button\" value=\"Un-Select\"/></div>"
    searchfield += "<input id=\"export2CSV\" type=\"button\" value=\"Export\" onclick=\"\"/></div>"
    head = "<head>" + meta + css + js + "</head>"
    body = "<body>" + inputfield + "<div>" + table + searchfield + "</div>" + "</body>"
    html = "<html>" + head + body + "</html>"
    return BeautifulSoup(html, "html.parser").prettify().encode("utf-8")

#Debug function to write some data to '<charid>.html'
def write_data(char_id, data):
    out_file=open(str(char_id)+'.html','w')
    out_file.write(data)
    out_file.close()