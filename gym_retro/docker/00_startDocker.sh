#!/bin/bash

docker_cont_name="gym_retro"
docker_repo_name="gym_repo"
current_dir=`pwd`/docker


if [ -d $current_dir/contents/card ]; then rm -rf $current_dir/contents/card; cp -r $current_dir/card $current_dir/contents;  else cp -r $current_dir/card $current_dir/contents;  fi 
if [ -d $current_dir/contents/AI/card ]; then rm -rf $current_dir/contents/AI/card; mkdir $current_dir/contents/AI/card; cp -r $current_dir/card/python $current_dir/contents/AI/card; else mkdir $current_dir/contents/AI/card; cp -r $current_dir/card/python $current_dir/contents/AI/card; fi 


os_type=$(uname -s)
arch_type=$(uname -m)

is_image_maked=`docker images | grep "$docker_repo_name" | awk '{print $1}'`
is_container_run=`docker ps -a --format "{{.Image}},{{.Status}}" | grep $docker_repo_name | awk -F "," '{print $2}' | awk '{print $1}'`

img_Flag=0
cont_Flag=0

if [ -n "$socat_pid" ]; then
	echo "kill socat PID"
	kill -9 $socat_pid
fi

if [ ! -n "$is_image_maked" ]; then

	if [ "$os_type" = "Darwin" ]; then
		xserver_ip=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
		socat_pid=`lsof -i TCP:6000 | awk '{print $2}' | grep -ve '[A-Z]'`

		if [ "$arch_type" = "arm64" ]; then

			
			defaults write org.xquartz.X11 enable_iglx -bool true

			open -a XQuartz
			socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &
			docker build --platform linux/amd64 \
				-f $current_dir/Dockerfile \
				--tag $docker_repo_name .
		else
			# For intel Mac
			docker build \
				--platform linux \
				--build-arg TZ=$(cat /etc/timezone) \
				-f $current_dir/Dockerfile \
				--tag $docker_repo_name .
		fi
	elif [ "$os_type" = "Linux" ]; then
			docker build \
				--platform linux \
				--build-arg TZ=$(cat /etc/timezone) \
				-f $current_dir/Dockerfile \
				--tag $docker_repo_name .
		#docker build --platform linux --tag $docker_repo_name .
	fi
	img_Flag=1

elif [ "$is_image_maked" = "$docker_repo_name" ]; then
	img_Flag=1
else
	img_Flag=0
fi


is_image_maked=`docker images | grep "$docker_repo_name" | awk '{print $1}'`
if [ "$img_Flag" = 1 ]; then
		if [ -n "$is_image_maked" ]; then
			if [ ! -n "$is_container_run" ]; then
				docker run -d -it \
					-e DISPLAY=$xserver_ip:0 \
					-v $current_dir/contents/AI:/home/conda \
					-v $current_dir/contents/card:/home/card \
					-p 80:80 \
					-v /tmp/.X11-unix:/tmp/.X11-unix \
					--gpus all \
					--name $docker_cont_name $docker_repo_name /bin/bash

				is_container_run=`docker ps -a --format "{{.Image}},{{.Status}}" | grep $docker_repo_name | awk -F "," '{print $2}' | awk '{print $1}'`
			fi
		fi
fi

if [ -n "$is_container_run"  ]; then
	if [ "$is_container_run" = "Exited" ] || [ "$is_container_run" = "Created" ]; then
		docker start $docker_cont_name
		docker attach $docker_cont_name
	else
		docker attach $docker_cont_name
	fi
fi
