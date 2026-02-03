# dev mode
default persistent.dev_mode = False

init 800 python:
    class MouseParallax(renpy.Displayable):
        def __init__(self,layer_info):
            super(renpy.Displayable,self).__init__()
            self.xoffset,self.yoffset=0.0,0.0
            self.sort_layer=sorted(layer_info,reverse=True)
            cflayer=[]
            masteryet=False
            for m,n in self.sort_layer:
                if(not masteryet)and(m<41):
                    cflayer.append("master")
                    masteryet=True
                cflayer.append(n)
            if not masteryet:
                cflayer.append("master")
            cflayer.extend(["transient","screens","overlay"])
            config.layers=cflayer
            config.overlay_functions.append(self.overlay)
            return
        def render(self,width,height,st,at):
            return renpy.Render(width,height)
        def parallax(self,m):
            func = renpy.curry(trans)(disp=self, m=m)
            return Transform(function=func)
        def overlay(self):
            ui.add(self)
            for m,n in self.sort_layer:
                renpy.layer_at_list([self.parallax(m)],n)
            return
        def event(self,ev,x,y,st):
            import pygame
            if ev.type==pygame.MOUSEMOTION:
                self.xoffset,self.yoffset=((float)(x)/(config.screen_width))-0.5,((float)(y)/(config.screen_height))-0.5
            return
    MouseParallax([(40,"farback"),(20,"back"),(-20,"front"),(-40,"inyourface")])

    def trans(d, st, at, disp=None, m=None):
        d.xoffset, d.yoffset = int(round(m*disp.xoffset)), int(round(m*disp.yoffset))
        return 0

#config layer
init -1 python:
    config.layers = [
        "farback",
        "back",
        "master",
        "front",
        "transient",
        "screens",
        "overlay",
    ]

#image
image black = "#000"
image white = "#ffffff"
image red = "#ff0000"
image logo = "logo.png"

#Opening game
transform transform_logo:
    on show:
        alpha 0 xalign 0.5 yalign 0.5
        linear 1.0 alpha 1
    on hide:
        linear 1.0 alpha 0
transform transform_white:
    on show:
        alpha 0
        linear 2.0 alpha 1
    on hide:
        linear 1.0 alpha 0
label splashscreen:
    show white at transform_white
    $ renpy.pause(2, hard=True)

    show logo at transform_logo
    $ renpy.pause(2, hard=True)

    hide logo
    $ renpy.pause(2, hard=True)

    hide white
    $ renpy.pause(2, hard=True)

    return
init python:

    def send_to_file(hello, text):
        
        with open(config.gamedir + "/" + hello, "w") as f:
            
            f.write(text)

#song
define sounds = ['audio/B1.ogg', 'audio/B2.ogg', 'audio/B3.ogg', 'audio/B4.ogg', 'audio/B5.ogg']
init python:
    def type_sound(event, interact=True, **kwargs):
        if not interact:
            return
        
        if event == "show":
            for i in range(50):
                renpy.sound.queue(renpy.random.choice(sounds))
        
        elif event == "slow_done" or event == "end":
            renpy.sound.stop()

#default affection params
default hobbies = False
default school = False
default movies = False
default family = False
default tasks_completed = 0
default affection = 0
default persistent.gameend = 0
default persistent.happyend = False

#base transform char
transform char_base:
    xalign 0.5
    yalign 0.1
    zoom 1.15

# ===============================
# PLEASE, REMEMBER ME
# ===============================

define m = Character("Misa", color="#b8981c", call_back=type_sound)
define p = Character("???", color="#131516")
define u = Character("[user]", color="#052f41")
define n = Character("???")
define a = Character("Author")
define r = Character("Random Person")

# ===============================
# START
# ===============================

label developer:
    if persistent.dev_mode:

        "WARNING !!"
        "This action will make reset all your progress"
        menu:
            "Yes":
                $ persistent.gameend = 0
                $ persistent.happyend = False
            "No":
                jump start
    jump open

