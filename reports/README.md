# REPORTS
Project to create a pipeline using food truck data and analysing this information to create a dashboard and a revenue report.

The reports file uses python and SQL to create an HTML string that is then sent to AWS lambda and then to a step function to send a report to a selected email.

## Installation

```sh
`pip install -r requirements.txt`
```

## Development setup

For running the script locally -- this generates the html string
```sh
`python3 summary_script.py`
```
### Script files
  
- summary_queries_func.py -- contains the functions required for generating the HTML string.

In order to set up automated emails you must configure AWS Lambda, AWS step function, AWS SES and AWS scheduler.
