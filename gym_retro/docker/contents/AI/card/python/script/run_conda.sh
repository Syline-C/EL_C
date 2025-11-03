#!/bin/bash


current_dir="/home/conda"

. /root/miniconda3/etc/profile.d/conda.sh 
conda init bash

#conda config --remove-key channels || true
#
#
#conda config --add channels pytorch
#conda config --add channels nvidia
#conda config --add channels conda-forge
#conda config --add channels defaults
#conda config --set channel_priority strict
#conda clean --index-cache -y
#
#conda init bash

is_retro_exist=`conda env list | grep gym_retro | awk '{print $1}'`

if [ ! -n "$is_retro_exist" ]; then
	CONDARC=$current_dir/card/python/.condarc conda env create -n gym_retro --file $current_dir/card/python/yaml/base.yml

	CONDARC=$current_dir/card/python/.condarc  conda env update -n gym_retro --file $current_dir/card/python/yaml/vision.yml
	CONDARC=$current_dir/card/python/.condarc  conda env update -n gym_retro --file $current_dir/card/python/yaml/rl.yml
	CONDARC=$current_dir/card/python/.condarc  conda env update -n gym_retro --file $current_dir/card/python/yaml/ui.yml
	CONDARC=$current_dir/card/python/.condarc  conda env update -n gym_retro --file $current_dir/card/python/yaml/jupyter.yml
	CONDARC=$current_dir/card/python/.condarc  conda env update -n gym_retro --file $current_dir/card/python/yaml/yolo.yml

	# (GPU는 택1)
	CONDARC=$current_dir/card/python/.condarc conda env update -n gym_retro --file $current_dir/card/python/yaml/gpu_pytorch.yml
	# or
	# conda env update -n mario -f envs/gpu-tensorflow.yml
fi



echo ""
echo "================================="
conda env list
echo "================================="
echo ""