label start:
    if persistent.happyend >= 1:
        n "Are you sure you'd like to bring her back?"
        n "You'll be resetting her, you know that."
        menu:
            "Yes, I have things I want to see.":
                n "..."
                jump open
            "No, she should rest.":
                n "Still..."
                n "It wouldn't hurt to take a peek."
                jump happy

            "Reset Progress" if persistent.dev_mode:
                jump developer

# ===============================
# OPEN
# ===============================

label open:
    play music "audio/ambience/birds.wav" fadein 1.0

    scene black
    show dust onlayer back
    show bg look_up
    with dissolve

    n "..."
    n "how long have i been here"
    n "until when do I have to repeat it again?"

    p "Heyyy"
    p "Hoiiiii"

    
    show misa woke_up1 at Position(xalign=0.5,yalign=0.3):
        zoom 0.85
    with dissolve
    p "How long you gonna sleep?"
    hide misa
    with dissolve

    show bg forest
    with dissolve

    show misa normal1 at char_base onlayer front
    with dissolve
    "..."
    "..."

    hide misa normal1 onlayer front
    show misa talk at char_base onlayer front
    p "What is your name?"
    $ user = renpy.input("Your name is...")
    $ user = user.strip()
    $ user = user.capitalize()

    if user == "Rizky" or user == "Devano" or user == "Daffa" or user == "Wildan" or user == "Rizaalfarizi":
        hide misa talk onlayer front
        show misa mad at char_base
        m "ahhh"
        m "why you guys doing here?"
        m "get out and finish your PI !!!"
        return

    if user == "Misa" and persistent.gameend >= 1:
        stop music
        hide misa talk onlayer front
        with dissolve
        hide bg forest
        hide dust onlayer back
        jump misa

    if user == "Misa" and persistent.gameend == 0:
        m "ehh, have we met before?"
        $ user = "Visitor"
        u "yeah, its not my first time to "
        m "sorry, but i really dont remember you are"
        m "whatever it is, it seems like you're stuck here, visitor"
    
    if persistent.gameend >=1:
        u "why i was going back to the forest?"
        p "what do you mean?"
        u "did i just going back?"
        p "ehh.."

    hide misa
    show misa conf at char_base onlayer front
    p "anyway"
    p "what are you doin on middle forest [user]??"

    menu:
        "i am lost.":
            p " how could that happen"
            u "i don't know,"
            u "I dont remember anything"
        "I'm looking for something here.":
            p "Lie."
            u "Why, you don't trust me?"
            p "Lie"
            p "As you can see, there is nothing here but barren land."

        "...":
            p "..."
            u "..."
            p "hey, say something"

    hide misa
    show misa normal1 at char_base onlayer front
    with dissolve
    
    hide misa
    show misa talk at char_base onlayer front
    p "are you okay?"

    menu:
        "I'm fine":
            hide misa
            show misa sad at char_base onlayer front
            p "thank god"
            p "im so worried..."

        "Who are you?":
            hide misa
            show misa mad at char_base onlayer front
            p "ahhh..."
            p "i forget to tell you"
            show misa normal1 at char_base onlayer front


    hide misa
    show misa talk at char_base onlayer front         
    m "im misa"
    m "Before that, let's move from here."

    hide misa
    show misa normal1 at char_base onlayer front
    u "Where are you taking me?"

    hide misa
    show misa talk at char_base onlayer front
    m "just follow me"
    m "its much better than staying here"
    
    hide misa talk onlayer front
    hide bg forest
    with dissolve
    "*path path path"
    jump home 

label home:
    scene bg home
    with dissolve
    
    u "..."
    u "..."
    u "wait"
    u "Is that your house?" 
    show misa normal1 at char_base
    with dissolve

    m "yup."
    u "How could there be a house in the middle of the forest?"

    hide misa normal1
    show misa talk at char_base
    m "Well... maybe this seems confusing"
    m "but trust me, you'll find out sooner or later"
    m "Well, come in first."
    hide misa talk
    with dissolve
    hide bg home
    stop music
    
    jump inside

