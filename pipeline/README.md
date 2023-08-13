# Tasty_Truck_Treats
Project to create a pipeline using food truck data and analysing this information to create a dashboard and a revenue report.

This project downloads relevant data from AWS S3, transforms the data by removing invalid rows and loads this to Postgres using Python. The database is utilised to analyse trends in food truck data this is presented as a dashboard using Streamlit. Further, a report is produced to highlight key statistics. These stages are automated using AWS ECR, ECS, Scheduler, Step functions and Lambda. 

## Installation

```sh
`pip install -r requirements.txt`
```

## Usage example

Can be used in analysing sales in different industries. The automation setup can be useful in sending breakdown reports to executives.

## Development setup

For running the script locally
```sh
`python3 main.py`
```
For visualisation of graphs:
```sh
`streamlit run graphs.py`
```

For testing the function
```sh
`pytest test_functions_for_etl.py`
```
### Script files

- main.py -- python script containing the main script to run
  `python3 main.py`
  
- clean_database.sh -- contains the script to clear the database out
  `bash clean_database.sh`
  
- functions_for_etl.py -- contains the functions required for extract, transform and load in the main.py script
- charts.ipynb -- jupyter notebook containing a few examples of graphs that are made using seaborn and pandas

### Testing files

- test_functions_for_etl.py -- tests the functions for etl work properly
- conftest.py -- contains the required pytest fixtures.

### Datafile

- combined.csv -- combined transaction file that has been cleared of invalid results, timezone information have been removed from the timestamp as in this project as we are not concerned with particular times but the schedule as humans will continue to eat at set time range.
- schema.sql -- contains the SQL schema needed to create tables in the database
- requirements.txt -- contains necessary libraries to carry out script

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
