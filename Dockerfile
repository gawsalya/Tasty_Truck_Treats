FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY clean_database.sh .
COPY schema.sql .

COPY functions_for_etl.py .
COPY main.py .

CMD python3 main.py