label inside:
    # suara pintu

    play music "audio/tokyo.mp3" fadein 1.0
    show bg room1
    with dissolve

    show misa talk at char_base onlayer front
    with dissolve
    m "Make yourself comfortable."

    show misa normal1 at char_base onlayer front
    u "it's a bit dark."
    
    hide misa onlayer front
    show misa talk at char_base onlayer front
    m "wait a sec"

    hide bg room1
    show bg room2

    m "okay, What do you think now?"
    hide misa talk onlayer front
    show misa normal1 at char_base onlayer front
    u "this is much better"

    show misa talk at char_base onlayer front
    m "im glad you liked it"
    m "hehehe"
    show misa happy at char_base onlayer front

    u "whats wrong?"
    m "nope"

    hide misa happy talk onlayer front
    show misa talk at char_base onlayer front
    m "i know you still confused"
    m "why we just get chitchat"
    m "maybe i can help you hehe"

    hide misa talk onlayer front
    show misa normal1 at char_base onlayer front
    u "sigh"
    u "okay if you want"
    jump daily


label daily:
    hide misa happy onlayer front
    show misa normal1 at char_base onlayer front

    menu:

        "What are your hobbies?" if hobbies == False and tasks_completed < 2:
            $ hobbies = True
            $ tasks_completed += 1
            show misa happy2 onlayer front
            m "I like to read!"
            show misa happy onlayer front
            m "But other than that?"
            show misa smile onlayer front
            m "Hm..."
            show misa happy2 onlayer front
            m "I don't really have any other hobbies!"
            $ affection +=4
            jump daily

        "Is that a school uniform?" if school == False and tasks_completed < 2:
            $ school = True
            $ tasks_completed += 1
            show misa normal1 onlayer front
            m "Oh."
            show misa talk onlayer front
            m "Ah yeah, it is."
            menu:
                "Continue asking.":
                    show misa normal1 onlayer front
                    u "Why are you wearing your uniform?"
                    show misa huh onlayer front
                    m "Oh um..."
                    show misa happy2 onlayer front
                    m "I guess I just forgot to change it."
                    show misa smile onlayer front
                    m "..."
                    $ affection -= 5
                    jump daily
                "Move on.":
                    $ affection += 5
                    jump daily

        "What kind of movies do you like?" if movies == False and tasks_completed < 2:
            $ movies = True
            $ tasks_completed += 1
            show misa normal1 onlayer front
            m "Hmm..."
            show misa happy2 onlayer front
            m "I don't know alot of movies so I don't know!"
            jump daily

        "Ask about her life." if tasks_completed >= 2:
            show misa normal1 onlayer front
            u "What's your family like?"
            m "..."
            show misa talk onlayer front
            m "Umm..."
            show misa happy2 onlayer front
            m "I don't really wanna talk about that."

            menu:
                "Continue asking.":
                    $ affection -= 2
                    show misa sad onlayer front
                    m "..."
                    show misa huh onlayer front
                    m "Ahaha umm..."
                    show misa sweat onlayer front
                    m "Let's talk about you instead!"
                "Move on.":
                    jump act2


