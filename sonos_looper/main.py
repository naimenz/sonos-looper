from soco import discover, SoCo
import time
import fire
from typing import Optional

from sonos_looper.server import HttpServer, make_server

def main(path: str, ip: Optional[str] = None, port: Optional[int] = None, load_time: int = 15) -> None:
    """Play a local audio file on repeat on the Sonos speaker.

    Requires setting up a local HTTP server to serve the file.

    Args:
        sonos: The Sonos speaker 'zone' to play the audio on.
        path: The path to the song to play.
        ip: The IP address of the server to serve the audio file. By default tries
            to infer the IP address of the local machine.
        port: The port of the server to serve the audio file. By default a random port
            between 8000 and 9000 is chosen.
        load_time: The time to wait for the audio to be sent from the server to
            the speaker before closing the server.
    """
    server = make_server(ip, port)
    print(f"Server will run at {server.base_url}")
    sonos = get_sonos()
    loop_local_audio(sonos, path, server)

def cli() -> None:
    fire.Fire(main)

def get_sonos() -> SoCo:
    sonoses: list[SoCo] = list(discover())  # type: ignore
    if len(sonoses) == 0:
        raise ValueError("No Sonos zones found")
    sonos = sonoses[0]
    if len(sonoses) >= 1:
        print(
            "Warning: More than one Sonos zone found."
            f" Using the first one ({sonos.player_name})."
        )
    return sonos


def loop_local_audio(
    sonos: SoCo,
    path: str,
    server: HttpServer,
    load_time: int = 15,
) -> None:
    """Play a local audio file on repeat on the Sonos speaker.

    Requires setting up a local HTTP server to serve the file.

    Args:
        sonos: The Sonos speaker 'zone' to play the audio on.
        path: The path to the song to play.
        server: The HTTP server to serve the audio file.
        load_time: The time to wait for the audio to be sent from the server to
            the speaker before closing the server.
    """
    server.start()
    uri = f"{server.base_url}/{path}"
    loop_audio(sonos, uri)
    time.sleep(load_time)
    server.stop()

def loop_audio(sonos: SoCo, uri: str) -> None:
    """Play an audio file on repeat on the Sonos speaker.

    Args:
        sonos: The Sonos speaker 'zone' to play the song on.
        uri (str): The URI of the song to play.
    """
    sonos.clear_queue()
    sonos.add_uri_to_queue(uri)
    sonos.play_mode = "REPEAT_ALL"
    sonos.play_from_queue(0)