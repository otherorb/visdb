# I went down a terrible rabbit-hole trying to recreate some docker stuff 
# using python and then decided that was a waste of time and these
# commands would do the job just fine. Note that this file is purposefully
# not executable and does not have bash magic notation at the beginning of the file. 
# This is so I avoid dangerous, unthinking deletion of docker containers and images 
# that I don't want to lose. 

# I strongly recommend the commands within parentheses (not including the parentheses) 
# be run by themselves before attempting to run the destructive commands. The
# commands here assume there's only one postgresql service running.
# If that's not true, then one needs to be selective of which one is killed or 
# deleted.

# If you will be copy-pasting these commands, note that the "-" at the front of the
# command is meant to make this file not something that can be run with a ./ command
# Don't copy the "-".


# Create a new postgres docker container using the image available in Docker's 
# service. This relies on the existing docker-compose.yml file in this directory. 
# 
# This command simply pulls the postgres image from docker hub. This is helpful, but it
# does not spin up the container. 
- docker-compose pull

# If the image is here (for example from the previous pull command), this command 
# spins up the container. If the image isn't downloaded from the docker hub,
# this also pulls that image down. 
- docker-compose up -d

# Find the docker container that is a postgresql service
- docker ps -a | grep -i postgres

# Stop the docker container that is a postgresql service:
- docker stop $(docker ps -a | grep -i postgres | awk '{print $1}')

# Remove the docker container that is a postgresql service:
- docker rm $(docker ps -a | grep -i postgres | awk '{print $1}')

# Delete the docker image that is a postgresql service:
- docker rmi --force $(docker images | grep -i postgres | awk '{print $3}')

# Delete the postgres-data directory
- sudo rm -rf postgres-data
# Delete the postgres transaction log directory
- sudo rm -rf pgdata
