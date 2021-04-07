# Django Imports
from django.shortcuts import render
from django.http import HttpResponse

# Standard Package Imports
import statistics
import os, io, urllib, base64

# Project Imports
from .models import *

# Third Party Imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from innovation import settings


abpath = str(settings.BASE_DIR)

# Create your views here.


def risk_return(request):
    stocks = Stock.objects.all()
    for stock in stocks:
        stock.dataset = pd.read_csv(
            abpath + stock.file.url,
            index_col='Date',
            parse_dates=True,
            keep_date_col=True
        )
        stock.returns = (
            (stock.dataset["Close Price"]
             - stock.dataset["Prev Close"])*100/stock.dataset["Prev Close"]
        )
        stock.mean_return = statistics.mean(stock.returns)
        stock.return_standard_deviation = statistics.stdev(stock.returns)
    for stock in stocks:
        print(stock.name)
        print(stock.mean_return, stock.return_standard_deviation, '\n\n')
    plt.figure(figsize=(8, 6))
    plt.scatter(
        np.array([stock.return_standard_deviation for stock in stocks]),
        np.array([stock.mean_return for stock in stocks]),
        s=40,
        color="red",
        marker="s"
    )
    plt.xlabel("Standard Deviation of day-wise percentage return")
    plt.ylabel("Mean Day-wise Return %")
    plt.title("Daily Risk Return Characteristics of stocks", fontsize=15)
    for stock in stocks:
        plt.annotate(
            stock.name,
            (stock.return_standard_deviation, stock.mean_return)
        )
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
    # plt.show()
    return render(request, "risk_return.html", {"data":url})
