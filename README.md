Django-CherryPy-PyInstaller-Standalone
======================================

An example application that demonstrates a Django/CherryPy application frozen into an executable using PyInstaller. 



I recently spent the better part of two days trying to get a working Django/WSGI/CherryPy application frozen into a windows executable. Much of what I found on via Google was from 2008 or spread throughout many StackOverflowposts. The three working examples here should help anyone trying to do build a similar application. Pay special attention to the "serve.spec" files in the windows builds, as well as the "serve.py" file in all three where Django and CherryPy are hooked up. 
