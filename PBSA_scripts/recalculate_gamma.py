#/bin/python

import sys;
import math;

out_filename = "feps_levels_all_brand_new.dat"
path_prototype = "fep_level_%n"
explicit_filename = "free_energy_fabp_explicit.dat"
opt_rmse_filename = "rmse_opt.dat"
rmse_array_filename = "rmse_array.dat"


eps_min = 1
eps_max = 19.5
eps_step = 0.5

gamma_min = 0
gamma_max = 0.5
gamma_step = 0.01

fep_level_min = -3.5
fep_level_max = 4.0
fep_level_step = 0.5

def frange(min, max, step):
	retval = min
	while(retval <= max):
		yield retval
		retval += step
 
def calcGamma(elec, apol, gamma):
	return (elec + apol * gamma)/4.184;
	
gamma_vals = [];
for gamma in frange(gamma_min, gamma_max, gamma_step):
	gamma_vals.append(round(gamma,2))
eps_vals = [];
for eps in frange(eps_min,eps_max, eps_step):
	eps_vals.append(round(eps,1))
fep_levels = [];
for fep_lev in frange(fep_level_min,fep_level_max, fep_level_step):
	fep_levels.append(fep_lev)
data = []
header = "eps\tgamma\t"
for fep_lev in frange(fep_level_min,fep_level_max, fep_level_step):
	fep_lev_data = []
	path = path_prototype.replace("%n",str(fep_lev))
	header+=path+"\t"
	for eps in frange(eps_min,eps_max, eps_step):
		gammas = []
		#read file
		fn = "apbs_"+str(eps) + ".out"
		apbs = open((path + "/" + fn).replace(".0",""),'r')
		for line in apbs:
			if "Global net ELEC energy" in line:
				elec_energy = float(line.split()[5]);
			if "Global net APOL energy" in line:
				apol_energy = float(line.split()[5]);
		#recalculate gamma
		for gamma in frange(gamma_min, gamma_max, gamma_step):
			val = calcGamma(elec_energy,apol_energy,gamma)
			gammas.append(val)
		fep_lev_data.append(gammas)
	data.append(fep_lev_data)
	
output = open(out_filename,'w')

output.write(header+"\n")
for eps in range(0,len(data[0])):
	eps_val = eps_vals[eps]
	offsets = []
	for gamma in range(0,len(data[0][0])):
		gamma_val = gamma_vals[gamma];
		sum=0;
		line = str(eps_val) + "\t" + str(gamma_val) + "\t"
		for fep_lev in range(0,len(data)):
			line += str(data[fep_lev][eps][gamma]) + "\t"
			sum+=data[fep_lev][eps][gamma]
		output.write(line.replace(".",",") + "\n")
		offsets.append(sum/len(data))
	
output.close()

explicit_file = open(explicit_filename,'r')
explicit = []
for line in explicit_file:
	explicit.append(float(line.split()[1]))

explicit_file.close()
#calculate offsets
offset=[]
for eps in range(0,len(data[0])):
	offsets = []
	for gamma in range(0,len(data[0][0])):
		sum=0;
		line = str(eps_val) + "\t" + str(gamma_val) + "\t"
		for fep_lev in range(0,len(data)):
			line += str(data[fep_lev][eps][gamma]) + "\t"
			sum+=(explicit[fep_lev]-data[fep_lev][eps][gamma])
		offsets.append(sum/len(data))
	offset.append(offsets)
	

#calculate rmse array
rmse_min = 99999
rmse_min_eps_ind = 0;
rmse_min_gamma_ind = 0;
rmse = []
rmseArrayFile = open(rmse_array_filename,'w')
rmseArrayFile.write("\t"+str(gamma_vals).replace("[","").replace("]","").replace(",", "\t").replace(".",",") + "\n")
for eps in range(0,len(data[0])):
	rmses = []
	for gamma in range(0,len(data[0][0])):
		sum=0;
		line = str(eps_val) + "\t" + str(gamma_val) + "\t"
		for fep_lev in range(0,len(data)):
			line += str(data[fep_lev][eps][gamma]) + "\t"
			sum+=(explicit[fep_lev] - data[fep_lev][eps][gamma] - offset[eps][gamma])**2
		cur_rmse = math.sqrt(sum/len(data))
		rmses.append(cur_rmse)
		if cur_rmse < rmse_min:
			rmse_min = cur_rmse
			rmse_min_eps_ind = eps
			rmse_min_gamma_ind = gamma
	rmseArrayFile.write(str(eps_vals[eps]) + "\t" + str(rmses).replace("[","").replace("]","").replace(",","\t").replace(".",",") + "\n")
	rmse.append(rmses)


rmseArrayFile.close()

print("RMSE Min : " + str(rmse_min))
print("RMSE Min Epsilon: " + str(eps_vals[rmse_min_eps_ind]))
print("RMSE Min Gamma: " + str(gamma_vals[rmse_min_gamma_ind]))
rmseFile = open(opt_rmse_filename, 'w')
rmseFile.write("fep_level\timplicit @ (eps: " + str(eps_vals[rmse_min_eps_ind]) + "gamma: " + str(gamma_vals[rmse_min_gamma_ind]) + ")\texplicit\n")
for fep_lev in range(0,len(data)):
	line = str(fep_levels[fep_lev]) + "\t"
	line += str(data[fep_lev][rmse_min_eps_ind][rmse_min_gamma_ind]) + "\t"
	line += str(explicit[fep_lev]) + "\n"
	rmseFile.write(line.replace(".",","))

rmseFile.close();

	





