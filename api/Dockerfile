FROM python:3.10
RUN mkdir /app
WORKDIR /app
ADD ./web .
RUN pip install -r requirements.txt
EXPOSE 8090
CMD ["python", "app.py", "runserver"]
