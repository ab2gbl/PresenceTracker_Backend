FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD sh -c "python manage.py makemigrations --noinput && \
           python manage.py migrate --noinput && \
           python manage.py runserver 0.0.0.0:8000"