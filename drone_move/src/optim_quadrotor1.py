


from numpy import *
from cvxopt import solvers
import cvxopt
from scipy.linalg import block_diag



def optim_quadrotor(num_horizon, P, Pdot, Pddot, x_init, y_init, vx_init, vy_init, ax_init, ay_init, x_fin, y_fin, vx_fin, vy_fin, ax_fin, ay_fin, ax_max, ay_max, vx_max, vy_max, jx_max, jy_max):

	num = num_horizon
	nvar = shape(P)[1]
	nvar_offset = nvar-3

	cx_1 = x_init
	cx_2 = vx_init
	cx_3 = ax_init

	cy_1 = y_init
	cy_2 = vy_init
	cy_3 = ay_init

	x_offset = cx_1*P[1:num, 0]+cx_2*P[1:num, 1]+cx_3*P[1:num, 2]
	vx_offset = cx_1*Pdot[1:num, 0]+cx_2*Pdot[1:num, 1]+cx_3*Pdot[1:num, 2]
	ax_offset = cx_1*Pddot[1:num, 0]+cx_2*Pddot[1:num, 1]+cx_3*Pddot[1:num, 2]

	y_offset = cy_1*P[1:num, 0]+cy_2*P[1:num, 1]+cy_3*P[1:num, 2]
	vy_offset = cy_1*Pdot[1:num, 0]+cy_2*Pdot[1:num, 1]+cy_3*Pdot[1:num, 2]
	ay_offset = cy_1*Pddot[1:num, 0]+cy_2*Pddot[1:num, 1]+cy_3*Pddot[1:num, 2]

	
	A_x_fin = hstack(( P[-1, 3:nvar].reshape(1, nvar-3), zeros((1, nvar-3   ))  ))
	B_x_fin = array([x_fin-x_offset[-1] ]) 
	
	A_y_fin = hstack(( zeros((1, nvar-3   )), P[-1, 3:nvar].reshape(1, nvar-3)  ))
	B_y_fin = array([ y_fin-y_offset[-1] ]) 

	A_pos_fin = vstack((A_x_fin, A_y_fin))
	B_pos_fin = hstack(( B_x_fin, B_y_fin  ))

	A_vel_fin = block_diag( Pdot[-1,3:nvar], Pdot[-1,3:nvar] )
	B_vel_fin = hstack(( vx_fin-vx_offset[-1], vy_fin-vy_offset[-1]  ))

	A_acc_fin = block_diag( Pddot[-1,3:nvar], Pddot[-1,3:nvar] )
	B_acc_fin = hstack(( ax_fin-ax_offset[-1], ay_fin-ay_offset[-1]  ))
	
	#######################################################################

	A_vx_ineq = vstack(( Pdot[1:num,3:nvar], -Pdot[1:num,3:nvar] ))
	B_vx_ineq = hstack(( vx_max*ones(num-1)-vx_offset, vx_max*ones(num-1)+vx_offset  ))

	A_ax_ineq = vstack(( Pddot[1:num,3:nvar], -Pddot[1:num,3:nvar] ))
	B_ax_ineq = hstack(( ax_max*ones(num-1)-ax_offset, ax_max*ones(num-1)+ax_offset  ))
	
	A_jx_ineq = vstack(( identity(nvar_offset), -identity(nvar_offset) ))
	B_jx_ineq = hstack(( jx_max*ones(nvar_offset), jx_max*ones(nvar_offset)  ))



	A_vy_ineq = vstack(( Pdot[1:num,3:nvar], -Pdot[1:num,3:nvar] ))
	B_vy_ineq = hstack(( vy_max*ones(num-1)-vy_offset, vy_max*ones(num-1)+vy_offset  ))

	A_ay_ineq = vstack(( Pddot[1:num,3:nvar], -Pddot[1:num,3:nvar] ))
	B_ay_ineq = hstack(( ay_max*ones(num-1)-ay_offset, ay_max*ones(num-1)+ay_offset  ))
	
	A_jy_ineq = vstack(( identity(nvar_offset), -identity(nvar_offset) ))
	B_jy_ineq = hstack(( jy_max*ones(nvar_offset), jy_max*ones(nvar_offset)  ))

	A_vel_ineq = block_diag( A_vx_ineq, A_vy_ineq  )
	B_vel_ineq = hstack(( B_vx_ineq, B_vy_ineq   ))

	A_acc_ineq = block_diag(A_ax_ineq, A_ay_ineq)
	B_acc_ineq = hstack(( B_ax_ineq, B_ay_ineq  ))

	A_jerk_ineq = block_diag(A_jx_ineq, A_jy_ineq)
	B_jerk_ineq = hstack(( B_jx_ineq, B_jy_ineq  ))
	
	A_ineq = vstack((A_vel_ineq, A_acc_ineq, A_jerk_ineq    ))
	B_ineq = hstack((B_vel_ineq, B_acc_ineq, B_jerk_ineq      ))

	A_eq = vstack(( A_vel_fin, A_acc_fin  ))
	B_eq = hstack(( B_vel_fin, B_acc_fin  ))

	weight = 100

	cost = weight*dot(A_pos_fin.T, A_pos_fin)+0.01*identity(2*nvar_offset)
	linccost = -weight*dot(A_pos_fin.T, B_pos_fin)

	sol = solvers.qp( cvxopt.matrix(cost, tc = 'd'), cvxopt.matrix(linccost, tc = 'd'), cvxopt.matrix(A_ineq, tc = 'd'), cvxopt.matrix(B_ineq, tc = 'd'), cvxopt.matrix(A_eq, tc = 'd'), cvxopt.matrix(B_eq, tc = 'd')    )

	sol = array(sol['x']).squeeze()

	cx = sol[0:nvar_offset]
	cy = sol[nvar_offset:2*nvar_offset]

	cx_sol = hstack((cx_1, cx_2, cx_3, cx  ))
	cy_sol = hstack((cy_1, cy_2, cy_3, cy   ))

	x = dot(P, cx_sol)
	xdot = dot(Pdot, cx_sol)
	xddot = dot(Pddot, cx_sol)

	y = dot(P, cy_sol)
	ydot = dot(Pdot, cy_sol)
	yddot = dot(Pddot, cy_sol)

	return x, xdot, xddot, y, ydot, yddot
	

