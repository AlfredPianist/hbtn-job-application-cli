<h1 align="center">
  Holberton Work Status CLI
</h1>

<h4 align="center">A simple job uploader to the Holberton intranet</h4>

<p align="center">
  <a href="#what-is-this">What Is This</a> •
  <a href="#how-to-use-it">How To Use It</a> •
  <a href="#future-features">Future Features</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## What Is This

This is a small project made with Python that lets you upload from an Excel file (sample Excel provided on this repository) all the job applications you're tracking to the Holberton's Working Statuses page, effectively bypassing filling the form.

I created this because I don't see myself filling 30 times the same form per month minimum (no one in my opinion, if you ask me. Do you like filling forms? Really?). This as per requirements to continue on the Career Development program on Holberton School Colombia.

## How To Use It

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/AlfredPianist/hbtn-work-status-cli

# Go into the repository
$ cd hbtn-work-status-cli

# Install dependencies
$ pip install -r requirements.txt

# Create a copy of .env.example and fill in the env variables
$ cp .env.example .env
$ vim .env # Or use your favorite text editor for that

# Create a copy of the sample Job Tracking System
$ cp Job_Tracking_System.xlsx Name_Of_Job_Tracking_System.xlsx

# Fill in your Job Tracking System and run the cli
$ ./cli.py Name_Of_Job_Tracking_System.xlsx
```

It is **highly** advisable to use [pyenv](https://github.com/pyenv/pyenv) or similar Python version managers. This to not bloat your system Python with lots of unnecesary dependencies.

Regarding the actual Job Tracking System, this repository provides a sample Job Tracking System in Excel. Use it or make a copy of it.

If you wish to customize your Job Tracking System to your needs, keep in mind that there are some mandatory fields that need to exist in order to successfully upload your job application. They are the following:

- Date_Saved
- Employment_Options
- Work_Type
- Company
- Location
- Work_Type

If you modify these headers from the Job Tracking System, the software will error out. Mind you, they are mandatory. They can't be empty.

Also, please don't modify the "Uploaded" column. This column will be used to verify if the job was already uploaded or not, given that the project currently doesn't track the already uploaded job applications. 

Lastly, to fully utilize this system, you will need to [create a Google Places API key](https://console.cloud.google.com/google/maps-apis/start) for the location, since Holberton uses that to autocomplete the job location. You have to enter your credit card to obtain the API key.

Google will charge you roughly USD $3.00 (assuming you'll upload maximum 200 jobs, which I doubt you'll go that far with your job search). But, as of today (2024-01-18), Google has a monthly free USD $200 credit that applies for the Places API. This means, Google won't charge you for this. If you have any questions, check out the pricing for Google Maps API [here](https://mapsplatform.google.com/pricing/) and [here](https://developers.google.com/maps/billing-and-pricing/billing).

## Future Features

There are some ideas about how to expand this with future features. But this depends on community demand. Here are some examples:

- Mirror jobs from the Intranet to the Job Tracking System.
- Editing and deleting jobs from within the Job Tracking System and sync them to the Intranet.
- Upload attachments on existing jobs from the Job Tracking System.

## Credits

This software uses the following open source packages:

- [Requests](https://docs.python-requests.org/en/latest/index.html)
- [MechanicalSoup](https://mechanicalsoup.readthedocs.io/en/stable/)
- [Pandas](https://pandas.pydata.org/)
- [fake-useragent](https://github.com/fake-useragent/fake-useragent)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/index.html)
- [Python Decouple](https://github.com/HBNetwork/python-decouple)

## License

GPL-3.0 license

---

> GitHub [@alfredpianist](https://github.com/AlfredPianist/) &nbsp;&middot;&nbsp;
> LinkedIn [@alfredo-delgado-moreno](https://www.linkedin.com/in/alfredo-delgado-moreno)
