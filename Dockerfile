FROM python:3

EXPOSE 8000

COPY requirements.txt ./

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD ["flask", "--app", "app", "run", "--port=5000", "--host=0.0.0.0"]
