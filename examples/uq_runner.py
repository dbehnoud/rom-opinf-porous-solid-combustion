from src.data_loader import load_snapshots_uq
from src.pre_processing import EulerLifter
from src.pre_processing import get_combustion_transformer
from src.rom_builder import train_param_rom
from src.config import *
import numpy as np
import matplotlib.pyplot as plt


time = np.linspace(0.005,0.5,100, endpoint=True)
Qs = load_snapshots_uq()
data_eval = Qs[:,0:100]
data_eval= [x[:,::2] for x in data_eval]
transformer = get_combustion_transformer()
lifter = EulerLifter()


#define parameters
porosity = np.array([0.825, 0.828, 0.831, 0.834, 0.837, 0.840, 0.843, \
                     0.846, 0.85, 0.856, 0.862, 0.868, 0.875])
dp = 0.0025/20
permiability = ((1.0-(1.0-porosity[:])**(1/3))**3)*\
    (1.0+(1.0-porosity[:])**(1.0/3))/(11.4*(1.0-porosity[:]))*dp**2
training_parameters = [np.ones(1)*1/x for x in permiability]
max= 1e5
training_parameters = [x/max for x in training_parameters]


def run_monte_carlo(rom_models, params, t_eval, num_samples = 150):

    def model(x):
        if (x<=params[0]) & (x>=params[8]):
            # i = find_nearest_index(params, x)
            i = 4
            q0_ = rom_models[0].basis.compress(transformer.fit_transform(lifter.lift(data_eval[i])))[:,0]
            Q_ROM_ = rom_models[0].model.predict(x, q0_, t_eval, method="BDF", first_step=1e-20, 
                                rtol=1e-6, atol=1e-8, max_step=1e-4)
            q_rom = rom_models[0].lifter.unlift(rom_models[0].transformer.inverse_transform(
                rom_models[0].basis.decompress(Q_ROM_)))
            q_rom = q_rom.astype(np.float32)
            return q_rom
        
        if (x<params[8]) & (x>=params[12]): 
            # i = find_nearest_index(params, x)
            i = 10
            q0_ = rom_models[1].basis.compress(transformer.fit_transform(EulerLifter().lift(data_eval[i])))[:,0]   
            Q_ROM_ = rom_models[1].model.predict(x, q0_, t_eval, method="BDF", first_step=1e-20, 
                                rtol=1e-6, atol=1e-8, max_step=1e-4)
            q_rom = rom_models[1].lifter.unlift(rom_models[1].transformer.inverse_transform(
                rom_models[1].basis.decompress(Q_ROM_)))
            q_rom = q_rom.astype(np.float32)
            return q_rom

    x_min = params[-1]            # Minimum value of input
    x_max = params[0]            # Maximum value of input

    # Compute mean and standard deviation assuming the range represents ~99.7% of values (±3σ)
    mean = (x_min + x_max) / 2
    std_dev = (x_max - x_min) / 6  # Since ~99.7% of data in a normal distribution lies within ±3σ

    # Generate Monte Carlo samples from a normal distribution
    samples = np.random.normal(loc=mean, scale=std_dev, size=num_samples)

    # Ensure samples stay within [x_min, x_max] by clipping them
    samples = np.clip(samples, x_min, x_max)

    # Evaluate the model for each sample
    return [model(np.array([x])) for x in samples]


# build parametric rom models
rom_models = [
train_param_rom(data_eval, [training_parameters[x] for x in [0,8]], \
             time[::2], transformer, lifter),
train_param_rom(data_eval, [training_parameters[x] for x in [8,12]], \
             time[::2], transformer, lifter),
]

# run Monte Carlo simulation
results = run_monte_carlo(rom_models, training_parameters, time)


# plot results for a point at grid with index 1367 (mid-interface)

split_results = [tuple(np.split(q_rom, NUM_STATES)) for q_rom in results]

# vx_romm = []; vy_romm= []; T_romm=[]; Ts_romm=[]; rho_romm=[]; Y_CH4_romm=[]; Y_O2_romm=[]
# Y_H2O_romm=[]; Y_CO2_romm=[]; Y_CO_romm=[]; Y_N2_romm=[]; Y_wood_romm=[]


# for split in split_results:
#     vx, vy, T, Ts, rho, Y_CH4, Y_O2, \
#     Y_H2O, Y_CO2, Y_CO, Y_N2, Y_wood = split 

#     vx_romm.append(vx); vy_romm.append(vy); T_romm.append(T); Ts_romm.append(Ts)
#     rho_romm.append(rho); Y_CH4_romm.append(Y_CH4); Y_CO_romm.append(Y_CO) 
#     Y_CO2_romm.append(Y_CO2); Y_O2_romm.append(Y_O2); Y_H2O_romm.append(Y_H2O) 
#     Y_N2_romm.append(Y_N2);  Y_wood_romm.append(Y_wood)

vy_romm, T_romm, Ts_romm, rho_romm, Y_CH4_romm, Y_O2_romm, \
Y_H2O_romm, Y_CO2_romm, Y_CO_romm, Y_N2_romm, Y_wood_romm = map(list, zip(*split_results))

T_rom1 = np.stack(T_romm, axis=0)
mean_result = np.mean(T_rom1, axis=0)
std_result = np.std(T_rom1, axis=0)
conf_interval = np.percentile(T_rom1, [2.5, 97.5], axis=0)  

fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
x = time
y = mean_result[1367,:]
ci_upper = conf_interval[1,1367,:]
ci_lower = conf_interval[0,1367,:]
ax.plot(x, y, label="Mean Prediction", color="black")
ax.fill_between(x, ci_lower, ci_upper, color='black', alpha=0.2, \
                label="Confidence Interval", edgecolor="none")
ax.set_xlabel("Time [s]", fontsize=12)
ax.set_ylabel("Temperature [K]", fontsize=12)
ax.set_ylim(380, 510)
ax.set_xlim(0.02, 0.5)
ax.grid(True)

    