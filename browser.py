import decouple
import mechanicalsoup
from fake_useragent import UserAgent

from exceptions import LoginException

ROOT_URL = "https://intranet.hbtn.io/"


def intranet_login():
    browser = mechanicalsoup.StatefulBrowser(user_agent=UserAgent().random)
    try:
        user = decouple.config("INTRANET_USERNAME")
        password = decouple.config("INTRANET_PASSWORD")
        if not (
            isinstance(user, str)
            and isinstance(password, str)
            and len(user.strip()) > 0
            and len(password.strip()) > 0
        ):
            raise LoginException("Please provide user name and password for login")
    except decouple.UndefinedValueError as exc:
        raise LoginException("Please provide user name and password for login") from exc
    browser.open(f"{ROOT_URL}auth/sign_in")
    browser.select_form('form[method="post"]')
    browser["user[login]"] = user
    browser["user[password]"] = password
    browser.submit_selected()

    print("Successfully logged in to the Holberton's intranet!")
    return browser


def fill_new_job_form(browser, new_job_form_data):
    browser.open(f"{ROOT_URL}/user_working_statuses/new/")
    browser.select_form('form[action="/user_working_statuses"]')

    for key, value in new_job_form_data.items():
        browser[key] = value
    browser.submit_selected()
