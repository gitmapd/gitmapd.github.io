import typer
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import time
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.optimize import curve_fit

app = typer.Typer()
load_app = typer.Typer()



app.add_typer(load_app, name="load")





def wave_model(x, A, k, phi, C):
    return A * np.sin(k * x + phi) + C

@app.command("model-wave")
def model_waves(files: list[str],
    fit: bool = typer.Option(False, help="Fit wave model to data"),
    plot: bool = typer.Option(False, help="Plot fitted wave"),
    save: bool = typer.Option(False, help="Plot fitted wave")) -> tuple[dict[str, pd.DataFrame] , dict[str, np.ndarray], dict[str, np.ndarray] ] | None:
    result = load_csv(files)
    if not result:
        typer.echo("No data loaded.")
        raise typer.Exit()
    dataframes, force_data , position_data = result
    fitted_params = {}
        
    if fit:
        for name, df in dataframes.items():
            if "position_cm" not in df.columns or "force_N" not in df.columns:
                typer.echo(f"Missing required columns in {name}")
                continue
            x_m = position_data[name]
            F_N = force_data[name]
            try:
                popt, _ = curve_fit(wave_model, x_m, F_N, p0=[1, 2*np.pi, 0, 0]) 
                A, k, phi, offset = popt
                fitted_params[name] = popt
                print(f"\nWave model for {name}:")
                print(f"Amplitude (A): {A:.4f}")
                print(f"Wave number (k): {k:.4f}")
                print(f"Phase (phi): {phi:.4f}")
                print(f"Offset: {offset:.4f}")
        
                if plot:
                    x_fit = np.linspace(min(x_m), max(x_m), 500)
                    F_fit = wave_model(x_fit, *popt)
                    plt.figure()
                    plt.plot(x_m, F_N, 'o', label='Data')
                    plt.plot(x_fit, F_fit, '-', label='Fitted wave')
                    plt.xlabel("Position (m)")
                    plt.ylabel("Force (N)")
                    plt.title(f"Wave Fit: {name}")
                    plt.legend()
                    plt.grid(True)
                    plt.show()
            except Exception as e:
                typer.echo(f"Fit failed for {name}: {e}")    
    if save and fitted_params:
        df_out = pd.DataFrame.from_dict(fitted_params, orient="index",columns=["A","k","phi","offset"])
        df_out.index.name = f"{name}"
        df_out.to_csv("fitted_parameters.csv")
        typer.echo("Saved fitted parameters to fitted_parameters.csv")

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
    force_data : dict[str, np.ndarray] = {}
    position_data: dict[str, np.ndarray] = {}
    for filename in tqdm(files, desc="Loading csv files",unit="file"):
        ext = Path(filename).suffix.lower()
        if ext != ".csv":
            typer.echo(f"Skipping {filename}")
            continue
        try:        
            df = pd.read_csv(filename)
            if "position_cm" not in df.columns or "force_N" not in df.columns:
               print(f"Missing expected columns in {filename}: found columns {df.columns.tolist()}")
               continue
            x_m = df["position_cm"].to_numpy() / 100
            F_N = df["force_N"].values
            F_N = df["force_N"].to_numpy()
            dataframes[filename] = df
            force_data[filename] = F_N
            position_data[filename] = x_m
            typer.echo(f"Loaded {filename}")
        except Exception as e:
            typer.echo(f"Error loading {filename}: {e}")
        time.sleep(0.3)
    typer.echo(f"Loaded {len(dataframes)} txt file(s)")
    if dataframes:
        return (dataframes, force_data, position_data) if dataframes else None


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
               typer.echo(f"File not supported {filename}")
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