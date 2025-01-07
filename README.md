# Alisam Cafe CLI Ordering System

A professional and fully-featured CLI-based order management system designed for efficiency and scalability. This project showcases advanced Python programming, error handling, and database interaction using PostgreSQL.

## Features

### Product Management
- **View Products**: Displays product ID, name, price, and quantity available.
- **Create Product**: Easily add new products with relevant details.
- **Update Product**: Flexible updates allowing modification of specific fields (e.g., name, price).
- **Delete Product**: Remove products with error handling for non-existent IDs.

### Order Management
- **View Open Orders**: Lists order details, including customer information, ordered items, status, and assigned courier.
- **Create Order**:
  - Input customer details and order items.
  - Validates item availability and sufficient stock.
  - Ensures a courier exists before order creation.
  - Checks if customer is registered in database, otherwise creates new account for them.
  - Automatically calculates total price and updates the customer’s total lifetime spend.
  - Assigns the courier with the lowest open orders for balanced workload.
- **Update Order Status**: Modify order statuses between Preparing, Ready, Collected, and Abandoned.
- **Filter Orders by Status**: Quickly view orders grouped by their current status.

### Courier Management
- **View Couriers**: List all active couriers.
- **Add Courier**: Register new couriers.
- **Delete Courier**: Remove couriers from the system.
- **View Courier Assignments**: Check orders currently assigned to a specific courier by ID.

### Customer Management
- **View Customers**: Displays customer records including name, phone, email, address, and total spend.
- **Add Customer**: Manually add customer data, with automatic creation during order placement if the customer doesn't already exist.
- **Update Customer**: Modify any customer details as needed.
- **Delete Customer**: Remove a customer record.

### Data Export
- **CSV Export**: Export all PostgreSQL database tables (Products, Orders, Couriers, Customers) to CSV files with timestamped filenames, stored in the `csv` folder under `src`.

### Graphics Integration
- **ASCII Art**: Enhance the CLI experience with professionally styled ASCII art logos stored in the `graphics` folder.


## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.12
- Docker

### Cloning the Repository
To clone the repository, run the following commands:
```bash
git clone https://github.com/Alisam-alkhalil/Cafe-Ordering-System
```


## Environment Setup

Create a .env file:

- Use the provided `.env.example` file as a template.
- Rename `.env.example` to `.env` and fill in the database credentials.

## Running the Application with Docker

Run the following command to start the application using Docker:
```bash
docker-compose --env-file ./.env up -d
```

This ensures the .env variables are used when setting up Docker.

## Accessing the Application

- Open your browser and navigate to `localhost:8080`.
- Use the credentials from the `.env` file to log in to the PostgreSQL database.

If `localhost` doesn't work as the input for `host`, use the following command to find the container's IP address:

```bash
docker inspect <postgres_container_id>
```

## Installing Python Requirements

Run this command to install the required Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Finally, run the application:
```bash
python src/main.py
``` 

## Code Quality & Error Handling

- **Error Handling**: Prevent invalid operations, such as deleting non-existent products or assigning unavailable couriers.

- **Data Validation**: Ensures data integrity by validating input fields and database consistency.

- **Efficiency**: The system auto-balances order assignments among couriers.