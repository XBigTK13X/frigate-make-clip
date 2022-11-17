FROM python

RUN apt update

RUN apt install -y mkvtoolnix

COPY ./ /root/app

WORKDIR /root/app/source

RUN pip install -r requirements.txt

WORKDIR /root/app

EXPOSE 8765

WORKDIR /root/app

CMD ["/bin/bash","-c","script/run-app.sh"]