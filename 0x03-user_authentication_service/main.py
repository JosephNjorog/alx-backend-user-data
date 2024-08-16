#!/usr/bin/env python3
"""Integration test for app.py
"""
import requests


BASE_URL = "http://0.0.0.0:5000{endpoint}"


def register_user(email: str, password: str) -> None:
    """Test user registration
    """
    response = requests.post(BASE_URL.format(endpoint="/users"),
                             data={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password
    """
    response = requests.post(BASE_URL.format(endpoint="/sessions"),
                             data={"email": email, "password": password})
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Test login to protected profile route
    without loggin-in
    """
    response_1 = requests.get(BASE_URL.format(endpoint="/profile"))
    assert response_1.status_code == 403
    response_2 = requests.get(BASE_URL.format(endpoint="/profile"),
                              cookies={"session_id": "123"})
    assert response_2.status_code == 403


def log_in(email: str, password: str) -> str:
    """Test login
    """
    response = requests.post(BASE_URL.format(endpoint="/sessions"),
                             data={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data == {"email": email, "message": "logged in"}
    session_id = response.cookies.get("session_id")
    assert (session_id is not None) and (type(session_id) == str)
    return session_id


def profile_logged(session_id: str) -> None:
    """Test protected route while logged in
    """
    response = requests.get(BASE_URL.format(endpoint="/profile"),
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    data = response.json()
    assert type(data) == dict
    assert "email" in data


def log_out(session_id: str) -> None:
    """Test log out
    """
    response = requests.delete(BASE_URL.format(endpoint="/sessions"),
                               cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.url == BASE_URL.format(endpoint="/")
    data = response.json()
    assert data == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test reset password with token
    """
    response = requests.post(BASE_URL.format(endpoint="/reset_password"),
                             data={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert type(data) == dict
    assert data.get("email") == email
    reset_token = data.get("reset_token")
    assert (reset_token is not None) and (type(reset_token) == str)
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating password with reset token
    """
    response = requests.put(BASE_URL.format(endpoint="/reset_password"),
                            data={
                                "email": email,
                                "reset_token": reset_token,
                                "new_password": new_password})
    assert response.status_code == 200
    data = response.json()
    assert data == {"email": email, "message": "Password updated"}


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
