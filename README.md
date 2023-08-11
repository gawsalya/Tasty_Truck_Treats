# Tasty_Truck_Treats
Project to create a pipeline using food truck data and analysing this information to create a dashboard and a revenue report.

One to two paragraph statement about your product and what it does.

## Installation

```sh
`pip install -r requirements.txt`
```

## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
`pip install -r requirements.txt`
`python3 main.py`
`pytest test_functions_for_etl.py`
```
### SCRIPT FILES

- main.py -- python script containing the main script to run
  `python3 main.py`
  
- clean_database.sh -- contains the script to clear the database out
  `bash clean_database.sh`
  
- functions_for_etl.py -- contains the functions required for extract, transform and load in the main.py script
- charts.ipynb -- jupyter notebook containing a few examples of graphs that are made using seaborn and pandas

### TESTING FILES

- test_functions_for_etl.py -- tests the functions for etl work properly
- conftest.py -- contains the required pytest fixtures.

### DATA FILES
- combined.csv -- combined transaction file that has been cleared of invalid results, timezone information have been removed from the timestamp as in this project as we are not concerned with particular times but the schedule as humans will continue to eat at set time range.
- schema.sql -- contains the SQL schema needed to create tables in the database
- requirements.txt -- contains necessary libraries to carry out script

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
