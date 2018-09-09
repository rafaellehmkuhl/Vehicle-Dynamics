# Import Math library (for trigonometry) and Matplotlib for plotting
import math
import matplotlib.pyplot as plt
import pandas as pd

# Fix the constants

m = 2100 # Massa [kg]
Fxf = 0 # Fx eixo frontal
Fxr = 5800 # Fx eixo traseiro
rho = 1.23 # Densidade do ar
Cx = 0.45 # Coeficiente de arrasto do carro
Af = 2 # Area frontal do carro
hp = 1 # Altura do centro de pressao aerodinamica
hcg = 1 # Altura do centro de gravidade
incl = 0 # Inclinaçao percentual da rampa
g = 9.81 # Gravidade
l1 = 1 # Distancia do eixo dianteiro em ralaçao ao Cg
l2 = 2.1 # Distancia do eixo traseiro em ralaçao ao Cg
ff = 0.04 # Fator de atrito das rodas dianteiras
fr = 0.04 # Fator de atrito das rodas traseiras

def calculate_abc(incl):
    # Calculate inclination angle
    theta = math.atan(incl/100)

    # Calculate the three constant therms
    a = (
        + (ff+fr) * (rho*Cx*Af*hp) / (2*(l1+l2))
        - (rho*Af*Cx) / 2
        )
    b = (
        + Fxf
        + ff * (m*g*hcg*math.sin(theta) - m*g*l1*math.cos(theta)) / (l1+l2)
        + Fxr
        + fr * (m*g*hcg*math.sin(theta) + m*g*l2*math.cos(theta)) / (l1+l2)
        - m*g*math.sin(theta)
        )
    c = (
        + m
        - m*hcg * (ff+fr) / (l1+l2)
        )
    return a, b, c

def delta_v(a, b, c, v, dt):
        # Calculate the increment in velocity "dv" as a function of the previous velocity and the increment in time
        dv = ((v**2*a+b)/c)*dt
        return dv

def get_velocity_curve(a, b, c):
    # Create vectors (Python's "list") to store the values of time and velocity
    time = []
    vel = []
    accel = []

    # Initialize variables for (previous and current) velocity and for time increment
    old_v = 0
    dt = 0.001 # seconds
    t_inst = 0 # Instantaneous time for the loop, in seconds

    _accel = 1 # Acceleration [m/s^2]
    _vel = 0

    # Time and Velocity increment Loop
    # Increment the time in steps of 1 millisecond
    while _accel > 0.001:
        # Increment time
        t_inst = t_inst + dt
        # Increment in time is calculated by the delta_v function
        dv = delta_v(a, b, c, old_v, dt)
        # Current velocity equals the previous velocity plus the numerical velocity increment in time
        _vel = old_v + dv
        # Updates acceleration value
        _accel = dv/dt
        # Updates previous velocity value with the new velocity value, so it can be incremented on the next iteration
        old_v = _vel
        # Append (include) time and velocity values on their lists (vectors)
        time.append(t_inst)
        vel.append(_vel*3.6)
        accel.append(dv/dt)

    return time, vel, accel

tva_df = []
for incl in range(0, 31, 3):

    # Calculate constants 'a', 'b' and 'c' for given inclination
    a, b, c = calculate_abc(incl)
    # Get Time_Velocity curve for given constants
    time, vel, accel = get_velocity_curve(a, b, c)
    # Create Time x Velocity plot
    plt.plot(time, vel, label=str(incl) + '%')
    # Create and append DataFrame
    df = pd.DataFrame({
            'Tempo': time,
            'Velocidade': vel,
            'Aceleraçao': accel
        })
    df.set_index('Tempo', inplace=True)
    tva_df.append(df)

# Show plots
plt.title('Velocidade x Tempo')
plt.xlabel('Tempo [s]')
plt.ylabel('Velocidade [km/h]')
plt.grid(True)
plt.legend(title='Inclinaçao')
plt.show()

# for incl in range(0, 31):
#     try:
#         # Print time for 0-100km/h
#         time100 = tva_df[incl][tva_df[incl]['Velocidade'].gt(100)].index[0]
#         print('Time for 0-100km/h: ' + str(time100))
#     except:
#         pass