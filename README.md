Simple program to display security cameras.
Written by Tod D. Huff
thuff@warmerbythelake.com
PLEASE send bug reports, requests, and improvements to me!

Depends: Python 2.x, python-configobj, fonts-droid, other stuff.

Coeptum is a relatively simple program to display IP cameras.
It was written to run on a Raspberry Pi driving an HDMI monitor.

I couldn't find anything to do what I wanted, so I wrote it myself.

The code is ugly. I didn't know python when I started, but pygame looked
like it had (almost) everything I needed, so I ran with it. This is the result.

When the program runs directly from the console (without X), it needs to
be run as root. Running under X requires no special permissions, though you
will need at least read access to /etc/weid/ (and any files in there).
