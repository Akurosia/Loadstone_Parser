#!/usr/bin/python
# Obtain a list of all items owned by a character
# Copyright Arthur Moore 2016
# Updated and revised by Akurosia Kamo in 2018

# DO NOT REMOVE sys and parse_loadstone
import sys
from parse_loadstone import *
import cgi
import cgitb
import os
cgitb.enable()
print('Content-type: text/html\n\n')

def main():
        # check if session id was given as a parameter
        if len(sys.argv) < 2:
                session_id = ''
        else:
                session_id = sys.argv[1]
        # only continue if user specified a session_id
        if session_id != "":
                items = []
                character_ids = get_character_id(session_id)
                # used for-loop to avoid issues with invalid session_id
                for character_id in character_ids:
                        # Free Company Area, used for-loop to avoid issues in case user is not in a FC
                        free_company_ids = get_fc_id(character_id, session_id)
                        for free_company_id in free_company_ids:
                                #print("Searching for FC items in the FC chest if allowed!")
                                items = get_fc_items(free_company_id,session_id)
                        # Retainer Area, used for-loop to avoid issues in case user has no retainer
                        retainer_ids = get_retainer_ids(character_id, session_id)
                        for retainer_id in retainer_ids:
                                #print("Searching for items in Retainer: " + str(retainer_id) + "!")
                                items +=get_retainer_items(character_id,retainer_id,session_id)
                                items +=get_retainer_selling(character_id,retainer_id,session_id)

                        # To sort the list by item name and create an html file with the user id as name
                        if items != []:
                                items = sorted(items, key=lambda k: k['name'])
                                #print("Creating file " + str(character_id) + ".html with all items!")
                                htmldata = items2html(list_items_table(items))
                                write_data(character_id, htmldata)
                return character_id
        else:
                return ""
                #print("No session_id found!")

def html(character_id):
        print("<meta http-equiv=\"refresh\" content=\"0; URL=http://"+os.environ['SERVER_NAME']+"/cgi/"+character_id+".html\">")

if __name__ == "__main__":
    char_id = main()
    useHTML = False
    if useHTML:
        html(char_id)
