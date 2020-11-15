# Docker Notes

# Confirms that the server side of Docker is running
docker info

# Verifies that Docker has installed correctly
# The docker run command starts an image 
docker run hello-world 

# Look at your docker images
docker images

# This is how we start the latest version of an Ubuntu image and run bash
# If you omit the latest tag, it will grab the latest by default
docker run -ti ubuntu:latest bash
-ti = (terminal interactive)

# Check what release you are running while in a linux environment
cat /etc/lsb-release

# Images and containers have different IDs 

# Take a look at running images
docker ps
# See all containers
docker ps -a 
# See the last container to exit
docker ps -l

# Take a container and make an image out of it (So you can access the files / your work again)
docker commit 




