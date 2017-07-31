from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.
import sqlite3


class DBHelper:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS swapdesc (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text):
        stmt = "INSERT INTO swapdesc (description) VALUES (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM swapdesc WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM swapdesc"
        return [x[0] for x in self.conn.execute(stmt)]

class SwapContract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    swap_name = models.CharField(max_length=100)
    swap_type = models.CharField(max_length=100)
    margin_money = models.IntegerField()
    contract_flag = models.IntegerField(default=0)
    contract_accept = models.IntegerField(default=0)
    contract_add_user_id = models.IntegerField(default=0)

    def __str__(self):
        return self.swap_name


class SwapIntermediate(models.Model):
    user_temp = models.ForeignKey(User, on_delete=models.CASCADE)
    swap_name_temp = models.CharField(max_length=100)
    swap_type_temp = models.CharField(max_length=100)
    margin_money_temp = models.IntegerField()

    def __str__(self):
        return self.swap_name_temp

currency_choice = (('USD', 'USD'), ('GBR', 'GBR'), ('JYP', 'JYP'))


class SwapDetails(models.Model):
    swap_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    swap_name = models.CharField(max_length=500)
    swap_sector = models.CharField(max_length=200)
    swap_counter_party = models.IntegerField(default=0)
    swap_margin = models.IntegerField()
    swap_base_curr = models.CharField(max_length=50, choices=currency_choice, default=None)
    swap_trade_curr = models.CharField(max_length=50, blank=True, choices=currency_choice)
    swap_status_request = models.IntegerField(default=0)
    swap_status_accept = models.IntegerField(default=0)
    swap_start_date = models.DateField()
    swap_end_date = models.DateField()

    def __str__(self):
        return self.swap_owner


class Currencies(models.Model):
    currency_name = models.CharField(max_length=20)