from soco import SoCo
from soco import discover
from soco import music_library
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

def display_menu(stdscr, selected_row_idx, items):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    for idx, item in enumerate(items):
        #x = w//2 - len(item)//2
        #y = h//2 - len(items)//2 + idx
        x = 0
        y = idx
        if idx == selected_row_idx:
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(y, x, '< ' + item + ' >')
            stdscr.attroff(curses.A_BOLD)
        else:
            stdscr.addstr(y, x, item)
    
    stdscr.refresh()

def mute_speaker(speaker, mute=False):
    speaker.group.mute = mute

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

    display_menu(stdscr, selected_row_idx, items)

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
        
        display_menu(stdscr, selected_row_idx, items)

curses.wrapper(main)