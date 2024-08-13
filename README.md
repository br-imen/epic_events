# Epic Events CLI

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Database Setup and Migrations](#database-setup-and-migrations)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
Epic Events is a command-line interface (CLI) application designed to manage clients, contracts, and events efficiently. The application is built using Python, with Click for the CLI, SQLAlchemy for ORM, and Alembic for managing database migrations. This tool is ideal for users who need to interact with their event management system directly from the terminal.

## Features
- Client Management: Create, update, list, and delete clients.
- Contract Management: Manage contracts associated with clients and events.
- Event Management: Organize and schedule events efficiently.
- User Authentication: Secure login and role-based access control.
- Command-Line Interface: Intuitive commands to interact with the application.

## Technologies Used
- Programming Language: Python
- CLI Framework: Click
- Database: SQLite (configurable to PostgreSQL/MySQL)
- ORM: SQLAlchemy
- Migrations: Alembic
- Testing: pytest

## Installation
To install and set up the Epic Events CLI application on your local machine, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/br-imen/epic_events.git
    cd epic_events
    ```

2. Set up a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database 
    

5. Run the CLI application:

    ```bash
    python epic_events.py
    ```

## Usage
Epic Events CLI allows you to manage event-related data via simple commands. All operations, including client, contract, and event management, are performed through the CLI.

To see the list of available commands, simply run:

```bash
python epic_events.py --help
```

## Commands
Below is a list of the primary commands available in the Epic Events CLI:

- Client Commands:

        add-client: Add a new client.
        update-client: Update existing client information.
        list-clients: List all clients.
        delete-client: Delete a client.
- Contract Commands:

        add-contract: Create a new contract.
        update-contract: Update an existing contract.
        list-contracts: List all contracts.
        delete-contract: Delete a contract.
- Event Commands:

        add-event: Schedule a new event.
        update-event: Update event details.
        list-events: List all events.
        delete-event: Delete an event.

- Authentication Commands:

        login: Log in to the system with your credentials.


## Testing
The project includes tests to ensure that the CLI functions as expected. To run the tests, use the following command:

```bash
pytest
```

## Code coverage
```bash
pytest --cov
```

Make sure your virtual environment is activated and that all dependencies are installed before running the tests.