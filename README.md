## Test task for SheepFish company

Used:

```
 - Django
 - PostgreSQL
 - Redis
 - Celery
 - wkhtmltopdf
```

Usage:

```
 > git clone https://github.com/ExSumbiT/SheepFish_TT.git
 > cd SheepFish_TT
 > pip install -r requirements.txt
 Replace the settings in the .env file with your own
```

Run docker-compose:

```
 > docker-compose up -d --build
```

Apply migrations and load Printer fixtures:

```
 > cd SheepFish
 > python manage.py migrate
 > python manage.py loaddata printers.json
```

Run Celery worker:

```
 > cd SheepFish
 > celery -A SheepFish worker -l info -P threads
```

Run django server:

```
 > cd SheepFish
 > python manage.py runserver
```

Printer program imitation:

```
 > cd SheepFish
 > cd printer_program
Replace printer api_key with your own
 > python printer.py
```