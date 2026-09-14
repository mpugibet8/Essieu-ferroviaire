import numpy as np
import matplotlib.pyplot as plt 

duration = 10.0
nb_points = 1000

time = np.linspace(0, duration, nb_points)

def calc_klingel(s_kmh, conicity):
    
    """
    Computing the oscillating frequency following the equation
    Args : 
        s_kmh (float)
        conicity (float) 

    Returns : 
        float : frequency in Hz

    """
    #1 constants (SI)
    e = 1.435 #standard gauge
    r0 = 0.460 # radius of the wheel in m

    #converting 
    s_ms = s_kmh / 3.6

    in_sqrt = np.sqrt(conicity / (e*r0))
    f = (s_ms / (2*np.pi))* in_sqrt
    return f


from matplotlib.widgets import Slider

s_0 = 100.0
lambda_0 = 0.2
amplitude_t = 5.0 #in mm

f_0 = calc_klingel(s_0,lambda_0)
y = amplitude_t * np.sin(2*np.pi *f_0*time)

#drawing of the curve

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)
ligne, = ax.plot(time, y, lw=2, color='red')

ax.set_title("Simulation")
ax.set_xlabel("time(s)")
ax.set_ylabel("lateral moove (mm)")
ax.set_ylim(-10, 10)

#add sliders 
ax_speed = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_conicity = plt.axes([0.25, 0.05, 0.65, 0.03])

s_speed = Slider(ax_speed,'speed(kmh)', 10.0, 300.0)
s_conicity = Slider(ax_conicity, 'Conicity ( no unit)', 0.05, 0.35)

#reaction loop 
def update(val):
    s = s_speed.val
    lam = s_conicity.val

    newfrequency = calc_klingel(s, lam)
    newy = amplitude_t* np.sin(2 * np.pi * newfrequency *time)

    ligne.set_ydata(newy)
    fig.canvas.draw_idle()
   
s_speed.on_changed(update)
s_conicity.on_changed(update)

plt.show()
