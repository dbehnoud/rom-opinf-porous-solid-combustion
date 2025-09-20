import numpy as np
import pandas as pd
import os, glob

def load_snapshots():
    columns = ["U:0", "U:1", "T", "Ts", "rhophi", "gas", "O2", "H2O",\
                                "CO2", "CO", "N2", "Ywood",'Ychar']
    csv_files = sorted(glob.glob(os.path.join("data","p875","*.csv")), 
                       key=lambda s: int(s.split('_')[1].split('.')[0]))
    snapshots = []
    for file in csv_files:
        df = pd.read_csv(file)
        df["rhophi"] = df["rho"] * df["porosityF"]
        snapshot = pd.concat([df[c] for c in columns], axis=0)
        snapshots.append(snapshot.to_numpy())
    return np.column_stack(snapshots)


def load_snapshots_uq():
    folders = [entry for entry in glob.glob("data/*") if os.path.isdir(entry)]

    columns = ["U:0", "U:1", "T", "Ts", "rhophi", "gas", "O2", "H2O",\
                                "CO2", "CO", "N2", "Ywood",'Ychar']
    Qs = []
    for folder in folders:
        csv_files = glob.glob(os.path.join(folder, "*.csv"))
        sorted_files = sorted(csv_files, key=lambda s: int(s.split('_')[1].split('.')[0]))
        df = pd.DataFrame()
        for i, file in enumerate(sorted_files):
            #if i >= 100:  
            #    break
            temp = pd.read_csv(file)
            new = (temp["rho"])*temp["porosityF"]
            temp["rhophi"] = new
            concatenated_column = pd.concat([temp[col] for col in columns], 
                                            axis=0, ignore_index=True)
            df = pd.concat([df, concatenated_column], axis=1)
            data = df.to_numpy()
        Qs.append(data)
        return Qs