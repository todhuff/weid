#weid
A simple program to display security cameras, written in python.

## Depends:
Python 2.x, python-configobj, fonts-droid, other stuff.

## Overview
Weid is a relatively simple program to display IP cameras.
It was written to run on a Raspberry Pi driving an HDMI monitor.

I couldn't find anything to do what I wanted, so I wrote it myself.

The code is ugly. I didn't know python when I started, but pygame looked
like it had (almost) everything I needed, so I ran with it. This is the result.

When running the program directly from the console (without X), you must
be root.

Running under X requires no special permissions, though you
will need at least read access to /etc/weid/ (and any files therein).

## Installation
By hand, for now.

Personally, I have the Raspberry Pis that I use for monitoring set up to
auto-login the user 'pi' to the console, and append the following to 
/home/pi/.profile :

cd
git clone http://github.com/todhuff/weid.git >/dev/null 2>&1
cd weid
git pull >/dev/null 2>&1
./weid.py

That will make an initial clone (that will fail to run properly, since you
will need to copy the files in 'config' to /etc/weid/), and will update
to the latest version on every reboot. This may not be optimal in all
situations, as the program will fail to start if the configuration file options
change (which should happen rarely).

## Configuring
Use the source, Luke!

## Issues
If you have any issues, please log them at https://github.com/todhuff/weid/issues

Check the wiki for additional help / info - https://github.com/todhuff/weid/wiki

## Pronunciation, origin, meaning, etc.
Pronounced "W-ay-d". Weid is ancient Greek for "to know / to see".
