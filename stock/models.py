from django.db import models
import pandas as pd


# Custom ModelFields here

# Create your models here.
class Stock(models.Model):
    '''def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.dataset = pd.read_csv(
            filename,
            index_col='Date',
            parse_dates = True,
            keep_date_col = True
        )
        self.returns = (
            (self.dataset["Close Price"]
             - self.dataset["Prev Close"])*100/self.dataset["Prev Close"]
        )
        self.mean_return = statistics.mean(self.returns)
        self.return_standard_deviation = statistics.stdev(self.returns)'''
    name = models.CharField(max_length=50)
    file = models.FileField()
    def __str__(self):
        return self.name