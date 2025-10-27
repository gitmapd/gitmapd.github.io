import subprocess
import sys
import re
import os
import typer
from typing import Optional
from enum import Enum


class DownloadQuality(str, Enum):
    low = "low"
    medium = "medium"
    best = "best"

app = typer.Typer()

def sanitize_filename(name):
    """Remove illegal characters from filenames."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

@app.command("download")
def download(
    video_url: str = typer.Argument(..., help="The URL of the Twitch video to download."),
    quality: DownloadQuality = typer.Option(DownloadQuality.best, "--quality", "-q", help="Desired video quality."),
    output_path: Optional[str] = typer.Argument(".",help="")
):
    video_id = re.search(r"(?:videos/|clip/|clips\.twitch\.tv/)([\w-]+)", video_url)
    video_id = video_id.group(1) if video_id else "twitch_video"
    output_file = os.path.join(output_path, f"{sanitize_filename(video_id)}.mp4")
    cmd = [
        "streamlink",
        video_url,
        quality,
        "-o",
        output_file
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to download {e}")
        
if __name__ == "__main__":
    app()
# import click
# @click.group()
# def cli():
#     pass

# @cli.command()
# @click.argument("video_url")
# @click.option("--quality", "-q", default="best", type=click.Choice(["low", "medium", "best"]))
# def download(video_url, quality):
#     print(f"URL: {video_url}")
#     print(f"Quality: {quality}")

# if __name__ == "__main__":
#     cli()
# import typer
# from typing import Optional
# from enum import Enum
# print(sys.argv)

# class DownloadQuality(str, Enum):
#     low = "low"
#     medium = "medium"
#     best = "best"

# app = typer.Typer()

# @app.command("download")
# def download_twitch_video(
#     video_url: str = typer.Argument(..., help="The URL of the Twitch video to download."),
#     quality: DownloadQuality = typer.Option("best", "--quality", "-q", help="Desired video quality.")
# ):
#     if quality not in DownloadQuality.__members__:
#         typer.echo(f"Error: Invalid quality '{quality}'. Choose from: low, medium, best.")
#         raise typer.Exit(code=1)

#     typer.echo(f"Downloading {video_url} with quality {quality}")

# if __name__ == "__main__":
#     app()