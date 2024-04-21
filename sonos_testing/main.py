from pathlib import Path
from soco import discover

from sonos_testing.server import HttpServer

if __name__ == '__main__':
    sonos = list(discover())[0]
    # sonos = SoCo('192.168.1.102') # Pass in the IP of your Sonos speaker
    # You could use the discover function instead, if you don't know the IP

    # Pass in a URI to a media file to have it streamed through the Sonos
    # speaker
    server = HttpServer(8000)
    server.run()

    test_path = "data/test.wav"
    local_uri = Path("http://localhost:8000") / test_path
    number_in_queue = sonos.add_uri_to_queue(local_uri)

    # sonos.play_uri(
    #     # 'http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3')

    #     "blob:https://noises.online/2eb31f52-89c2-412c-be5c-6298ea141fa6"
    # )
    sonos.play_from_queue()

    track = sonos.get_current_track_info()

    print(track['title'])

    sonos.pause()

    # Play a stopped or paused track
    sonos.play()
