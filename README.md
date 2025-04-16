# TerraVest Website

TerraVest is a web application designed to empower users with sustainable investment tools. It provides AI-driven ESG (Environmental, Social, and Governance) analysis, real-time insights, and personalized investment recommendations.

## Features

- **Real-Time Insights**: Live sentiment analysis and dynamic ESG scores.
- **Transparent Reporting**: Clear and narrative explanations for informed decisions.
- **Custom Recommendations**: Tailored strategies to match unique investment goals.
- **Portfolio Management**: Manage your investments with detailed performance metrics.
- **ESG News Feed**: Stay updated with the latest ESG-related news.
- **User Preferences**: Customize your investment strategy and exclusions.

## Tech Stack

- **Frontend**: Vue 3, TypeScript, Vite
- **Backend**: Django
- **API**: Axios for HTTP requests
- **Styling**: Tailwind CSS, Scoped CSS
- **Database**: Django ORM
- **Authentication**: Django's built-in authentication system

## Project Structure

### Frontend

The frontend is located in the `frontend` directory and is built using Vue 3 with TypeScript and Vite.

#### Key Directories

- **`src/pages`**: Contains Vue components for individual pages like `MainPage.vue`, `PortfolioPage.vue`, etc.
- **`src/components`**: Reusable components like `Header.vue`, `Footer.vue`, `HoldingsTable.vue`, etc.
- **`src/assets`**: Static assets like images and icons.
- **`src/styles`**: Global and scoped styles.

#### Scripts

- `npm run dev`: Start the development server.
- `npm run build`: Build the project for production.
- `npm run preview`: Preview the production build.

### Backend

The backend is located in the `api` directory and is built using Django.

#### Key Files

- **`views.py`**: Contains API endpoints for user preferences, portfolio management, and more.
- **`models.py`**: Defines the database schema.
- **`urls.py`**: Maps URLs to views.
- **`templates`**: Contains HTML templates for the app.

#### Commands

- `python manage.py runserver`: Start the Django development server.
- `python manage.py migrate`: Apply database migrations.
- `python manage.py createsuperuser`: Create an admin user.

## Setup Instructions

### Prerequisites

- Node.js and npm
- Python 3.x and pip
- A virtual environment for Python (recommended)

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend