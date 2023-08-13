source .env
echo "clean up initiated"
export PGPASSWORD=$PASSWORD
psql --host $HOST --port $PORT -U $DB_USER $DB_NAME -c "DROP TABLE sigma_gawsalya_schema.dim_date, sigma_gawsalya_schema.dim_truck, sigma_gawsalya_schema.dim_type, sigma_gawsalya_schema.fact_truck_transaction CASCADE;"
psql --host $HOST --port $PORT -U $DB_USER $DB_NAME -c "\q"
echo "clean up complete"