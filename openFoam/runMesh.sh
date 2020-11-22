
#for j in 1 1.2 1.4 1.6 1.8 2.0 2.2 2.4 ; do
for j in 3.5; do
    echo "######################### CASE_$j"
    mkdir mesh_$j

    	A=$(awk "BEGIN {printf \"%.0f\n\", $j*23}")
	B=$(awk "BEGIN {printf \"%.0f\n\", $j*9}")
	C=$(awk "BEGIN {printf \"%.0f\n\", $j*22}")
	D=$(awk "BEGIN {printf \"%.0f\n\", $j*23}")
	E=$(awk "BEGIN {printf \"%.0f\n\", $j*9}")
	F=$(awk "BEGIN {printf \"%.0f\n\", $j*10}")
	G=$(awk "BEGIN {printf \"%.0f\n\", $j*23}")
	H=$(awk "BEGIN {printf \"%.0f\n\", $j*9}")
	I=$(awk "BEGIN {printf \"%.0f\n\", $j*16}")
	J=$(awk "BEGIN {printf \"%.0f\n\", $j*23}")
	K=$(awk "BEGIN {printf \"%.0f\n\", $j*9}")
	L=$(awk "BEGIN {printf \"%.0f\n\", $j*13}")
	M=$(awk "BEGIN {printf \"%.0f\n\", $j*23}")
	N=$(awk "BEGIN {printf \"%.0f\n\", $j*9}")
	O=$(awk "BEGIN {printf \"%.0f\n\", $j*11}")
	P=$(awk "BEGIN {printf \"%.0f\n\", $j*23}")
	Q=$(awk "BEGIN {printf \"%.0f\n\", $j*9}")
	R=$(awk "BEGIN {printf \"%.0f\n\", $j*13}")

    cp -R ./head_mesh/* ./mesh_$j/
    sed -i "s/(A B C)/("$A" "$B" "$C")/g" ./mesh_$j/system/blockMeshDict
    sed -i "s/(D E F)/("$D" "$E" "$F")/g" ./mesh_$j/system/blockMeshDict
    sed -i "s/(G H I)/("$G" "$H" "$I")/g" ./mesh_$j/system/blockMeshDict	
    sed -i "s/(J K L)/("$J" "$K" "$L")/g" ./mesh_$j/system/blockMeshDict
    sed -i "s/(M N O)/("$M" "$N" "$O")/g" ./mesh_$j/system/blockMeshDict
    sed -i "s/(P Q R)/("$P" "$Q" "$R")/g" ./mesh_$j/system/blockMeshDict

    echo "Running blockMesh at ./mesh_$j"
    blockMesh -case ./mesh_$j > ./mesh_$j/1_blockMesh.log

    echo "Running renumberMesh at ./mesh_$j"
    renumberMesh -case ./mesh_$j -overwrite > ./mesh_$j/2_renumberMesh.log

    echo "Running topoSet at ./mesh_$j"
    for i in 1 2 3 4 5; do
		topoSet -case ./mesh_$j -dict ./system/topoSetDict.${i} > ./mesh_$j/3_topoSet.log
		refineMesh -case ./mesh_$j -dict ./system/refineMeshDict -overwrite > ./mesh_$j/3_topoSet.log
    done
#    echo "surfaceFeatureExtract at ./mesh_$j"; 
#    surfaceFeatureExtract -case ./mesh_$j > ./mesh_$j/4_surfaceFeatureExtract.log
#    echo "Decomposing mesh ./mesh_$j";
#    decomposePar -force -case ./mesh_$j > ./mesh_$j/5_decompose.log
#    echo "Running SnappyHexMesh at ./mesh_$j";
#    mpirun -H hpc5 -np 20 --oversubscribe snappyHexMesh -case ./mesh_$j -parallel > ./mesh_$j/6_snappy.log
#    echo "Running reconstructParMesh at ./mesh_$j";
#    reconstructParMesh -case ./mesh_$j -latestTime > ./mesh_$j/7_reconstruct.log rm -rf ./mesh_$j/processor*
#    echo "Running renumberMesh after Snappy at ./mesh_$j";
#    renumberMesh -case ./mesh_$j > ./mesh_$j/8_renumberMesh.log
done