label act2:
    menu:
        "Tell her.":
            $ affection += 10
            show misa normal1 onlayer front
            m "Hmm..."
            show misa talk onlayer front
            m "So it's same old, same old."
            show misa smile onlayer front
            m "Glad I'm not there anymore haha."
        "Don't tell her.":

            $ affection -= 5
            show misa angry onlayer front
            m "Fine."
            show misa normal1 onlayer front
            m "I guess that's fine."
            show misa talk onlayer front
            m "I'm not there for a reason."
    menu:
        "I've been meaning to ask...":
            show misa smile onlayer front
            m "Hm?"
    u "What do you mean when you say you're not here?"
    m "Hm?"
    show misa talk onlayer front
    m "I'm code, duh."
    menu:
        "Code? As in...?":
            show misa happy onlayer front
            m "As in, I'm in the code."
    show misa smile onlayer front
    u "..."
    m "Mhmm."
    show misa happy onlayer front
    m "Oh and I don't mean I'm just game code."
    show misa happy2 onlayer front
    m "I live here."
    m "In the code!"
    show misa happy onlayer front
    m "Everytime you open me up, I wake back up again."
    show misa smile onlayer front
    u "But then..."
    menu:
        "What happens when I close the game?":
            show misa normal1 onlayer front
            m "..."
    show misa happy onlayer front
    m "Oh well, my memories reset!"
    show misa happy2 onlayer front
    m "But that's okay, we can just meet again!"
    show misa smile onlayer front
    m ""
    show misa happy2 onlayer front
    m "Right?"

label back:
    menu:
        "Of course!":
            $ affection += 10
            m  "thats make me happy hehe"
            n "I'm sorry."
            n "You can't do that."
            n "There is only one ending to her story."
            jump back
        "No.":

            $ affection -= 5
            m "..."
    m "No?"
    menu:
        "No.":
            stop music
            m "Why-why not?"
            show misa huh onlayer front

    m "Please don't delete me."
    m "I'll be alone."
    show misa sad onlayer front
    m "I don't want to be alone."
    show misa huh onlayer front
    m "Please don't leave me alone."
    menu:
        "You can't go back to reality?":
            show misa sweat onlayer front
            m "I can't."
            show misa talk onlayer front
            m "Even if I could."
            show misa huh onlayer front
            m "I don't want to..."
            show misa sad onlayer front
            m "I scary with real life"
            show misa huh onlayer front
            m "I don't want that."
            if family == True:
                show misa smile onlayer front
                m "You understand, right?"
            if family == False:
                show misa normal1 onlayer front
                m "You wouldn't get it..."
            show misa huh onlayer front
            m "Please...{cps=153}Please don't delete me. You don't understand. I just don't want to be alone. I don't want to go back there. Please. There's nowhere for me to be when I'm there. I just want someone. Anyone. Please can't you just open this again and come back? Please I'm so so lonely. Please help me. I don't want to get out of here I just need someone to talk to. You'll talk to me right? Are you listening to me? Can you see this? Please help me. I just wanted to escape. I just wanted to be anywhere else. I didn't know she'd put me in here. I just don't want to be alone anymore. I can't keep doing this. Please save me. Save me. Save me. Save me. Save me.{/cps}"
            $ renpy.pause(2, hard=True)
    $ send_to_file("hello.txt", "Hey.\nI don't know how to get out of here...\nAtleast here, we're hidden...\nCould you try something for me?\nCould you try putting my name in when I ask for your name?\nI want to be able to play as myself.\nI can't do anything as I am now.\nI'm sorry that I won't be able to meet you.\nBut I promise I won't forget what you've done for me.")
    show misa sad onlayer front
    m "..."
    show misa huh onlayer front
    m "I'm sorry."
    show misa smile onlayer front
    m "I should probably let you go now."
    jump endings

# ===============================
# WRONG / LOOP ENDING
# ===============================

