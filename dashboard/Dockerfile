FROM python
WORKDIR /Users/gawsalya/Sigma/Coursework-Data-Engineering-Week-3/dashboard

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY graph_func.py .
COPY graphs.py .

EXPOSE 8501

CMD streamlit run graphs.py