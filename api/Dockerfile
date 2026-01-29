FROM python:3.8.18
RUN mkdir /app
WORKDIR /app
ADD ./web .
RUN pip install -r requirements.txt
EXPOSE 8090
CMD ["python", "app.py", "runserver"]
