FROM python:3.14.0-alpine3.22
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
#aktualizace tabulek na nejnovejsi db model
#RUN python app.py db upgrade
EXPOSE 5000
CMD ["python", "app.py"]