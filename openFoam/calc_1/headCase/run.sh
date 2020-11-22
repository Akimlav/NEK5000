#!/bin/sh
path="loc"
path1="loc1"
echo "Bash: Running setFields"
setFields -case $path > $path/2_setFields.log
echo "Bash: Running decomposePar"
decomposePar -case $path > $path/3_decomposePar.log
echo "Bash: Running potentialFoam"
mpirun -np n_of_proc* potentialFoam -case $path1 -parallel > $path1/4_potential.log
echo "Bash: Running solver"
mpirun -np n_of_proc* interFoam -case $path1 -parallel > $path1/5_solution.log
echo "Bash: Running reconstructPar"
reconstructPar -case $path > $path1/6_reconstructPar.log
echo "Bash: Calculating yPlus"
pimpleFoam -postProcess -func yPlus -case $path1 > $path1/6_yPlus.log
echo "Bash: Removing trash"
rm -rf ./$path1/processor* > $path1/7_rm.log
echo "Bash: Job done!"

