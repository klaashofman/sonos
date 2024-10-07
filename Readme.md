# Summary

Collection of python scripts used to control Sonos Speakers

## favourits
This script is a simple curses based menu to play Sonos favourites
It uses the soco library to interact with the Sonos speaker

The script displays a list of Sonos favourites and allows the user to select one to play.
The user can also adjust the volume, mute the speaker, pause/play the music

## Installation

Create a virtual environment:

``` virtualenv .venv```

Install required pip packages:

``` pip install -r requirements.txt ```

Edit favourites.py and replace wih your local speaker name:

``` SONOS_SPEAKER_NAME = 'Rimshot HQ' ```

Run the script:

``` python3 src/favourites.py ```
