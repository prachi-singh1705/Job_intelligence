import os
import threading

def run_scraper():
    os.system("python main.py")

def run_dashboard():
    os.system("streamlit run app.py")

t1 = threading.Thread(target=run_scraper)
t2 = threading.Thread(target=run_dashboard)

t1.start()
t2.start()
