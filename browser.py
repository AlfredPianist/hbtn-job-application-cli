import re

import decouple
from playwright.sync_api import sync_playwright

from exceptions import LoginException

ROOT_URL = "https://intranet.hbtn.io/"


def intranet_login():
    """
    Login to the intranet and return a Playwright page instance to navigate.
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
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
    page.goto(f"{ROOT_URL}auth/sign_in")
    page.locator("#user_login").fill(user)
    page.locator("#user_password").fill(password)
    page.locator("//input[@type='submit']").click()

    print("Successfully logged in to the Holberton's intranet!")
    return page


def create_job_status(page, job, job_form_data, job_notes):
    """
    Creates a new job on the intranet.
    """
    if page.url != f"{ROOT_URL}/user_working_statuses/new/":
        page.goto(f"{ROOT_URL}/user_working_statuses/new/")

    job_id = fill_job_form(page, job_form_data, job_notes, "Create")
    if job_id is None:
        print(f"Job {job.Job_Position} from company {job.Company} upload unsuccessful!")
    else:
        print(
            f"Job {job.Job_Position} from company {job.Company} successfully uploaded!"
        )
    return job_id


def edit_job_status(page, job, job_form_data, job_notes):
    """
    Edits an existing job on the intranet.
    """
    if page.url != f"{ROOT_URL}/user_working_statuses/{job.Hbtn_Job_ID}/edit":
        page.goto(f"{ROOT_URL}/user_working_statuses/{job.Hbtn_Job_ID}/edit/")

    fill_job_form(page, job_form_data, job_notes, "Edit")
    print(f"Job {job.Job_Position} from company {job.Company} successfully updated!")


def delete_job_status(page, job):
    """
    Deletes an existing job from the intranet.
    """
    page.goto(f"{ROOT_URL}/user_working_statuses/{job.Hbtn_Job_ID}")
    if page.url.split("/")[-1] != str(job.Hbtn_Job_ID):
        print(f"Job {job.Job_Position} from company {job.Company} doesn't exist!")
        return
    page.locator("//a[@data-method='delete']").click()
    print(f"Job {job.Job_Position} from company {job.Company} deleted successfully!")


def fill_job_form(page, job_form_data, job_notes, type):
    """
    Fills the complete job form with the information from the Job Tracking System.
    """
    for key, value in job_form_data.items():
        if key in [
            "#company_name",
            "#title",
            "#user_working_status_salary",
        ]:
            page.locator(key).fill(value)
        elif "location" in key:
            page.evaluate(
                f"""() => {{
                document.querySelector("{key}").value = '{value}';
            }}"""
            )
        else:
            page.locator(key).select_option(value)

    if type == "Create":
        page.locator(
            "//input[@type='submit' and @value='Create User working status']"
        ).click()
        page.wait_for_url(re.compile(".*\d+$"))
        url_components = [
            component for component in page.url.split("/") if component != ""
        ]
        job_id = int(url_components[-1])

    elif type == "Edit":
        url_components = [
            component for component in page.url.split("/") if component != ""
        ]
        job_id = int(url_components[-2])

    if job_notes is not None:
        fill_notes_form(page, job_notes, job_id)
        page.locator(
            "//input[@type='submit' and @value='Update User working status']"
        ).click()

    return job_id


def fill_notes_form(page, job_notes, job_id):
    """
    Upload the notes linked to the job application.
    """
    if page.url != f"{ROOT_URL}/user_working_statuses/{job_id}/edit/":
        page.goto(f"{ROOT_URL}/user_working_statuses/{job_id}/edit/")

    total_notes = job_notes.shape[0]
    for note in range(total_notes):
        page.locator("//a[text()='+ add a new note']").click()

    md_editors = page.locator(".CodeMirror").all()
    for note, editor in zip(job_notes.itertuples(), md_editors):
        editor.click()
        editor.type(note.Note)
