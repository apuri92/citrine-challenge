rm ./data/out*txt

./sampler.py ./data/mixture.txt ./data/out_mixture.txt 1000
./sampler.py ./data/example.txt ./data/out_example.txt 1000
./sampler.py ./data/formulation.txt ./data/out_formulation.txt 1000
./sampler.py ./data/alloy.txt ./data/out_alloy.txt 1000

wc -l data/out_*