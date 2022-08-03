#!/usr/bin/env python3

import requests


def register_user(email: str, password: str) -> None:
    """This function will register a user"""
    resp = requests.post('http://localhost:5000/users',
                         data={'email': email, 'password': password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """This function will log_in with wrong password"""
    resp = requests.post('http://localhost:5000/sessions',
                         data={'email': email, 'password': password})
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """This function will log in with proper credentials"""
    resp = requests.post('http://localhost:5000/sessions',
                         data={'email': email, 'password': password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    sess = resp.headers['Set-Cookie']
    session_id = sess.split(" ")[0].split("=")[1].split(";")[0]
    return session_id


def profile_unlogged() -> None:
    """This function will unlog a profile"""
    resp = requests.get('http://localhost:5000/')
    assert resp.status_code == 200
    assert resp.json() == {"message": "Bienvenue"}


def profile_logged(session_id: str) -> None:
    """This function will check profile with session_id"""
    resp = requests.get('http://localhost:5000/profile',
                        data={'session_id': session_id})
    json_response = resp.json()
    email = json_response['email']
    assert resp.status_code == 200
    assert resp.json() == {"email": email}


def log_out(session_id: str) -> None:
    """This function will logout"""
    resp = requests.delete('http://localhost:5000/sessions',
                           data={'session_id': session_id})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """This function will reset_password token"""
    resp = requests.post('http://localhost:5000/reset_password',
                         data={'email': email})
    json_response = resp.json()
    token = json_response['reset_token']
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "reset_token": token}
    return token


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """This function will update an existing password"""
    resp = requests.put('http://localhost:5000/reset_password',
                        data={'email': email,
                              'reset_token': reset_token,
                              'new_password': new_password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
