



from scipy.io import loadmat
import matplotlib.pyplot as plt

# scipy.io.savemat('x_quad.mat', {'x_quad': x_leader_interp})
# scipy.io.savemat('y_quad.mat', {'y_quad': y_leader_interp})
# scipy.io.savemat('z_quad.mat', {'z_quad': z_leader_interp})


ax_traj_temp = loadmat('ax_robot_1.mat')
ax_traj_robot_1 = ax_traj_temp['ax_quad'].squeeze()


ay_traj_temp = loadmat('ay_robot_1.mat')
ay_traj_robot_1 = ay_traj_temp['ay_quad'].squeeze()



ax_traj_temp = loadmat('ax_robot_2.mat')
ax_traj_robot_2 = ax_traj_temp['ax_quad'].squeeze()


ay_traj_temp = loadmat('ay_robot_1.mat')
ay_traj_robot_2 = ay_traj_temp['ay_quad'].squeeze()


pitch_temp = loadmat('pitch_robot_1.mat')
pitch_robot_1 = pitch_temp['pitch_quad'].squeeze()

roll_temp = loadmat('roll_robot_1.mat')
roll_robot_1 = roll_temp['roll_quad'].squeeze()

pitch_temp = loadmat('pitch_robot_2.mat')
pitch_robot_2 = pitch_temp['pitch_quad'].squeeze()

roll_temp = loadmat('roll_robot_2.mat')
roll_robot_2 = roll_temp['roll_quad'].squeeze()



plt.plot(roll_robot_1)
plt.plot(roll_robot_2)
plt.show()