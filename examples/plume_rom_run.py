from src.data_loader import load_snapshots
from src.lifters import EulerLifter
from src.transformers import get_combustion_transformer
from src.rom_builder import train_rom
from src.config import *
import numpy as np
import matplotlib.pyplot as plt
import os


folder = os.path.join("data", "p875")
time = np.linspace(0.005,1,200, endpoint=True)
snapshots = load_snapshots(folder, STATE_VARIABLES)
transformer = get_combustion_transformer()
lifter = EulerLifter()
rom = train_rom(snapshots[:,0:100], time[0:100], transformer, lifter)

# Predict
q0 = rom.basis.compress(transformer.fit_transform(lifter.lift(snapshots[:,0:100])))[:, 0]
t_eval = np.linspace(time[0],.5,200, endpoint=True)
Q_ROM = rom.model.predict(q0, t_eval, method="BDF", first_step=1e-20, 
                           rtol=1e-6, atol=1e-8, max_step=1e-3)
q_rom = rom.lifter.unlift(rom.transformer.inverse_transform(rom.basis.decompress(Q_ROM)))

# Plot one variable (e.g., temperature)
vx_rom, vy_rom, T_rom, Ts_rom, rhop_rom, Y_CH4_rom, Y_O2_rom, Y_H2O_rom, Y_CO2_rom,\
      Y_CO_rom, Y_N2_rom,Y_wood_rom, Y_char_rom = np.split(q_rom,NUM_ROMVARS)
vx, vy, T, Ts, rhophi, Y_CH4, Y_O2, Y_H2O, Y_CO2, Y_CO, Y_N2,\
            Y_wood, Y_char = np.split(snapshots[:,0:100],NUM_STATES)

xy = np.arange(0,T.shape[0], 1)
fig, ax = plt.subplots(1,1)
ax.scatter(time[0:100],T[1367,:], label="Snapshot data", linewidth=1, color="darkorange", \
           marker='o',facecolor="none")
ax.plot(time[0:100],T_rom[1367,:], label="ROM state output", linestyle="-",\
         color="black", linewidth=2)
ax.set_xlabel(r"Time [s]", fontsize=12)
ax.legend(loc="lower center", frameon=False)
ax.grid(True)