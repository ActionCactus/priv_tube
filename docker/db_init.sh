echo "----- Checking for existing db"
if [ -f $DB_LOCATION ];
then
    echo "Database exists at ${DB_LOCATION}"
else
    echo "Database doesn't exist; creating at ${DB_LOCATION}."
    touch $DB_LOCATION
fi

echo "----- Running migrations"
python -m flask db upgrade --directory ./priv_tube/migrations

echo "----- Initializing db process"
/usr/bin/sqlite3 $DB_LOCATION