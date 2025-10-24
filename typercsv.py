import typer
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import time
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.optimize import curve_fit
import logging

app = typer.Typer()
load_app = typer.Typer()
app.add_typer(load_app, name="load")

log_path = Path("load_txt.log")

logging.basicConfig(
        filename=log_path,
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )



def wave_model(x, A, k, phi, C):
    return A * np.sin(k * x + phi) + C

@app.command("model-wave")
def model_waves(files: list[str],
    fit: bool = typer.Option(False, help="Fit wave model to data"),
    plot: bool = typer.Option(False, help="Plot fitted wave"),
    save: bool = typer.Option(False, help="Save plot"),
    latex: bool = typer.Option(False, help="Save plot"),
    compile: bool = typer.Option(False, help="Compile LaTeX report to PDF")) -> tuple[dict[str, pd.DataFrame] , dict[str, np.ndarray], dict[str, np.ndarray] ] | None:
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
                    plot_path = f"wave_fit_{Path(name).stem}.pdf"
                    if save:
                        plt.savefig(plot_path)
                    else:
                        plt.show()
                    plt.close()
            except Exception as e:
                typer.echo(f"Fit failed for {name}: {e}")
        df_out = pd.DataFrame.from_dict(
        fitted_params, orient="index", columns=["A", "k", "phi", "offset"])
        df_out.index.name = "filename"
        latex_table = df_out.to_latex(index=True, float_format="%.4f")   
    if save and fitted_params:
        df_out.to_csv("fitted_parameters.csv")
        typer.echo("Saved fitted parameters to fitted_parameters.csv")
    if latex and not fit:
        typer.echo("Use --fit with --latex.")
    elif latex and fitted_params:
        with open("wave_report.tex", "w") as f:
            f.write(r"\documentclass{article}" + "\n")
            f.write(r"\usepackage{graphicx}" + "\n")
            f.write(r"\usepackage{amsmath}" + "\n")
            f.write(r"\usepackage{booktabs}"+ "\n")
            f.write(r"\begin{document}" + "\n")
            f.write(r"\section*{Wave Modeling Report}" + "\n")
            f.write(latex_table + "\n")
            for name in fitted_params:
                fig_name = f"wave_fit_{Path(name).stem}.pdf"
                f.write(r"\begin{figure}[h!]\centering" + "\n")
                f.write(fr"\includegraphics[width=0.8\textwidth]{{{fig_name}}}" + "\n")
                f.write(fr"\caption{{Wave fit for {Path(name).stem}}}" + "\n")
                f.write(r"\end{figure}" + "\n")
            f.write(r"\end{document}" + "\n")
            typer.echo("LaTeX report saved as wave_report.tex")
            if compile:
                import subprocess
                try:
                    subprocess.run(["pdflatex","wave_report.tex"],check=True)
                    typer.echo(f"Compiled wave_report.pdf")
                except Exception as e:
                    typer.echo(f"pdflatex failed {e}")
    
@load_app.command("txt")

def load_txt(files: list[str],
             save: bool = typer.Option(False, help="Save to csv")) -> dict[str, pd.DataFrame] | None:
    dataframes : dict[str, pd.DataFrame] = {} 
    with tqdm(total=len(files), desc="Loading txt files", unit="file") as pbar:
        for filename in files:
            start_time = time.time()
            ext = Path(filename).suffix.lower()
            stem = Path(filename).stem
            
            logging.info(f"Processing {stem}") 
            
            if ext != ".txt":
                logging.info(f"Skipping {stem}")
                pbar.update(1)
                continue
            try:
                df = pd.read_csv(filename, sep='\s+', skiprows=1, names=['position_cm', 'force_N'])
                logging.info(f"Loaded {filename}")
                if save:
                    df.to_csv(f"{filename}_converted.csv")
                    logging.info(f"Saved {stem}_converted.csv")
                else:
                    logging.info(f"Couldnt save {stem}_converted.csv")
                    continue
                dataframes[filename] = df        
            except Exception as e:
                logging.info(f"Error loading {filename}: {e}")
            elapsed = time.time() - start_time
            logging.info(f"Finished {filename} in {elapsed:.2f}s")
            pbar.update(1)
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