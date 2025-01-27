"""
Program to show a water drop hitting the surface
Move the slider based on a timer
Provide buttons to play, pause, and step the slider
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Global constants and variables
pond_radius = 500.0  # Radius of pond (meters)
grid_points = 300
wave_speed = 1  # Speed of wave propagation (m/s)
wave_amplitude = 0.01  # Wave height amplitude
wave_length = 20  # Wavelength (meters)
t_init = 0  # Initial time
time_steps = 200  # Total time (seconds)
mass = 0.001  # Mass of water drop (kg)
g = 9.8  # Acceleration due to gravity (m/s^2)
# drop_position = (0, 0, -1)
# impact_energy = mass * g * 1  # 1 meter drop height

slider_moving = False

# Generate pond grid
x = np.linspace(-pond_radius, pond_radius, grid_points)
y = np.linspace(-pond_radius, pond_radius, grid_points)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X ** 2 + Y ** 2)


def wave_function(t):
    """
    | Wave function
    :param t: simulated time in seconds
    :return: wave value as float
    """

    damping = np.exp(-r / pond_radius)  # Damping factor
    wave = wave_amplitude * np.sin(
        2 * np.pi * (r - wave_speed * t) / wave_length) * damping
    wave[r > pond_radius] = 0  # No waves outside pond
    return wave

# Plot setup
fig = plt.figure(figsize=(8, 5))
plt.subplots_adjust(bottom=0.1)  # Leave room for the slider
ax = fig.add_subplot(111, projection='3d')

# Slider setup
ax_slider = fig.add_axes((0.2, 0.02, 0.6, 0.03))
time_slider = Slider(ax_slider, "Time (s)",
                     valmin=0, valmax=time_steps, valinit=t_init)

# Button setup in a new figure
fig2 = plt.figure(figsize=(4, 1))
fig2.suptitle('\nControl Panel')

ax_button1 = fig2.add_axes((0.05, 0.05, 0.22, 0.25))
ax_button2 = fig2.add_axes((0.3, 0.05, 0.2, 0.25))
ax_button3 = fig2.add_axes((0.55, 0.05, 0.2, 0.25))
ax_button4 = fig2.add_axes((0.75, 0.05, 0.2, 0.25))

button1 = Button(ax_button1, 'NO OP')
def button1_on_clicked(_):
    global slider_moving
    if slider_moving:
        slider_moving = False
    else:
        slider_moving = True
button1.on_clicked(button1_on_clicked)

button2 = Button(ax_button2, 'RESET')
def button2_on_clicked(_):
    time_slider.set_val(0)
button2.on_clicked(button2_on_clicked)

button3 = Button(ax_button3, 'STEP -')
def button3_on_clicked(_):
    if time_slider.val >= 1 and not slider_moving:
        time_slider.set_val(time_slider.val - 1)
button3.on_clicked(button3_on_clicked)

button4 = Button(ax_button4, 'STEP +')
def button4_on_clicked(_):
    if time_slider.val <= 199 and not slider_moving:
        time_slider.set_val(time_slider.val + 1)
button4.on_clicked(button4_on_clicked)


# Update function (event handler for slider changed)
def update(val):
    t = val  # value read from the slider
    Z = wave_function(t)

    ax.clear()
    ax.set_title(f"Wave Propagation from Droplet Impact (Time = "
                 f"{t:.2f} s)")
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Y (meters)")
    ax.set_zlabel("Wave Height (mm)")
    ax.set_zlim(-10, 10)

    ax.plot_surface(X, Y, Z * 1000, cmap="viridis")

time_slider.on_changed(update)

# Move the slider once per second
def move_slider():
    global slider_moving
    slider_moving = True
    for i in np.arange(0, 210, 10):
        time_slider.set_val(float(i))
        plt.pause(1)
    slider_moving = False

# Create the plot at t=0
update(0)

# Call the function to move the slider automatically
# move_slider()

plt.show()
