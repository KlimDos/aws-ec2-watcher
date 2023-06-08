
FROM python:slim-buster
LABEL maintainer="Sasha Alimov klimdos@gmail.com"
WORKDIR /
COPY src/ src/
RUN pip install -r src/requirements.txt
#EXPOSE 5000
ARG EC2_MAX_HOURS
#ENV FLASK_RUN_PORT=${FLASK_RUN_PORT} 
ENTRYPOINT ["python"]
CMD [ "src/app.py" ]
