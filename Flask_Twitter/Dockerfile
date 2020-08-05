FROM python:3.8
RUN mkdir -p /usr/src/app1/
WORKDIR /usr/src/app1/
COPY . /usr/src/app1/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080

CMD [“python”, “flask_app1.py”]
