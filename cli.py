#!/usr/bin/env python

import argparse
import pathlib

import browser
import jts

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file_path", type=pathlib.Path, help="Job Tracking System Excel file path"
    )
    args = parser.parse_args()

    file_path = pathlib.Path(args.file_path)

    job_tracking_system, job_tracking_system_notes = jts.read_job_tracking_system(
        file_path
    )
    intranet = browser.intranet_login()
    jts.process_jobs(job_tracking_system, job_tracking_system_notes, intranet)
    jts.save_job_status_on_job_tracking_system(
        job_tracking_system, job_tracking_system_notes, file_path
    )
