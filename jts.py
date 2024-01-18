import decouple
import pandas as pd
import requests
from openpyxl import load_workbook
from pandas import DataFrame

import browser
from exceptions import FileNotExpectedError

MANDATORY_FIELDS = [
    "Date_Saved",
    "Employment_Options",
    "Work_Type",
    "Company",
    "Location",
    "Work_Type",
]
GOOGLE_PLACES_API_HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": decouple.config("GOOGLE_PLACES_API_KEY"),
    "X-Goog-FieldMask": "places.formattedAddress,places.addressComponents,places.location",
}


def check_nan(row, field):
    """Check if a dataframe value is NaN and return a tuple with the result and the field name."""
    return pd.isna(getattr(row, field)), field


def read_job_tracking_system(file_path):
    try:
        job_tracking_system: DataFrame = pd.read_excel(
            file_path,
            dtype={
                "Date_Saved": "datetime64[ns]",
                "Job_Position": "str",
                "Company": "str",
                "Work_Type": "str",
                "Employment_Options": "str",
                "Min_Salary": "float64",
                "Max_Salary": "float64",
                "Currency": "str",
                "Frequency": "str",
                "Location": "str",
                "Status": "str",
                "Excitement": "int8",
                "Last_Updated": "datetime64[ns]",
                "Uploaded": "str",
            },
        )
    except pd.errors.ParserError:
        raise FileNotExpectedError("Wrong format for files")

    print("Job Tracking System successfully loaded!")
    return job_tracking_system


def save_job_status_on_job_tracking_system(job_tracking_system, file_path):
    book = load_workbook(file_path)
    ws = book["Job Search Tracker"]
    start_cell = ws["A2"]

    for row in job_tracking_system.itertuples():
        for col_idx, value in enumerate(row[1:]):
            ws.cell(
                row=start_cell.row,
                column=start_cell.column + col_idx,
                value=value,
            )
        start_cell = ws.cell(row=start_cell.row + 1, column=start_cell.column)

    book.save(file_path)
    book.close()

    print("Job Tracking System successfully updated!")


def fill_form_data(row):
    results = [check_nan(row, field) for field in MANDATORY_FIELDS]
    if any(result[0] for result in results):
        print(
            f"No data in row {row.Index}. Missing data in columns:",
            ",".join([f"{result[1]}" for result in results if result[0]]),
            "- Can't save form entry with incomplete data",
        )
        print(f"  Row data for debugging in your Job Tracking System: {row._asdict()}")
        return

    if not check_nan(row, "Uploaded")[0]:
        print(f"Job {row.Job_Position} from company {row.Company} already uploaded!")
        return

    google_places_api_data = {"textQuery": row.Location}
    response = requests.post(
        url="https://places.googleapis.com/v1/places:searchText",
        json=google_places_api_data,
        headers=GOOGLE_PLACES_API_HEADERS,
    )
    parsed_response = response.json()
    place = parsed_response["places"][0]

    components = {}
    for component in place["addressComponents"]:
        for type in component["types"]:
            components[type] = component["shortText"]
    location_lat = place["location"]["latitude"]
    location_lng = place["location"]["longitude"]
    location_city = components.get("locality")
    location_state = components.get("administrative_area_level_1")
    location_country = components.get("country")

    end_date_year = ""
    end_date_month = ""
    end_date_day = ""
    if not pd.isna(row.Last_Updated) and row.Status in ["Resigned", "Laid off"]:
        end_date_year = row.Last_Updated.year
        end_date_month = row.Last_Updated.month
        end_date_day = row.Last_Updated.day

    salary = row.Min_Salary if not pd.isna(row.Min_Salary) else ""
    salary_currency = row.Currency if not pd.isna(row.Currency) else ""
    salary_frequency = row.Frequency if not pd.isna(row.Frequency) else ""

    form_data = {
        "user_working_status[start_date(1i)]": row.Date_Saved.year,
        "user_working_status[start_date(2i)]": row.Date_Saved.month,
        "user_working_status[start_date(3i)]": row.Date_Saved.day,
        "user_working_status[end_date(1i)]": end_date_year,
        "user_working_status[end_date(2i)]": end_date_month,
        "user_working_status[end_date(3i)]": end_date_day,
        "user_working_status[employment]": row.Employment_Options,
        "user_working_status[work_type]": row.Work_Type,
        "user_working_status[company_name]": row.Company,
        "user_working_status[location_city]": location_city,
        "user_working_status[location_state]": location_state,
        "user_working_status[location_country]": location_country,
        "user_working_status[location_lat]": location_lat,
        "user_working_status[location_lng]": location_lng,
        "user_working_status[title]": row.Job_Position,
        "user_working_status[salary]": salary,
        "user_working_status[salary_currency]": salary_currency,
        "user_working_status[salary_frequency]": salary_frequency,
    }
    return form_data


def upload_jobs(job_tracking_system, intranet):
    print("Uploading new jobs...")
    jobs_total = len(job_tracking_system)
    jobs_uploaded = 0
    for job in job_tracking_system.itertuples():
        new_job_form_data = fill_form_data(job)
        if new_job_form_data is None:
            continue
        browser.fill_new_job_form(intranet, new_job_form_data)
        job_tracking_system.at[job.Index, "Uploaded"] = "Yes"
        jobs_uploaded += 1
        print(
            f"Job {job.Job_Position} from company {job.Company} successfully uploaded"
        )

    print(f"{jobs_uploaded} of {jobs_total} jobs successfully uploaded!")
