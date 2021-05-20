# Django Imports
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Standard Package Imports
import statistics
import os, io, urllib, base64, json

# Project Imports
from .models import *
from innovation import settings

# Third Party Imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


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

# This decorator exempts csrf token from the frontend
@csrf_exempt
def contact_form(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    # Extracting vars
    name = body['name']
    email = body['name']
    mobile = body['name']
    subject = body['name']
    message = body['name']
    mail_subject = 'Portfolio: New contact message'
    mail_body = render_to_string('mails/portfolio_contact_mail.html', {
        'name': name,
        'email': email,
        'mobile': mobile,
        'subject': subject,
        'message': message,
    })
    email = EmailMessage(
        mail_subject, mail_body, to=[
            'praneeth.kolanu.iitkgp@gmail.com', 'k.praneeth1199@gmail.com']
    )
    email.send()
    print("Sucess")
    data = {
        "message": "Request Recieved"
    }
    return JsonResponse(data)