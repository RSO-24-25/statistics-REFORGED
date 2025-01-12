# Statistics Microservice

## Overview
The Statistics Microservice provides insights and data visualizations related to product pricing. It connects to an Azure SQL database to fetch historical pricing data, generates graphs, and serves them through a gRPC-based service.

## Features
- Fetch and visualize product price history as graphs.
- Retrieve a list of all available products with their IDs.
- Expose gRPC endpoints for seamless integration.

---

## Architecture
The microservice uses the following components:
- **gRPC**: For communication and service definitions.
- **Python (grpcio)**: Framework for implementing gRPC services.
- **Azure SQL Database**: Stores historical price data.
- **Matplotlib**: Generates graphs for price visualizations.

---

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Docker
- Azure SQL database with necessary tables and data.
- A valid MongoDB URI for use with the service.

### Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd statistics-microservice
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Build and run with Docker Compose:
    ```bash
    docker-compose up --build
    ```

### Environment Variables
| Variable Name | Description                                    |
|---------------|------------------------------------------------|
| `MONGO_URI`   | URI for connecting to the MongoDB database.    |

Update the `docker-compose.yaml` file to set the `MONGO_URI` and other required values.

---

## Usage

### gRPC Endpoints
The microservice provides the following gRPC endpoints:

#### 1. **Get_Prices_Graph**
   - **Request**: Product ID
   - **Response**: A PNG image of the price history graph.

