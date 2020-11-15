import os, re, sys, datetime, random
from flask import Flask, request, jsonify
import json, time
import requests, requests_toolbelt
from fnmatch import fnmatch
from unidecode import unidecode
import shutil
# ----------------------



ID_ADMIN = "2967189363337819"
ACCESS_TOKEN = "EAAMnENRUnygBAEJOSdZClbfUCZB0nBIvWjMpvb5LOfcvyhL12qd7tkr68k9ZCUsEBZCsTNAJykhjVmiehtZBrLWOtDrVFmtxcr9mGoGbCM7Wlsu6ztRZB1JP9muHN242H5NbB3hCmbAiRGkGK6pjd8Ef6dnHmrjzpkiT0rddKdv7XQVMrQa5FZBnnJa3fjiZAVIZD"
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





