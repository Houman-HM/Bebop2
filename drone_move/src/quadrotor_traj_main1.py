


from numpy import *
import matplotlib.pyplot as plt
import optim_quadrotor1
from pol_matrix_comp import pol_matrix_comp


num_horizon = 200
t_fin = 5
tot_time = linspace(0.0, t_fin , num_horizon) 
t = t_fin/len(tot_time)


tot_time_copy = tot_time.reshape(num_horizon, 1)
P, Pdot, Pddot = pol_matrix_comp(tot_time_copy)
nvar = shape(P)[1]


x_init = 0.0
y_init = 0.0

vx_init = 0.0
ax_init = 0.0

vy_init = 0.0
ay_init = 0.0

ax_max = 2.0
ay_max = 2.0

jx_max = 1.0
jy_max = 1.0

vx_max = 3.0
vy_max = 3.0

x_fin =8.0
y_fin = 8.0

vx_fin = 0.0
vy_fin = 0.0

ax_fin = 0.0
ay_fin = 0.0


def compute():
    x, xdot, xddot, y, ydot, yddot = optim_quadrotor1.optim_quadrotor(num_horizon, P, Pdot, Pddot, x_init, y_init, vx_init, vy_init, ax_init, ay_init, x_fin, y_fin, vx_fin, vy_fin, ax_fin, ay_fin, ax_max, ay_max, vx_max, vy_max, jx_max, jy_max)
    return xddot, yddot



def compute_roll_pitch():
    pitch = []
    roll = []
    xddot, yddot = compute()
    for i in range (size (xddot)):
        u  = math.sqrt(xddot[i]**2 + yddot[i]**2 + 100)
        temp_pitch =math.asin(-yddot[i]/u)
        temp_roll = math.asin(xddot[i]/(u*math.cos(temp_pitch)))
        pitch.append(temp_pitch)
        roll.append(temp_roll)
    return pitch, roll
# pitch, roll, x,y= compute_roll_pitch()

# # xdot, ydot, x, y = compute()
# # print (size(x))
# plt.figure(1)
# plt.plot(x, y)
# plt.figure(2)
# plt.plot(pitch, '-r')
# plt.plot(roll, '-k')

# xddot, yddot = compute()
# plt.figure(3)
# plt.plot(xddot, '-r')
# plt.plot(yddot, '-k')
# plt.show()

