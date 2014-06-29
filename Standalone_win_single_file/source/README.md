To build you need the following modules

Cherrypy 3.2.3

Django 1.6.5

pyinstaller 2.1



from the main directory where "serve.py" lives run: pyinstaller -F serve.spec

this will generate a "build" directory (you and delete this) and a "dist" directory where you will find "serve.exe"

DB changes don't persist between sessions and the static files don't aren't working, though they are being picked up. You can confirm this by looking in Appdata/Local/Temp/_MEIxxxxx where "xxxxx" is the session generated when you run the executable. (example: "C:\Users\...\AppData\Local\Temp\_MEI59402") There is a static directory but Django can't see it, but has no problem seeing the "templates" directory. weird...

Admin panel doesn't work.

Login UN/PW: user/foo
