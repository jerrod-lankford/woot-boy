#Woot Boy

Woot Boy is a server friendly, instant notifier for woot-offs. Notifications are displayed popup style in the corner of the window. It tries its best to keep a load off the server while still instantly notifying you of new items as they come up.

##FAQ

What is with the name woot boy?
I accidently hit the 'y' instead of the 't' and I didn't feel like changing it.

Server friendly you say?
Yes, on a technical level I parse the progress bar and adjust the refresh rate accordingly. They change but at the moment these are the refresh thresholds:

75-100%: 260s
50-75%: 180s
25-50%: 120s
10-25%: 50s
5-10%: 20s
2-5%: 5s
1-2%: 1s
Sold-out: 1s

Truth is some items are occasionaly missed but I plan on fixing as much as I can, while still being friendly to the woot servers.

How do I compile/use this?

Simple, you need to have python and wxPython installed (tutorial coming soon).
Then just run it!

pyton woot-boy.py

The gui is currently blank, im just using the frame for toaster box purposes but there is a menu dropdown that will let you start and stop the bot.

##TODOS:

-Add a quick item check (some items sell out ~1 minute)

-Fix some bugs with item switchovers
-Write a gui
-Make it fully configurable.
-Add a systray icon
-Crashes because the image is a png or gif (Still throws error but doesnt crash)
-Crashes during lunch sale (Crashes due to the format of the percentage
-Make resolution detection automatic (Done)


