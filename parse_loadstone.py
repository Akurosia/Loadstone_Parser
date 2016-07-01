#!/bin/python3
#Utilities for downloading and parsing Final Fantasy 14 Loadstone content
#Copyright Arthur Moore 2016 BSD 3 clause license

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

    return BeautifulSoup(raw_page.text)

#Each item has a separate detail page that must be loaded to determine if it's HQ or not
def is_item_hq(raw_item,session_id):
        tooltip_url = 'http://na.finalfantasyxiv.com/' + item.find('div', attrs={"class": 'item_txt'})['data-lazy_load_url']
        tooltip_page = get_loadstone_page(tooltip_url,session_id)
        return bool(tooltip_page.find("img", src = re.compile('http://img\.finalfantasyxiv\.com/lds/pc/global/images/common/ic/hq.png.*')))

#Debug function to write some data to 'test.html'
def write_data(data):
    out_file=open('test.html','w')
    #for i in data:
        #out_file.write(str(i))
    out_file.write(str(data))
    out_file.close()

#Debug function to write a pretty parsed version of a Loadstone page
def write_loadstone_page(url,session_id):
    soup_page = get_loadstone_page(url,session_id)
    write_data(soup_page.prettify().encode('utf8'))

#Use this to convert the provided items into something useful
def list_items_table(items):
    item_row_format='<tr><td><img src="{image}"></img></td><td>{name}</td><td>{quantity}</td><td>{location}</td><td>{sub_location}</td></tr>\n'
    item_buffer = '<table>\n'
    for i in items:
        item_buffer += item_row_format.format(**i)
    item_buffer += '</table>\n'
    return item_buffer


#Get all items in the Free company chest (does not get number of crystals or gil)
#Does not handle HQ Items yet
def get_fc_items(fc_id,session_id):
    url = 'http://na.finalfantasyxiv.com/lodestone/freecompany/'+str(fc_id)+'/chest/'
    soup_page = get_loadstone_page(url,session_id)
    #Get all items
    raw_items=soup_page.find_all("tr", attrs={"data-default_sort": True})
    #Parse the items
    items=[]
    for item in raw_items:
        tmp = {}
        tmp['name']         = item.find("h2", attrs={"class": 'db-tooltip__item__name'}).text.strip()
        tmp['quantity']     = int(item['data-stack'])
        tmp['image']        = item.find("img")['src']
        tmp['location']     = 'Company Chest'
        tmp['sub_location'] = item.find_parent('tbody')['id']
        items.append(tmp)
    return items

#Get all items in a retainers inventory (does not get number of crystals or gil)
#Does not handle HQ Items yet
def get_retainer_items(char_id,retainer_id,session_id):
    url = 'http://na.finalfantasyxiv.com/lodestone/character/'+str(char_id)+'/retainer/'+retainer_id+'/baggage/'
    soup_page = get_loadstone_page(url,session_id)
    #Get retainers name
    retainer_name = soup_page.find("div", attrs={"class": 'retainer--name'}).p.text.strip()
    #Get all items
    raw_items=soup_page.find_all("tr", attrs={"data-default_sort": True})
    #Parse the items
    items=[]
    for item in raw_items:
        #if(is_item_hq(item,session_id)):
            #print("HQ")
        tmp = {}
        tmp['name']         = item.find("a", attrs={"class": 'highlight'}).text.strip()
        tmp['quantity']     = int(item['data-stack'])
        tmp['image']        = item.find("img")['src']
        tmp['location']     = 'Retainer:  ' + retainer_name
        tmp['sub_location'] = 'Inventory'
        items.append(tmp)
    return items

#Get all items a retainer is selling (does not get number of crystals or gil)
#HQ Item handling is suspect
#Note:  This may return already sold items:
#       sale_inventory is supposed to filter those out, but I din't think it's working correctly
def get_retainer_selling(char_id,retainer_id,session_id):
    url = 'http://na.finalfantasyxiv.com/lodestone/character/'+str(char_id)+'/retainer/'+retainer_id+'/market/'
    soup_page = get_loadstone_page(url,session_id)
    #Get retainers name
    retainer_name = soup_page.find("div", attrs={"class": 'retainer--name'}).p.text.strip()
    #Get all items
    sale_inventory=soup_page.find("div", attrs={"class": 'active'})
    raw_items=sale_inventory.find('tbody').find_all("tr")
    #Parse the items
    items=[]
    for item in raw_items:
        tmp = {}
        tmp['name']         = item.find("a", attrs={"class": 'highlight'}).text.strip()
        tmp['quantity']     = int(item.find("td", attrs={"class": 'even'}).text.strip())
        tmp['image']        = item.find("img")['src']
        tmp['location']     = 'Retainer:  ' + retainer_name
        tmp['sub_location'] = 'Selling'
        tmp['is_hq']        = bool(item.find("img", src = re.compile('http://img\.finalfantasyxiv\.com/lds/pc/global/images/common/ic/hq.png.*')))
        items.append(tmp)
    return items
