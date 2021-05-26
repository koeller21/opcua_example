FROM python:3


RUN apt update && apt upgrade -y

## install them requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

## set workdir
WORKDIR /opcua
COPY ./src .

# run command
CMD python3 server_washing_machine.py