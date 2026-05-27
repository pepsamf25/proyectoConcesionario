import decimal
import json
import bleach
import html
import secrets
from flask import session, has_request_context
import bcrypt
import os
import datetime
from werkzeug.http import http_date
from flask_wtf.csrf import generate_csrf as flask_generate_csrf

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def sanitize_field(data):
    if isinstance(data, str):
        return bleach.clean(html.escape(data))
    if isinstance(data, dict):
        return {k: sanitize_field(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_field(v) for v in data]
    return data

def prepare_response_extra_headers(include_security_headers):

    response_extra_headers = {
        # always
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Last-Modified': http_date(datetime.datetime.now()),
        'Server':''
    }
    if include_security_headers:
        response_security_headers = {
            # X-Frame-Options: page can only be shown in an iframe of the same site
            'X-Frame-Options': 'SAMEORIGIN',
            # ensure all app communication is sent over HTTPS
            'Strict-Transport-Security': 'max-age=63072000; includeSubdomains',
            # instructs the browser not to override the response content type
            'X-Content-Type-Options': 'nosniff',
            # enable browser cross-site scripting (XSS) filter
            'X-XSS-Protection': '1; mode=block'
        }
        response_extra_headers.update(response_security_headers)

    return response_extra_headers

def create_session(usuario,perfil):
    if has_request_context():
        session["usuario"] = usuario
        session["perfil"] = perfil


def delete_session():
    if has_request_context():
        session.clear()


def generate_csrf():
    try:
        return flask_generate_csrf()
    except Exception:
        return secrets.token_urlsafe(32)


def validar_session_normal():
    try:
        if session["usuario"] and session["usuario"] != "":
            return True
        else:
            return False
    except Exception:
        return False


def validar_session_admin():
    try:
        if (
            session["usuario"]
            and session["usuario"] != ""
            and session["perfil"] == "admin"
        ):
            return True
        else:
            return False
    except Exception:
        return False

def cipher_password(password):
    PEPPER_KEY = os.getenv("PASSWORD_PEPPER")  # Hay que pasar esta variable de entorno en docker-compose y kubernetes
    if PEPPER_KEY is None:
        PEPPER_KEY = ""

    password_peppered = password + PEPPER_KEY
    hashAndSalt = bcrypt.hashpw(password_peppered.encode("utf-8"), bcrypt.gensalt(10))
    return hashAndSalt.decode("utf-8")

def compare_password(password_hash,password):
    if password_hash is None:
        return False
    try:
        if isinstance(password_hash, str):
            password_hash = password_hash.encode("utf-8")
        PEPPER_KEY = os.getenv("PASSWORD_PEPPER")
        if PEPPER_KEY is None:
            PEPPER_KEY = ""

        password_peppered = password + PEPPER_KEY

        return bcrypt.checkpw(password_peppered.encode("utf-8"),password_hash)
    except:
        return False

def prepare_response_extra_headers(include_security_headers):

    response_extra_headers = {
        # always
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Last-Modified': http_date(datetime.datetime.now()),
        'Server':''
    }
    
    if include_security_headers:
        response_security_headers = {
            # X-Frame-Options: page can only be shown in an iframe of the same site
            'X-Frame-Options': 'SAMEORIGIN',
            # ensure all app communication is sent over HTTPS
            'Strict-Transport-Security': 'max-age=63072000; includeSubdomains',
            # instructs the browser not to override the response content type
            'X-Content-Type-Options': 'nosniff',
            # enable browser cross-site scripting (XSS) filter
            'X-XSS-Protection': '1; mode=block'
        }
        response_extra_headers.update(response_security_headers)

    return response_extra_headers