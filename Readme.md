#Loadstone Parser

The Loadstone Parser is a python project to parse and extract Character data from the Loadstone.  The social site for Final Fantasy XIV (14).  In its current form this allows players to see the inventory of all their retainers and their Free Company chest.

#Why

Final Fantasy XIV has multiple inventory areas.  Unfortunately, these areas scattered about and players can not easily view everything at once.  While there is a search for item feature, it only works for single items and does not find upgraded versions.  This is made all the worse by the limited number of inventory slots.  If a player has a stackable item in two locations, that item is taking up two precous slots instead of a single slot.

#What's Missing

Quite a bit.  The largest piece of missing functionality is the ability to log-in.  Once that's done the next focus is character information.  Things like character id, Free Company id, and retainer ids.  Those currently have to be manually input by the user.  Then we can focus on usability improvements, like making the data sortable in the browser.

One major feature that is missing is seeing a character's own inventory.  The Loadstone doesn't appear to provide that information, so there is nothing we can do.


#How to Use

The first step is to obtain a valid session cookie.

Currently players must manually visit `finalfantasyxiv.com/lodestone/` and log-in.  Next they need to press `ctrl+shift+c` to acess the debug menu of their browser.

* On Chrome:  Select Resources, then Cookies, then the website.  Next right click the `Value` fiels of `ldst_sess` and select copy.


Next we need to obtain all of the ids.  These are strings of numbers for different pages in the URL bar.

* Free Company:

    ```
    http://na.finalfantasyxiv.com/lodestone/my/#myfc
    Click on the name of your Free Company
    ```

* Character:
    Click your name under `Character Profile`

* Retainers:
    From that page click `Retainers`
    You will now need to select each individual retainer from the drop down menu, while copying each id from the URL bar.


Paste all this information into the appropriate fields of `get_all_items.py` and run `get_all_items.py`

Test.html will now contain a list of all items the player can see.
