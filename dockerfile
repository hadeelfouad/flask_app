FROM python:3.6-alpine
COPY . /thndr-app
WORKDIR /thndr-app
RUN python3 -m pip install --user -r requirements.txt
EXPOSE 5000
CMD ["python3", "main.py"]