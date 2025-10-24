import typer
import pandas as pd
#from typing import List, Optional
from pathlib import Path
from tqdm import tqdm
import time

app = typer.Typer()
load_app = typer.Typer()
app.add_typer(load_app, name="load")



@load_app.command("txt")

def load_txt(files: list[str]) -> dict[str, pd.DataFrame] | None:
    dataframes : dict[str, pd.DataFrame] = {} 
    for filename in tqdm(files, desc="Loading txt files", unit="file"):
        ext = Path(filename).suffix.lower()
        if ext != ".txt":
            typer.echo(f"Skipping {filename}")
            continue
        try:
            df = pd.read_csv(filename, sep='\s+', skiprows=1, names=['position_cm', 'force_N'])
            dataframes[filename] = df        
            typer.echo(f"Loaded {filename}")
        except Exception as e:
            typer.echo(f"Error loading {filename}: {e}")
        time.sleep(0.3)
    typer.echo(f"Loaded {len(dataframes)} txt file(s)")
    return dataframes if dataframes else None

@load_app.command("csv")

def load_csv(files: list[str]) -> dict[str, pd.DataFrame] | None:
    dataframes : dict[str, pd.DataFrame] = {}
    for filename in tqdm(files, desc="Loading csv files",unit="file"):
        ext = Path(filename).suffix.lower()
        if ext != ".csv":
            typer.echo(f"Skipping {filename}")
            continue
        try:        
            df = pd.read_csv(filename)
            dataframes[filename] = df
            typer.echo(f"Loaded {filename}")
        except Exception as e:
            typer.echo(f"Error loading {filename}: {e}")
        time.sleep(0.3)
    typer.echo(f"Loaded {len(dataframes)} txt file(s)")
    return dataframes if dataframes else None


@load_app.command("load_all")

def load_all(files: list[str]) -> dict[str, pd.DataFrame] | None:
    dataframes : dict[str, pd.DataFrame] = {}
    for filename in tqdm(files,desc="Loading txt and csv",unit="file"):
       try: 
           ext = Path(filename).suffix.lower()
           if ext == ".txt": 
               df = pd.read_csv(filename, sep='\s+', skiprows=1, names=['position_cm', 'force_N'])
           elif ext == ".csv":
               df = pd.read_csv(filename)
           else:
               typer.echo(f"Ficheiro não suportado {filename}")
               continue
           dataframes[filename] = df
           typer.echo(f"Loaded {filename}")
       except Exception as e:
            typer.echo(f"There was an error reading the file: {e}")
       time.sleep(0.3)
    typer.echo(f"Loaded {len(dataframes)} {ext} file(s)")
    return dataframes if dataframes else None

if __name__ == "__main__":
    app()