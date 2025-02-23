**Docker Commands**
docker-compose up --build
docker-compose stop
docker-compose down / docker-compose down -v

**Executing Commands**
1. Run the migrations: 
    docker-compose exec web python manage.py migrate
2. Run the collectstatic: 
    docker-compose exec web python manage.py collectstatic
3. Create Superuser: 
    docker-compose exec web python manage.py createsuperuser
