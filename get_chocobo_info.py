
#http://na.finalfantasyxiv.com/lodestone/character/12358054/retainer/8850d448c0/baggage/20/tooltip/

a_page = get_loadstone_page('http://na.finalfantasyxiv.com/lodestone/character/12358054/buddy/',session_id)
a_section=a_page.findAll("div", { "class" : "base_body" })
write_data(a_section[1])

 <head>
  <!-- ** CSS ** -->
  <link href="http://img.finalfantasyxiv.com/lds/pc/global/css/lodestone.css?1467272369" rel="stylesheet"/>
  <link href="http://img.finalfantasyxiv.com/lds/pc/global/css/add/lodestone.css?1467272369" rel="stylesheet"/>
  <link href="http://img.finalfantasyxiv.com/lds/pc/global/css/style.css?1467272263" rel="stylesheet"/>
  <link href="http://img.finalfantasyxiv.com/lds/pc/global/css/setindex.css?1467272263" rel="stylesheet"/>
  <link href="http://img.finalfantasyxiv.com/lds/pc/global/css/jquery.fancybox.css?1467272263" rel="stylesheet"/>
  <link href="http://img.finalfantasyxiv.com/lds/pc/en/css/base.css?1467272211" rel="stylesheet"/>
  <link href="http://img.finalfantasyxiv.com/lds/pc/global/css/eorzea_db.css?1467272263" rel="stylesheet"/>
  <script src="lodestone.plugin.bbcode_render.js"></script>
 </head>

#opacity: 1; left: 0px; display: block;
