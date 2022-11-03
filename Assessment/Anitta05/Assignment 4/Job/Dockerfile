FROM python:3.10.6
COPY requirements.txt ./app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python","./app.py"]
