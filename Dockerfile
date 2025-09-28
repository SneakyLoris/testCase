FROM python:3.13-trixie

COPY crontab /etc/cron.d/my-cron
RUN chmod 644 /etc/cron.d/my-cron
RUN apt update
RUN apt install -y cron

RUN pip install --upgrade pip

WORKDIR /work_dir
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/main.py"]