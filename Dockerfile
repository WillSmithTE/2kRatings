FROM postgres:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3.7-dev
# RUN apt-get install postgresql-server-dev-10 gcc python3-dev musl-dev
# RUN pip3 install psycopg2

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# USER postgres
# EXPOSE 5432
# VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD [ "python3", "./main.py" ]