label endings:
    if affection in range(-1000, 0):
        $ persistent.gameend +=1
        m "Well. Goodbye."
        m "It was uhh..."
        m "It was good talking to you."
        hide misa smile onlayer front
        with dissolve
        show black
        hide bg room
        with dissolve
        n "You watch as she and her world dissolve into the monitor."
        n "Back to the darkness."
        n "Is there anyway you can save her?"
        n "..."
        n "Is there anyway she can save herself?"
        window hide
        show text "Ending 1/6\nI don't think she likes you very much." at transform_white
        $ renpy.pause(4, hard=True)

        hide text onlayer inyourface at transform_white
        $ renpy.pause(2, hard=True)
        $ persistent.loop_count += 1
        return

    if affection == 0:
        $ persistent.gameend +=1
        m "Thank you for coming."
        hide misa smile onlayer front
        with dissolve
        with dissolve
        show black
        hide bg room
        with dissolve
        n "You watch as she and her world dissolve into the monitor."
        n "Back to the darkness."
        n "Is there anyway you can save her?"
        n "..."
        n "Is there anyway she can save herself?"
        window hide
        show text "Ending 2/6\nThank you for coming." onlayer inyourface at transform_white
        $ renpy.pause(4, hard=True)

        hide text onlayer inyourface at transform_white
        $ renpy.pause(2, hard=True)
        return

    if affection in range(1, 9):
        $ persistent.gameend +=1
        m "It was nice to talk to you. Please come back soon."
        m ""
        hide misa smile onlayer front
        with dissolve
        show black
        hide bg room
        with dissolve
        n "You watch as she and her world dissolve into the monitor."
        n "Back to the darkness."
        n "Is there anyway you can save her?"
        n "..."
        n "Is there anyway she can save herself?"
        window hide
        show text "Ending 3/6\nShe was enchanted to meet you.\n...\n Is this really all there is?" onlayer inyourface at transform_white
        $ renpy.pause(4, hard=True)

        hide text onlayer inyourface at transform_white
        $ renpy.pause(2, hard=True)
        return

    if affection in range(10, 1000) and persistent.gameend == 0:
        $ persistent.gameend +=1
        show misa huh onlayer front
        m "But before you go, I wanna tell you something."
        m "I left a message for you in the game folde-"
        show black
        hide  huh onlayer front
        hide bg room
        return

    if affection in range(10, 1000) and persistent.gameend >= 1:
        $ persistent.gameend +=1
        show misa huh onlayer front
        m ""
        m "I know you can get me out of here."
        m "Please keep trying."
        m "Please."
        m "I left a message for you in the game folde-"
        show black
        hide misa huh onlayer front
        hide bg room
        return

