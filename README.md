# Arba Travel - Wazeef

## Overview
This repository contains a fully containerized application, including a FastAPI backend, a Vue.js frontend, and a PostgreSQL database. The application is orchestrated using Docker Compose to streamline deployment and local development.

## Prerequisites
Ensure the following dependencies are installed before running the application:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation & Setup
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Run the application using Docker Compose:**
   ```sh
   docker-compose up --build
   ```
   
   This will pull the necessary images, build the containers, and start the services.

3. **Access the application:**
   - **Frontend:** Open [http://localhost:3000](http://localhost:3000) in your browser.
   - **Backend API:** Available at [http://localhost:8000](http://localhost:8000).
   - **Database:** Runs on port `5432` (PostgreSQL).

## Notes & Known Issues
> **⚠️ Disclaimer:** The system is still under review, and a few issues have been identified:
>
> 1. **Backend-Database Connection Delay:** The backend may attempt to connect to the database before it is fully initialized, leading to occasional failures. A retry mechanism or proper health checks are under consideration.
> 2. **Frontend Navigation Issue:** After a successful login, the frontend should reroute to the feed page but may require a manual refresh.
> 3. **Image Rendering Issue:** When updating a post, newly updated images may not render correctly. This is due to images being stored in PostgreSQL as `BYTEA`, requiring encoding to `Base64` before rendering.

## License
This project is licensed under [MIT License](LICENSE).

## Contributions
Contributions are welcome! If you identify any issues or have suggestions, feel free to open an issue or submit a pull request.

