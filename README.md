# autowemote

A Python program to toggle a wemo switch based on what chromecast app is
currently running.

Needs to be rewritten without the pychromecast library since it isn't really
supported and doesn't support newer APIs and we only need to hit one endpoint to
get the info we need.
