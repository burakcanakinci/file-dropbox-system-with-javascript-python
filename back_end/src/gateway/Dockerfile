# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /src

# copy the dependencies file to the working directory
#COPY requirements.txt .
COPY . .
COPY logs/logFile-gateway.txt ./logs/

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local gateway directory to the working directory
#COPY gateway.py .

# command to run on container start
