#!/bin/python3
#Obtain a list of all items owned by a character
#Copyright Arthur Moore 2016
#TODO:  Get character inventory

from parse_loadstone import *

session_id   = ''
character_id = ''
fc_id        = ''
retainer_ids = ['','']


items = get_fc_items(fc_id,session_id)

for retainer_id in retainer_ids:
    items +=get_retainer_items(character_id,retainer_id,session_id)
    items +=get_retainer_selling(character_id,retainer_id,session_id)

#To sort the list by item name
items = sorted(items, key=lambda k: k['name'])

write_data(list_items_table(items))
