import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
from flask import Flask, request, jsonify
import os
import json

def get_unique_users_count():
    response = requests.get("https://meistrelis.herokuapp.com/api/UserServices/GetAllServicesNoKey")
    df = pd.DataFrame(json.loads(response.text))
    return len(df["mechanicEmail"].unique())

def get_user_services_stats():
    tmpfile = BytesIO()
    plt.tight_layout()
    response = requests.get("https://meistrelis.herokuapp.com/api/UserServices/GetAllServicesNoKey")
    df = pd.DataFrame(json.loads(response.text))
    plt.figure(figsize=(10, 6))
    plt.bar(df.groupby(["serviceTitle"]).count().index, df.groupby(["serviceTitle"])["price"].count())
    plt.xticks(rotation=90)
    plt.title("Services Count")
    plt.savefig(tmpfile, format="png", bbox_inches="tight")
    return base64.b64encode(tmpfile.getvalue()).decode('utf-8')

def get_user_services_stats3():
    tmpfile = BytesIO()
    plt.tight_layout()
    response = requests.get("https://meistrelis.herokuapp.com/api/UserServices/GetAllServicesNoKey")
    df = pd.DataFrame(json.loads(response.text))
    df = df.drop_duplicates(subset=["mechanicPhone"])
    df["mechanicRating"] = df["mechanicRating"].round()
    plt.figure(figsize=(10, 6))
    plt.pie(df["mechanicRating"].unique(), labels=df["mechanicRating"].unique(), autopct='%1.1f%%',)
    plt.xticks(rotation=90)
    plt.title("Mechanics' rating distribution")
    plt.savefig(tmpfile, format="png", bbox_inches="tight")
    return base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    
def get_user_services_stats1():
    tmpfile = BytesIO()
    plt.tight_layout()
    response = requests.get("https://meistrelis.herokuapp.com/api/UserServices/GetAllServicesNoKey")
    df = pd.DataFrame(json.loads(response.text))
    plt.figure(figsize=(10, 6))
    plt.bar(df.groupby(["serviceTitle"]).count().index, df.groupby(["serviceTitle"])["price"].mean())
    plt.xticks(rotation=90)
    plt.title("Services Average Price")
    plt.savefig(tmpfile, format="png", bbox_inches="tight")
    return base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    
def get_user_services_stats2():
    tmpfile = BytesIO()
    plt.tight_layout()
    response = requests.get("https://meistrelis.herokuapp.com/api/UserServices/GetAllServicesNoKey")
    df = pd.DataFrame(json.loads(response.text))
    plt.figure(figsize=(10, 6))
    plt.pie(df.groupby(["serviceTitle"])["price"].count(), labels=df.groupby(["serviceTitle"])["price"].count().index, autopct='%1.1f%%',)
    plt.xticks(rotation=90)
    plt.title("Services Distrubution")
    plt.savefig(tmpfile, format="png", bbox_inches="tight")
    return base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    

IMG1 = get_user_services_stats()
IMG2 = get_user_services_stats1()
IMG3 = get_user_services_stats2()
IMG4 = get_user_services_stats3()
USERS_COUNT = get_unique_users_count()

html_string = '<!doctype html><html lang="en"><head><meta charset="utf-8"><style>' + '.title{font-size:2rem}.title-class{text-align:center;padding:3rem}.img{max-width:100%;max-height:100%}.imgs-row{padding:2rem}.usersText{text-align:center}.usersCount{font-size:4rem;color:blue}.usersText{font-size:1.5rem}</style>' + f'<meta name="viewport" content="width=device-width, initial-scale=1"><link href="./index.css", rel="stylesheet" /><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous"><title>Meistrelis Stats</title></head><body><div class="container"><div class="row"><div class="col title-class"><h1 class="title">MEISTRELIS STATS</h1></div></div></div><div class="container"><div class="row imgs-row"><div class="col"> <img src="data:image/png;base64,{IMG1}" class="img"/></div><div class="col"> <img src="data:image/png;base64,{IMG2}" class="img"/></div></div><div class="row imgs-row"><div class="col"> <img src="data:image/png;base64,{IMG3}" class="img"/></div><div class="col"> <img src="data:image/png;base64,{IMG4}" class="img"/></div></div><div class="row imgs-row"><div class="col usersText"><h1 class="usersCount">{USERS_COUNT}</h1><h1 class="usersText"> Unique Users</h1></div><div class="col"></div></div></div> <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script> </body></html>'

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    if request.method == "GET":
        return "OK", 200
    return "Not found", 404


@app.route("/stats", methods=["GET"])
def predict():
    if request.method == "GET":
        try:
           return html_string
        except:
            return "Server error", 500

    return "Not found", 404


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
