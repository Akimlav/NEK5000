#!/bin/sh
path="loc"
path1="loc1"
#echo "Bash: Running setFields"
#setFields -case $path > $path/2_setFields.log
echo "Bash: Running decomposePar"
decomposePar -case $path > $path/3_decomposePar.log
echo "Bash: Running potentialFoam"
mpirun -np 28 potentialFoam -case $path1 -parallel > $path1/4_potential.log
echo "Bash: Running solver"
mpirun -np 28 pimpleFoam -case $path1 -parallel > $path1/5_solution.log
echo "Bash: Running reconstructPar"
reconstructPar -case $path > $path1/6_reconstructPar.log
echo "Bash: Removing trash"
rm -rf ./$path1/processor* > $path1/7_rm.log
echo "Bash: Job done!"

