FROM pytorch/pytorch

ENV TZ="Asia/Kolkata"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
#RUN chmod +rx ./script.sh
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
