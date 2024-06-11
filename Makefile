setup:
	docker-compose up -d --build
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py createsuperuser
	docker-compose exec web python auto_add_drugs.py
	docker-compose exec web python manage.py collectstatic --no-input

build:
	docker-compose build

run:
	docker-compose up

stop:
	docker-compose down

remove:
	docker-compose down --rmi all

rmall:
	docker system prune -a --volumes

web-logs:
	docker-compose logs -f web
