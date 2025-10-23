# with open("futurocsv.txt") as csv:
#     linhas = csv.readlines()
#     linhas_modificadas = []
#     for linha in linhas:
#         linha_limpa = linha.strip()
#         if '\t' in linha_limpa:
#             linha_modificada = linha_limpa.replace('\t','\n',1)
#             linhas_modificadas.append(linha_modificada)
#         else:
#             linhas_modificadas.append(linha)
# with open("futurocsv2.txt",'w') as csv_out:
#     csv_out.writelines(linhas_modificadas)

import argparse
import numpy as np
from pathlib import Path
import os
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def print_styled_dataframe(df, filename, n):
    print(f"\n DataFrame from {filename}:")
    print(tabulate(df.head(n), headers='keys', tablefmt='fancy_grid', showindex=False))
    
    
parser = argparse.ArgumentParser(description=".")
parser.add_argument("-i","--input", nargs="+", required=False, help="Process CSV")
parser.add_argument("-o", "--output", default=None, help="Saving CSV")
parser.add_argument("--save-csv", action="store_true", help="Only saving CSV")
parser.add_argument("--print-df", action="store_true", help="Print df")
parser.add_argument("--load-csv", type=str, help="Load CSV")
parser.add_argument("--run-func", type=str, choices=["print", "describe", "head"], help="Function to run on the loaded DataFrame")
parser.add_argument("--head", type=int, default=5, help="Rows to print from each DataFrame")

args = parser.parse_args()
txt_files = args.input
output_files = args.output
csv_files = args.load_csv

def run_function(df, func_name, head_rows=5):
    if func_name == "print":
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    elif func_name == "head":
        print(tabulate(df.head(head_rows), headers="keys", tablefmt="fancy_grid", showindex=False))
    elif func_name == "describe":
        print(tabulate(df.describe(), headers="keys", tablefmt="fancy_grid"))
        
def criar_dataframe_de_txt(txt_files):
    dataframes = {}
    for filename in txt_files:
        try:
            df = pd.read_csv(
            filename, 
            sep='\s+', 
            skiprows=1, 
            names=['position_cm', 'force_N']
            )
            print(f"Dataframe is successfully created from: {filename}")
            dataframes[filename] = df
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return None
        except Exception as e:
            print(f"There was an error reading the file: {e}")
            return None
    return dataframes
    
dd=criar_dataframe_de_txt(txt_files)

def salvar_dataframe_csv(dataframes, output_dir="convertidos"):
    os.makedirs(output_dir, exist_ok=True)
    for name, df in dataframes.items():
        base = os.path.splitext(os.path.basename(name))[0]
        out_path = os.path.join(output_dir,f"{base}_convertido.csv")
        try:
            df.to_csv(out_path, index=False)
            print(f"Dataframe is successfully created from: {df} -> {out_path}")
        except Exception as e:
            print(f"{e}")
            
def load_csv(csv_files):
    dataframes = {}
    force_data = {}
    position_data = {}
    for filename in csv_files:
        df = pd.read_csv(filename)
        x_cm = df["position_cm"].values
        F_N = df["force_N"].values
        x_m = x_cm / 100  # convert to meters
        dataframes[filename] = df
        force_data[filename] = F_N
        position_data[filename] = x_m
    return dataframes, force_data, position_data

if args.input:
    dfs,_,_ = load_csv(args.input)
    if args.print_df:
        for name, df in dfs.items():
            print_styled_dataframe(df, name, args.head)
    if args.save_csv:
        salvar_dataframe_csv(dfs, args.output or "convertidos")

if args.print_df:
    for name, df in dd.items():
        print_styled_dataframe(df, name,args.head)

if args.save_csv:
    salvar_dataframe_csv(dd)
    
if args.load_csv:
    dfs, _, _ = load_csv([args.load_csv])  # wrap in list
    df = dfs.get(args.load_csv)
    if df is not None and args.run_func:
        run_function(df, args.run_func, args.head)


mass = 0.412 # Kg

def wave_model(x, A, k, phi, C):
    return A * np.sin(k * x + phi) + C



    # # Fit sinusoidal model
    # params, _ = curve_fit(wave_model, x_m, F_N)
    # A, k, phi, C = params
    # k_eff = abs(A * k)
    # omega = np.sqrt(k_eff / mass)
    # f = omega / (2 * np.pi)
    # T = 2 * np.pi / omega
    # delta_U = 0.5 * k_eff * A**2
    # F_max = A