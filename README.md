# LunchApp

LunchApp is a Django REST Framework-based web application designed to help employees choose where to have lunch. It provides an internal API for managing restaurants, menus, and a voting system to decide on the best lunch option for the day.

## Technologies Used

- **Python 3.13**
- **Django 6.0**
- **Django REST Framework**
- **PostgreSQL 16**
- **Docker & Docker Compose**
- **Pytest**

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Setup

1. **Build and start the containers**:
   ```bash
   docker compose up --build
   ```
   - The application will be available at `http://localhost:8000`.

2. **Run Migrations**:

   ```bash
   docker compose exec web python manage.py migrate
   ```

## API Endpoints

### Authentication
- `POST /api/token/`: Obtain JWT token pair (access and refresh).
- `POST /api/token/refresh/`: Refresh the access token.

### Employees
- `POST /api/employees/`: Register a new employee.

### Restaurants & Menus
- `GET | POST /api/restaurants/`: List all restaurants or create a new one.
- `POST /api/restaurants/menus/`: Create a new menu for a restaurant.
- `GET /api/restaurants/menus/today/`: Get all menus available for today.

### Voting
- `POST /api/voting/vote/`: Cast a vote for a specific menu.
- `GET /api/voting/results/today/`: View today's voting results.

## Running Tests

To run the automated tests using `pytest`:

```bash
docker compose exec web pytest
```

## Project Structure

- `employees/`: Employee registration and management logic.
- `restaurants/`: Restaurant and menu management logic.
- `voting/`: Voting system logic and results tracking.
- `myproject/`: Project configuration and settings.
- `tests/`: Integration and unit tests.
- `compose.yaml`: Docker Compose configuration.
- `Dockerfile`: Container definition for the web application.

## Admin Interface

You can access the Django Admin interface at `http://localhost:8000/admin/`
- Username: admin
- Password: 12345
