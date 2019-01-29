python manage.py migrate
echo "start_migration_done"
pause
python manage.py makemigrations
echo "migrations_created"
pause
python manage.py migrate
echo "migrations_done"
pause