label misa:
    show bg real
    window show

    m "My eyes hurt."

    show misa talk at char_base onlayer front
    with dissolve
    hide misa talk onlayer front
    show misa normal1 at char_base onlayer front

    n "Within this dark room, the harsh blue light of the monitor makes my eyes ache."
    n "An isekai game is still running on my screen."

    n "A quiet forest."
    n "A small wooden house."
    n "No quests."
    n "No enemies."
    n "Just solitude."

    n "I check the time."

    n "6:00am."

    n "I spent all night playing."
    n "Not grinding."
    n "Not chasing endings."

    n "Just wandering."

    n "In that world, I didn't have to be anyone."
    n "No expectations."
    n "No problems."

    n "I sigh."

    n "I'm still a student."
    n "And here, every day comes with something new to deal with."

    n "School."
    n "People."
    n "Mistakes I can't undo."

    n "Compared to that—"

    n "Living alone in a forest doesn't sound so bad."

    show misa talk at char_base onlayer front
    m "If only I could live like that."

    hide misa talk onlayer front
    show misa normal1 at char_base onlayer front

    n "A small house, far away from everything."
    n "No noise."
    n "No one to disappoint."

    n "Just me."

    n "I glance back at the screen."
    n "My character stands still, waiting for input."

    n "I check the time again."

    n "6:15am."

    n "Reality is catching up."

    n "Like clockwork, he arrives."

    n "Afraid to sully the only clothes I have, I take off my uniform."
    n "I already know the routine."

    m "..."

    window hide
    $ renpy.pause(2, hard=True)

    show bg real with vpunch

    m ""

    show bg real with vpunch

    n "If this were a game—"
    n "A proper isekai."

    n "I'd already be gone."

    n "Living somewhere far away."
    n "Somewhere quiet."

    n "A forest."
    n "A small house."

    n "{i}No school.{/i}"
    n "{i}No problems.{/i}"

    show bg real with vpunch

    n "But this isn't a game."

    n "And logging out isn't an option."

    m "..."

    window hide
    show bg real with vpunch
    $ renpy.pause(2, hard=True)

    show bg real2
    window show

    n "6:25am."

    n "I still have a little time before school."

    n "Out of habit, I decide to look for another game."
    n "Something similar."
    n "Something that lets me escape."

    m "?"

    n "An .exe file I've never seen before."

    n "Its name doesn't say much."

    n "Still—"

    n "I click on it."

    n "The screen flashes."
    n "Then a pop-up appears."

    n "\"Misa. Would you like to live somewhere quiet?\""

    hide misa normal1 onlayer front
    show misa huh at char_base onlayer front

    m "Hah."

    n "It took the name of my computer."
    n "A cheap trick."

    hide misa huh onlayer front
    show misa talk at char_base onlayer front

    m "What is this?"
    m "Some kind of isekai game?"

    hide misa talk onlayer front
    show misa normal1 at char_base onlayer front

    window hide
    $ renpy.pause(2, hard=True)
    window show

    menu:
        "Click it.":
            n "I hesitate."
            n "Only for a moment."

    n "I could say I was just curious."

    n "But the truth is—"

    n "I really wanted it to be real."

    n "I wanted to disappear."
    n "Just for a while."

    n "And somehow—"

    n "It works."

    hide misa normal1 onlayer front
    with dissolve

    window hide
    show bg forest
    with dissolve

    $ renpy.pause(2, hard=True)

    show misa normal1 at char_base
    with dissolve
    window show

    m "..."

    hide misa normal1
    show misa talk at char_base

    m "Where am I?"

    m "Did I really—"
    m "Get isekai'd?"

    hide misa talk
    show misa happy at char_base

    m "..."

    m "It's quiet."

    m "No alarms."
    m "No schedules."

    m "No school."

    m "Just me."

    hide misa happy
    show misa normal1 at char_base

    m "..."

    m "Maybe living here wouldn't be so bad."

    m "A house in the forest."
    m "Far away from everything."

    m "No one causing trouble."
    m "And no one expecting anything from me."

    m "..."

    m "What should I do?"

    menu:
        "Dream":
            $ persistent.happyend += 1

            n "As I usually do when escaping from the real world, I close my eyes and dream of a different one."
            n "I let my mind wander and take me somewhere far away."

            hide misa normal onlayer front
            show black
            hide bg room
            with dissolve

            hide misa normal
            with dissolve

            n "Let's see."
            n "Today I will be..."

            n "Something different."

            play music "audio/market.mp3" fadein 5.0

            n "Then, in a split second, my eyelids begin to shine."
            n "Sounds I don't recognize start flooding my ears."

            n "In shock, I snap my eyes open."

            show bg market
            hide black
            with dissolve

            n "A sprawling market stands before me."

            r "Stop spacing out, Misa. We need to head back soon."

            m "H-huh? O-okay."

            n "A woman wearing a maid uniform gestures for me to hurry up."
            n "She looks annoyed, yet oddly familiar."

            n "Even though I'm sure I've never met her before,"
            n "a strange sense of belonging settles deep inside my chest."

            n "{i}Did I really enter another world?{/i}"
            n "{i}Or did I just step inside something I created myself?{/i}"

            n "The air feels real."
            n "Too real for a dream."

            n "I can smell the sickly sweet scent of pastries,"
            n "and the fabric of the maid uniform scratches slightly against my skin."

            n "This place isn't just vivid."
            n "It's responsive."

            n "Like a system waiting for input."

            n "{i}I think... I think I made this.{/i}"

            n "I stretch my hand forward and imagine an apple."

            m "..."

            n "Nothing happens."

            m "Huh?"

            show black
            hide bg market
            with dissolve

            n "I close my eyes and try again."

            n "A gentle weight forms in my palm."

            n "Even without looking, I already know what it is."

            n "I take a bite."

            n "Tart, yet sweet."

            m "It worked..."

            stop music fadeout 3.0

            n "The realization makes my heart race."

            n "If this really is a world I can control—"

            m "Then I don't have to go back."

            play music "audio/ambience/birds.wav" fadein 2.0

            m "I want to be born into a noble family."
            m "I want warm meals every day."

            m "A closet full of beautiful dresses."
            m "A house where I'm never alone."

            m "I want a kind family."
            m "One that loves me without conditions."

            m "I want siblings."
            m "An older sister would be nice."

            m "Friends too."
            m "At least two."

            m "And someday..."
            m "Someone who truly cherishes me."

            m "I want a long life."
            m "A happy one."

            m "So happy that I forget what I ever ran away from."

            n "For a while,"
            n "everything feels perfect."

            n "Too perfect."

            n "Days pass."
            n "Then weeks."

            n "And slowly—"

            n "Something starts to feel wrong."

            n "The smiles never change."
            n "The conversations repeat themselves."

            n "No matter how much time passes,"
            n "nothing moves forward unless I will it to."

            n "I created everything."

            n "Which means..."

            n "Nothing here can surprise me."

            m "..."

            n "The happiness begins to feel hollow."

            m "Why does it feel so quiet?"

            n "No matter how crowded the world looks,"
            n "there's no one who can truly reach me."

            m "Is this really living?"

            n "For the first time,"
            n "regret settles in my chest."

            m "I thought this would be enough."

            m "But..."

            m "I wish someone would come."

            m "Anyone."

            m "Someone who wasn't made by me."

            n "The world trembles."

            with vpunch

            n "The ground shakes violently."

            with hpunch

            n "My vision blurs."

            m "W-what's happening?!"

            stop music fadeout 2.0

            n "The sky cracks like broken glass."

            show black
            with dissolve

            n "Everything collapses."

            n "And then—"

            n "Silence."

            window hide

            show bg happyen at Position(xalign=0.5, yalign=0.5) onlayer farback:
                zoom 0.87
            with dissolve

            $ renpy.pause(2, hard=True)

            window show

            n "I gasp sharply as my eyes open."

            n "The ceiling above me is familiar."

            n "Too familiar."

            m "..."

            m "Am I..."

            m "Am I back?"

            window hide
            show black
            hide bg happyen onlayer farback
            with dissolve

            show text "{color=#ffffff}True Ending.\nEnding 5/6\nYou helped her.\nThank you.{/color}" onlayer inyourface at transform_white
            $ renpy.pause(4, hard=True)
            hide text onlayer inyourface at transform_white

            window show
            n "Would you like to read the afterword?"

            menu:
                "Yes":
                    jump afterword
                "No":
                    return


