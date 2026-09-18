#sizing of a Bogie side frame according to the EN 13749 norm
#the bogie side frame is represented as a sipmly supported beam
#the model does not reproduce all load case required by EN 13749

import numpy as np
import matplotlib.pyplot as plt 

# entry parameters
L = 2.6 
m1 = 20000.0 #vehicle mass
g = 9.81
kv = 1.4 #according to EN 13749

#steel S355 properties 
Re = 355.0
safety_factor = 1.5 
sigma_adm = Re / safety_factor
sigma_limit_weld = 140.0 #safety factor with the help of EN 15085
#used for preliminary comparison 
rho_steel = 7850.0 

#exterior dimensions from side frame 
H = 0.250
B = 0.180

#static and dynamic calculations
F_th = (m1 * g ) / 2.0 
F = kv * F_th 
R_1 = F / 2.0
R_2 = F / 2.0
# Simplified beam model - not a complete EN 13749 load case

x = np.linspace(0, L, 500)
T = np.where(x < L/2, R_1 / 1e3, (R_1 - F) / 1e3)
Mf = np.where(x < L/2, R_1 * x, R_1 * x - F * (x - L/2)) 
Mf_max = np.max(Mf)
print(f"strenght of materials results")
print(f"dynamic load F : {F/1e3:.2f} kN")
print(f"maximum bending moment Mf_max : {Mf_max/1e3:.2f} kN.m")

#parametric sweep 
t_values_mm = np.linspace(6, 16, 100)
sigma_max_values = []
linear_mass_values = []
for t_mm in t_values_mm:
    t = t_mm / 1e3
    b = B - 2 * t
    h = H - 2 * t 
   
    #quadratic moment I in m^4
    I = (B * H**3 - b * h**3) / 12 

    #elastic bending module 
    wel = I / (H / 2.0)
    
    #maximal stress in MPa 
    sigma = (Mf_max / wel) / 1e6
    sigma_max_values.append(sigma)

    #linear mass : ideal selection
    area = (B * H ) - (b * h)
    linear_mass = area * rho_steel
    linear_mass_values.append(linear_mass)

sigma_max_values = np.array(sigma_max_values)
linear_mass_values = np.array(linear_mass_values)

#creation of reports figures
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

#first figure : graphic strenght of materials
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
ax1.plot(x, T, color='tab:blue', lw=2)
ax1.fill_between(x, T, color='tab:blue', alpha=0.15)
ax1.set_ylabel("shear force $T_y$ (kN)", fontsize=11)
ax1.set_title(f"Sollicitations from side frame (Lenght L = {L} m, $F$ = {F/1e3:.1f} kN)", fontsize=12, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.6)

ax2.plot(x, Mf / 1e3, color='tab:red', lw=2)
ax2.fill_between(x, Mf / 1e3, color='tab:red', alpha=0.15)
ax2.set_xlabel("Position on side frame $x$ (m)", fontsize=11)
ax2.set_ylabel("Bending moment $M_{fz}$ (kN·m)", fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("graphics_som.png", dpi=300)
plt.show()

# 2nd figure : sizing and choices for mass and stress
fig, ax = plt.subplots(figsize=(8, 5))
color = 'tab:red'
ax.set_xlabel("steels plate thickness $t$ (mm)", fontsize=11)
ax.set_ylabel(r"maximal stress $\sigma_{\max}$ (MPa)", color=color, fontsize=11)
line1 = ax.plot(t_values_mm, sigma_max_values, color=color, lw=2.5, label=r"$\sigma_{\max}(t)$")
ax.tick_params(axis='y', labelcolor=color)

#criteria lines
ax.axhline(sigma_adm, color='darkred', linestyle='--', alpha=0.7, label=r"static limit adm. $[\sigma] = 236.7$ MPa")
ax.axhline(sigma_limit_weld, color='orange', linestyle=':', lw=2, label=r"maximal material fatigue $\approx 140$ MPa")
#other axle for 2nd mass
ax_mass = ax.twinx()
color_mass = 'tab:gray'
ax_mass.set_ylabel("Linear mass for structural steel (kg/m)", color=color_mass, fontsize=11)
line2 = ax_mass.plot(t_values_mm, linear_mass_values, color=color_mass, lw=1.8, linestyle='-.', label="linear mass (kg/m)")
ax_mass.tick_params(axis='y', labelcolor=color_mass)


plt.title("cross section design criteria (EN 13749 / S355)", fontsize=12, fontweight='bold')
fig.tight_layout()
plt.savefig("sizing_study.png", dpi=300)
plt.show()