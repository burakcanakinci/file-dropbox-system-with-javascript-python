FROM python:3.6

EXPOSE 4500

RUN apt-get update && apt-get install -y vim

#WORKDIR /app


ADD . .
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
COPY ./logFile.txt ./logs/

COPY requirements.txt .
RUN pip install -r requirements.txt

#CMD ["python", "./views.py" ]

