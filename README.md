# weid
A simple program to display security cameras, written in python.

## Depends:
Python 2.x, python-configobj, python-pygame, fonts-droid.

On the Pi, you can do this:
```
sudo aptitude install python-pygame python-configobj fonts-droid 
```
## Overview
Weid is a relatively simple program to display IP cameras.
It was written to run on a Raspberry Pi driving an HDMI monitor.

I couldn't find anything to do what I wanted, so I wrote it myself.

The code is ugly. I didn't know python when I started, but pygame looked
like it had (almost) everything I needed, so I ran with it. This is the result.

When running the program directly from the console (without X), you must
be root, or a user with access to the screen.

Running under X requires no special permissions, though you
will need at least read access to /etc/weid/ (and any files therein).

## Installation
By hand, for now.

Personally, I have the Raspberry Pis that I use for monitoring set up to
auto-login the user 'pi' to the console, and append the following to 
/home/pi/.profile :
```
cd
git clone http://github.com/todhuff/weid.git >/dev/null 2>&1
cd weid
git pull >/dev/null 2>&1
sudo ./weid.py
```
That will make an initial clone (that will fail to run properly, since you
will need to copy the files in 'config' to /etc/weid/), and will update
to the latest version on every reboot. This may not be optimal in all
situations, as the program will fail to start if the configuration file options
change (which should happen rarely).

## Configuring
Use the source, Luke!

In addition, the following information may be helpful.
Camera config sections follow this format:

```
[CAMERA NAME]
URL = 'STRING'
Authentication = BOOL
Username = 'STRING'
Password = 'STRING'
X_Position = INT
Y_Position = INT
Scaled = BOOL
X_Scale = INT
Y_Scale = INT
Enabled = BOOL
Sleep = INT
Show_Errors = BOOL
```

Other config sections are as follows (And should probably not be changed
unless you know what you're doing, and have a good reason):

```
[Time]
# Format is a standard datetime() format string
Format = "%a, %b %d, %Y - %I:%M %p"
# Change the font to something else if you don't want to install the Droid
# font.
Font = "/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf"
Font_Size = 36
X_Position = 20
Y_Position = 720
# Very light grey, very visible.
Colour = 200, 200, 200
# If set to false, don't bother displaying the time.
Enabled = True

[Tagline]
# The default is a little bit of frippery.
Format = "Weid - Room 101 Software"
# Change the font to something else if you don't want to install the Droid
# font.
Font = "/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf"
# Very small, almost invisible.
Font_Size = 8
X_Position = 1
Y_Position = 1
# Extremely dark grey; difficult to notice.
Colour = 35, 35, 35
# If set to false, don't bother displaying the tagline.
Enabled = True

[Defaults]
# Set to whatever you like; I use NTSC colourbars. The image will be
# auto-adjusted and auto-scaled as needed.
Error_Image="/etc/weid/oops.png"
```

If you don't want to install the droid font for some reason, Time & Tagline
would be the sections to change (Setting 'Enabled' to 'False' is not enough).


## Issues
If you have any issues, please log them at https://github.com/todhuff/weid/issues

Check the wiki for additional help / info - https://github.com/todhuff/weid/wiki

## Pronunciation, origin, meaning, etc.
Pronounced "W-ay-d". Weid is ancient Greek for "to know / to see".
