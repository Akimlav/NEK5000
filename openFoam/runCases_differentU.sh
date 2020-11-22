
for i in -10.370 -14.815 -18.518 -20.576 -22.634 -27.160 -35.308; do  
	echo "######################### case_$i"
	mkdir case_$i
	U=$(awk "BEGIN {printf \"%.5f\n\", $i}")
	cp -R ./head_case/* ./case_$i/		
	sed -i "s/(U 0 0)/("$U" 0 0)/g" ./case_$i/0/U
	cp -R ./headCase/constant/polyMesh ./case_$i/constant/	
	echo "topoSet ./case_$i";

	echo "Decomposing case ./case_$i";
	decomposePar -force -case ./case_$i > ./case_$i/1_decompose.log
	echo "Running potentialFoam at ./case_$i";
	echo "Check log at $(pwd)/case_$i/2_potential.log";
	mpirun -H hpc3 -np 20 -oversubscribe potentialFoam -case ./case_$i -parallel > ./case_$i/2_potential.log
	echo "Running simpleFoam at ./case_$i";
	echo "Check log at $(pwd)/case_$i/3_simple.log";
	mpirun -H hpc3 -np 20 -oversubscribe simpleFoam -case ./case_$i -parallel > ./case_$i/3_simple.log
	echo "Running yPlus calculation at ./case_$i";
	echo "Check log at $(pwd)/case_$i/4_yPlus.log";
	mpirun -H hpc3 -np 20 -oversubscribe simpleFoam -postProcess -func yPlus -case ./case_$i -parallel > ./case_$i/4_yPlus.log
	echo "Running reconstructPar at ./case_$i";
	reconstructPar -case ./case_$i > ./case_$i/5_reconstruct.log
	rm -rf ./case_$i/processor*
done


