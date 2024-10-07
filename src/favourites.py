#!python3
# -*- coding: utf-8 -*-
from soco import discover
import curses

# TODO: move this to a config file
SONOS_SPEAKER_NAME = 'Rimshot HQ'

def find_speaker(speaker_name):
    # sometimes the spaeker is not found on the first try
    for i in range(0, 100):
        zone_list = list(discover())
        for zone in zone_list:
            if (zone.player_name == speaker_name):
                return zone
    return None

def display_menu(stdscr, selected_row_idx, items, speaker):
    stdscr.clear()
    stdscr.addstr(0,0,"Sonos Favorites:")
    y = 2

    h, w = stdscr.getmaxyx()

    for idx, item in enumerate(items):
        y = idx + 2
        x = 0
        if idx == selected_row_idx:
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(y, x, '< ' + item + ' >')
            stdscr.attroff(curses.A_BOLD)
        else:
            stdscr.addstr(y, x, item)

    # put the status bar below the channel list
    y,x = stdscr.getmaxyx()
    y -= 2
    stdscr.attron(curses.A_ITALIC | curses.A_BOLD)
    status = f"{speaker.get_current_transport_info()['current_transport_state']}"
    status += f" - Volume: {speaker.group.volume}"
    stdscr.addstr(y, 0, status)
    stdscr.attroff(curses.A_ITALIC | curses.A_BOLD)

    # add a blinking message, above the status if the speaker is muted
    if (is_speaker_muted(speaker)):
        y -= 1
        stdscr.attron(curses.A_BLINK | curses.A_BOLD)
        stdscr.addstr(y, 0, "-- MUTED --")
        stdscr.attroff(curses.A_BLINK | curses.A_BOLD)

    stdscr.refresh()

def mute_speaker(speaker, mute=False):
    speaker.group.mute = mute

def is_speaker_muted(speaker):
    return speaker.group.mute

def volume_speaker(speaker, volume):
    speaker.group.volume = volume

def play_radio_station(speaker, uri):
    try:
        speaker.clear_queue()
        speaker.add_uri_to_queue(uri=uri)
        speaker.play_from_queue(0)
        mute_speaker(speaker, False)
    except Exception as e:
        print(f"Error: {e}")

def main(stdscr):
    speaker = find_speaker(SONOS_SPEAKER_NAME)
    if speaker is None:
        print(f"Speaker {SONOS_SPEAKER_NAME} not found")
        exit(1)

    # get the favouurite radio stations
    search_results = speaker.music_library.get_sonos_favorites()
    if search_results.number_returned == 0:
        print("No favourites found")
        exit(0)

    # obtain the list of radio stations
    radio_stations = search_results._metadata['item_list']
    for station in radio_stations:
        print(f"{station.favorite_nr} - {station.title}")

    items = [station.title for station in radio_stations]
    selected_row_idx = 0

    display_menu(stdscr, selected_row_idx, items, speaker)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row_idx > 0:
            selected_row_idx -= 1
        elif key == curses.KEY_DOWN and selected_row_idx < len(items) - 1:
            selected_row_idx += 1
        # play the selected radio station
        elif key == ord('\n'):
            uri = radio_stations[selected_row_idx].get_uri()
            play_radio_station(speaker, uri)
        elif key == ord('+'):
            volume_speaker(speaker, speaker.group.volume + 1)
        elif key == ord('-'):
            volume_speaker(speaker, speaker.group.volume - 1)
        # toggle mute
        elif (key == ord('m') or key == ord('M')):
            mute = False if is_speaker_muted(speaker) else True
            mute_speaker(speaker, mute)
        # toggle pause/play
        elif key == ord('p') or key == ord('P'):
            if speaker.get_current_transport_info()['current_transport_state'] == 'PLAYING':
                speaker.pause()
            else:
                speaker.play()
        display_menu(stdscr, selected_row_idx, items, speaker)

curses.wrapper(main)
