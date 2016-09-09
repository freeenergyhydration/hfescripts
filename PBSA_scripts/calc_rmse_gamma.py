#!/usr/bin/python

import math

print "Hello Python"

infilename = "feps_levels_all_gamma.dat"
outfilename = "rmse_gamma_out.dat"

dataArray = []

file = open(infilename)

lines = file.readlines()

for line in lines:
  vals = line.replace("]","").replace("\n","").split(",[")
  tarr = []
  for val in vals:
    array = val.split(",")
    tarr.append(array)
  dataArray.append(tarr)
  
dataArray[0] = dataArray[0][0]

fep_lev_count = len(lines) - 1;

# result append to table
a = []
for gamma in range(1, len(dataArray[1])-2):
    arow = []
    for eps in range(0, len(dataArray[1][1])):
      avalue = 0
      for fep_lev in range (1, fep_lev_count+1):
	dataArray[fep_lev][gamma][eps] = float(dataArray[fep_lev][gamma][eps]) - float(dataArray[fep_lev][len(dataArray[fep_lev])-1][0])
	avalue += dataArray[fep_lev][gamma][eps];
      avalue /= fep_lev_count;
      arow.append(avalue);
    a.append(arow);

# rmse result
rmse = []
for gamma in range(1, len(dataArray[1]) - 2 ):
  rmserow = []
  for eps in range(0, len(dataArray[1][1])):
    rmse_eps = 0
    for fep_lev in range (1, fep_lev_count+1):
      rmse_eps += (dataArray[fep_lev][gamma][eps] - a[gamma-1][eps])**2 # rmse += (x_i - y_i - a)^2
    rmse_eps = math.sqrt(rmse_eps/fep_lev_count)  
    rmserow.append(rmse_eps)
  rmse.append(rmserow)

outfile = open(outfilename,'w')

for gamma in range(0, len(rmse)):
  outfile.write(str(dataArray[0][gamma+1]))
  outfile.write(",")
  outfile.write(str(rmse[gamma]).replace("[","").replace("]",""))
  outfile.write("\n")
  
outfile.close()