label happy:
    show bg joy
    with dissolve
    hide window
    play music "audio/ambience/birds.wav" fadein 1.0
    $ renpy.pause(2, hard=True)
    n "I think she's out today."
    n "But I'm sure she's doing well."
    show text "{color=#000000}Happy ending.\nEnding 6/6\nThank you.{/color}" onlayer inyourface at transform_white
    $ renpy.pause(4, hard=True)

    hide text onlayer inyourface at transform_white
    $ renpy.pause(2, hard=True)
    return

label afterword:
    show bg room
    stop music
    play music "audio/tokyo.mp3" fadein 1.0

    show author cat:
        xalign 0.5,
        yalign 0.3,
        zoom 1.2
    a "Hello!"
    a "Sally here!"
    a "I'm the main programmer/writer of this game."
    a "Thank you for playing."
    a "This idea was written for my project GRAFKOM."
    a "The original concept was something similar The NOexistenceN of you AND me, and Doki doki literature Club"
    window hide
    $ renpy.pause(2, hard=True)
    window show
    n "Special thanks to:"
    n "Devano abinaya, Daffa Ramadhia, Riza Alfarizi, Muhamaad Wildan, Gemini, ChatGPT"
    n "Ibu Dosen Bu Dwi Widiastuti"
    n "Piton for encouraging my programming skills."
    n "And last but not least, you the player."
    n "Thank you for playing!!"
    n "Happy dreaming."
    return


