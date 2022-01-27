echo "----- Running migrations"
cd priv_tube/cms/db
python -m flask db upgrade

echo "----- Initializing db process"
/usr/bin/sqlite3 app.db