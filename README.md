# Tasty_Truck_Treats
Project to create a pipeline using food truck data and analysing this information to create a dashboard and a revenue report.

This project downloads relevant data from AWS S3, transforms the data by removing invalid rows and loads this to Postgres using Python. The database is utilised to analyse trends in food truck data this is presented as a dashboard using Streamlit. Further, a report is produced to highlight key statistics. These stages are automated using AWS ECR, ECS, Scheduler, Step functions and Lambda. 

## Usage example

Can be used in analysing sales in different industries. The automation setup can be useful in sending breakdown reports to executives.

### Folders
 _please use the folders in this order as you will need to run pipeline prior to using dashboard and reports_
- pipeline -- this contains the scripts needed to run a pipeline from downloading to uploading to postgres
- dashboard -- scripts to create graphs representing data in the database using streamlit
- reports -- scripts to generate HTML string that will be displayed in emails as revenue reports. 

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
