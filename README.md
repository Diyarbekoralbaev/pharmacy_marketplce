# Pharmacy Marketplace
## Description
This is a pharmacy marketplace where users can buy and sell drugs. The application is built using Django and Django Rest Framework.
## Features
- Users can register and login in 3 roles: `admin`, `seller`, `buyer`
- Admin can add, update, delete drugs
- Seller can add, update, delete drugs
- Buyer can view drugs and buy drugs
- Buyer can view order history
- Buyer can view order details
- Buyer can cancel order

## Technologies
- Django
- Django Rest Framework
- Docker
- Docker Compose
- Django Rest Framework Simple JWT
- drf-yasg
- Redis
- Django Cors Headers

## Installation
1. Clone the repository
```bash
git clone https://github.com//Diyarbekoralbaev/Pharmacy-Marketplace.git
```
2. Change directory
```bash
cd Pharmacy-Marketplace
```
3. Run the application
```bash
docker-compose up --build
```
4. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```
5. Access the application at `http://localhost:8000`
6. Access the admin panel at `http://localhost:8000/admin`
7. Access the Swagger documentation at `http://localhost:8000/swagger`
8. Access the Redoc documentation at `http://localhost:8000/redoc`

## API Endpoints
### Users
- GET `/users/` - Get all users
- POST `/users/signup/` - Register user
- POST `/users/login/` - Login user
- GET `/users/me/` - Get current user
- PUT `/users/me/` - Update current user
- POST `/users/change-password/` - Change password (current user)
- POST `/users/forgot-password/` - Forgot password (send email)
- POST `/users/reset-password/` - Reset password (via otp code sent to email)
- GET `/users/{id}/` - Get user by id
- PUT `/users/{id}/` - Update user by id
- DELETE `/users/{id}/` - Delete user by id

### Drugs
- GET `/drugs/` - Get all drugs
- POST `/drugs/create/` - Create drug
- GET `/drugs/{id}/` - Get drug by id
- PUT `/drugs/update/{id}/` - Update drug by id
- DELETE `/drugs/delete/{id}/` - Delete drug by id
- GET `/drugs/categories/` - Get all drug categories
- GET `/drugs/my_drugs/` - Get all drugs created by current user

### Orders
- GET `/users/orders/` - Get all orders created by current user
- POST `/users/orders/` - Create order
- GET `/users/orders/{id}/` - Get order by id
- PUT `/users/orders/{id}/` - Update order by id
- DELETE `/users/orders/{id}/` - Delete order by id
- POST `/users/orders/items/` - Delete item from order

## License
This project is open-sourced software licensed under the [MIT license](https://github.com//Diyarbekoralbaev/Pharmacy-Marketplace/blob/main/LICENSE).

## Author
- [Diyarbek Oralbaev](https://github.com//Diyarbekoralbaev/)
- [Email](mailto:diyarbekdev@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/diyarbek-oralbaev-66a020316/)
- [Telegram](https://t.me/Diyarbek_Dev)

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Django Rest Framework Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/)
- [Redis](https://redis.io/)
- [Django Cors Headers](https://pypi.org/project/django-cors-headers/)

## Support
For support, contact me from the links provided above.

# Thank you for using Pharmacy Marketplace!