













define config.name = _("Please, remember me")





define gui.show_name = True




define config.version = "0.2"





define gui.about = _p("""
""")






define build.name = "Pleaserememberme"








define config.has_sound = True
define config.has_music = True
define config.has_voice = True













define config.main_menu_music = "audio/carousel.mp3"










define config.enter_transition = dissolve
define config.exit_transition = dissolve




define config.intra_transition = dissolve




define config.after_load_transition = None




define config.end_game_transition = None
















define config.window = "auto"




define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)







default preferences.text_cps = 20





default preferences.afm_time = 15
















define config.save_directory = "Anna-1691772531"






define config.window_icon = "gui/window_icon.png"






init python:




















    build.archive("TTest1","all") 
    build.archive("scripts", "all")  
    build.archive("images", "all")  

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.classify('**.md', None)
    build.classify('**.pdf', None)
    build.classify('**.psd', None)
    build.classify('**.doc', None)
    build.classify('**.txt', None)
    build.classify('**.xlsx',None)
    build.classify('game/**.rpy', None)
    build.classify('game/scripts/**.rpy', None)

    build.classify("game/**.rpyc", "scripts") 
    build.classify("game/**.jpg", "images") 
    build.classify("game/**.png", "images")
    build.classify("game/**.webp", "images")
    build.classify("game/**.webm", "images")
    build.classify('**/**.**', "TTest1") 









    build.documentation('*.html')
    build.documentation('*.txt')