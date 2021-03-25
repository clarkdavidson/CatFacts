FROM python:3.9-alpine
WORKDIR /root/workspace/catfacts
RUN apk update && apk add ca-certificates
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install requests
RUN pip install boto3
COPY catfacts.py ./
CMD ["python", "catfacts.py"]
EXPOSE 5000