# Import Math library (for trigonometry) and Matplotlib for plotting
import math
import matplotlib.pyplot as plt


# Fix the constants

m = 2100 # Massa [kg]
Fxf = 1000 # Fx eixo frontal
Fxr = 1000 # Fx eixo traseiro
rho = 1.23 # Densidade do ar
Cx = 0.45 # Coeficiente de arrasto do carro
Af = 2 # Area frontal do carro
hp = 1 # Altura do centro de pressao aerodinamica
hcg = 1 # Altura do centro de gravidade
incl = 0 # Inclinaçao percentual da rampa
theta = math.atan(incl/100) # Angulaçao da rampa
g = 9.81 # Gravidade
l1 = 1 # Distancia do eixo dianteiro em ralaçao ao Cg
l2 = 2.1 # Distancia do eixo traseiro em ralaçao ao Cg
ff = 0.5 # Fator de atrito das rodas dianteiras
fr = 0.5 # Fator de atrito das rodas traseiras

# Calculate the three constant therms
a = (
    (rho*Cx*Af*hp*ff + Af*hp*fr)/(2*l1+l2) -
    (rho*Af*Cx)/2
    )
b = (
    Fxf +
    ff * (m*g*hcg*math.sin(theta) - m*g*l2*math.cos(theta))/(l1+l2) +
    Fxr -
    (m*g*math.sin(theta)) +
    fr * (m*g*hcg*math.sin(theta) + m*g*l2*math.cos(theta))/(l1+l2)
    )
c = (
    m -
    m*hcg * ((ff+fr)/(l1+l2))
    )

# Print a, b and c so we can know if they have ok values
print('a: ' + str(a))
print('b: ' + str(b))
print('c: ' + str(c))

def delta_v(a, b, c, v, dt):
    # Divide the increment in time "dt" by 1000 to transform from milliseconds to seconds
    dt = dt/1000
    # Calculate the increment in velocity "dv" as a function of the previous velocity and the increment in time
    dv = ((v**2*a+b)/c)*dt
    return dv

# Create vectors (Python's "list") to store the values of time and velocity
time = []
vel = []
acel = []

# Initialize variables for (previous and current) velocity and for time increment
old_v = 0
new_v = 0
dt = 1 # milliseconds

# Time and Velocity increment Loop
# Increment the time in steps of 1 millisecond
for t_inst in range(0, 500000, dt):
    # Increment in time is calculated by the delta_v function
    dv = delta_v(a, b, c, old_v, dt)
    # Current velocity equals the previous velocity plus the numerical velocity increment in time
    new_v = old_v + dv
    # Updates previous velocity value with the new velocity value, so it can be incremented on the next iteration
    old_v = new_v
    # Append (include) time and velocity values on their lists (vectors)
    time.append(t_inst/1000)
    vel.append(new_v*3.6)
    acel.append(dv/dt)

# Create Time x Velocity plot
plt.subplot(211)
plt.plot(time, vel)
plt.title('Velocidade')
plt.grid(True)

# Create Time x Velocity plot
plt.subplot(212)
plt.plot(time, acel)
plt.title('Aceleraçao')
plt.grid(True)

# Show plots
plt.show()