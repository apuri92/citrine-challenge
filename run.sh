# rm ./data/out*txt
./sampler.py ./data/example1D.txt ./data/out_example1D.txt 1000
./sampler.py ./data/example2D.txt ./data/out_example2D.txt 1000
./sampler.py ./data/example3D.txt ./data/out_example3D.txt 1000

./sampler.py ./data/mixture.txt ./data/out_mixture.txt 1000
./sampler.py ./data/formulation.txt ./data/out_formulation.txt 1000
./sampler.py ./data/alloy.txt ./data/out_alloy.txt 1000

wc -l data/out_*
