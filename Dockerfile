FROM python:3.10
RUN mkdir /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
RUN pip install --upgrade pip 
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000

CMD python manage.py migrate contenttypes \
    && python manage.py makemigrations admin auth sessions \
    && python manage.py migrate admin \
    && python manage.py migrate auth \
    && python manage.py migrate sessions \
    && python manage.py makemigrations diario mentha protocolo \
    && python manage.py migrate diario \
    && python manage.py migrate mentha \
    && python manage.py migrate protocolo \
    && python manage.py runserver 0.0.0.0:8000