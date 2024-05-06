FROM 24663209/docker-selenium:1.0.3
ADD . app
WORKDIR app
#RUN pip install -r requirements.txt