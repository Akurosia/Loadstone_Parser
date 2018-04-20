#Loadstone Parser

The Loadstone Parser is a python project to parse and extract Character data from the Loadstone.  The social site for Final Fantasy XIV (14).  In its current form this allows players to see the inventory of all their retainers and their Free Company chest.

#Why

Final Fantasy XIV has multiple inventory areas.  Unfortunately, these areas scattered about and players can not easily view everything at once.  While there is a search for item feature, it only works for single items and does not find upgraded versions.  This is made all the worse by the limited number of inventory slots.  If a player has a stackable item in two locations, that item is taking up two precous slots instead of a single slot.

#What's Missing

Quite a bit.  The largest piece of missing functionality is the ability to log-in.  
Once that's done the next focus is character information.  
Then we can focus on usability improvements, like making the data sortable in the browser.

One major feature that is missing is seeing a character's own inventory.  The Loadstone doesn't appear to provide that information, so there is nothing we can do.

#Installation
First, install Python 3.  Then run these commands:
```
pip install requests
pip install bs4
```

#How to Use

The first step is to obtain a valid session cookie.

Currently players must manually visit `finalfantasyxiv.com/lodestone/` and log-in.  
Next they need to press `ctrl+shift+c` to acess the debug menu of their browser.

* On Chrome:  
Select Resources, then Cookies, then the website.  Next right click the `Value` fiels of `ldst_sess` and select copy.

* On Firefox:  
Select Web-Storage, then Cookies, then the website.  Next copy the value of `ldst_sess`.

Paste the session_id into the appropriate field of `get_all_items.py` and run `get_all_items.py`

<char_id>.html will now contain a list of all items the player can see.

#Additions (NOT usefull for everyone)
If you have an Apache with cgi enabled you can set "useHTML" to 'True' to enable directly access the result from a browser. (mostly only usefull for me ^^)

If you want to use filter and export functionality, you have to link the included css and js files + a jquery.js file (you can find this online easily).

For images of shards, crystals and polycrystals replace {yourDomain} inside css file and change the path to a correct location (in my case 1. url represented the crystal type and 2. url the elment).