# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local gateway directory to the working directory
#COPY ../src/auth/ .
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
COPY app.py .
COPY logs/log_file.txt ./logs/
COPY . ./src/auth

# command to run on container start
#CMD [ "python", "./app.py" ]
