import os, re, sys, datetime, random
from flask import Flask, request, jsonify
import json, time
import requests, requests_toolbelt
from fnmatch import fnmatch
from unidecode import unidecode
import shutil
# ----------------------



ID_ADMIN = "2967189363337819"
ACCESS_TOKEN = "EAAHi2ZAwSZAqABALGMKoNZAxHMyF0OTejkknbsMHWkaZCX0hMhByquRgRHkVLCZBk0FGspa0AV7HRUpdXvnVfpHKFZAKkeBZAGVZBo87TrtdsNaAcv2QGZCtEnVBXHOM9aZAtdGyZAEs8W5NLwVunYWl3epo7Am1LJ8QbhUvBZBWRDcZAgQZDZD"
VERIFY_TOKEN = 'jedeconne'
 
 
def decode_url(url_encode):
    if url_encode.startswith('http'):
        return url_encode
    url = ''
    for u in url_encode.split('-'):
        url = url + chr(int(u))
    return url


def encode_url(url):
    url_encode = ''
    for u in url:
        url_encode = url_encode + str(ord(u)) + '-'
    return url_encode[:-1]


def database(**kwargs):
    return {
        'host' : 'gaetanbot.xyz',
        'user' : 'bot',
        'password' : '__bot__',
        'db' : 'BOT'
    }


def monitor(id, what):
    """
        Fonction pour incrementer le nombre d'utilisation par jour

        defini dans le fichier gaetanbot, car besoin d etre utiliser ici aussi
    """
    db = mysql.connector.connect(**database())
    cursor = db.cursor()

    cursor.execute("SELECT 1 FROM Monitoring WHERE id_user=%s AND date=CURDATE()", (id,))
    dump_ = cursor.fetchall()
    if len(dump_)==0:
        cursor.execute("INSERT INTO Monitoring(id_user) VALUES(%s)", (id,))
        db.commit()
    try:
        cursor.execute(f"UPDATE Monitoring SET {what}={what}+1 WHERE id_user=%s AND date=CURDATE()", (id, ))
    except Exception as err:
        print(err)
        db.rollback()
    else:
        db.commit()


def check_module_pornhub(id):
    db = mysql.connector.connect(**database())
    cursor = db.cursor()

    cursor.execute("""
        SELECT 1 FROM User
        WHERE id_user=%s AND pornhub=True
    """, (id,))

    return len(cursor.fetchall())>0


def check_account(id):
    db = mysql.connector.connect(**database())
    cursor = db.cursor()

    cursor.execute("SELECT auth, exp FROM User where id_user=%s", (id, ))
    data = cursor.fetchall()

    if data[0][0]:
        if data[0][1] <= datetime.date.today():
            return "Désolé, Votre abonnement est epuisé"
        elif abs((datetime.date.today() - data[0][1]).days) == 1:
            return "Attention, Votre abonnement sera epuisé demain"
    else:
        return False
    
    return True
