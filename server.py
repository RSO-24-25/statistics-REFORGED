import grpc
from concurrent import futures
import time
import pyodbc
import matplotlib.pyplot as plt
from io import BytesIO


import service_pb2
import service_pb2_grpc


server = 'rsosqlserver.database.windows.net'  # Azure SQL server name
database = 'inventory'                        # Database name
username = 'musicn@rsosqlserver'              # Username
password = 'nekiPogacarneki123'             # Replace with your password
driver =  '{ODBC Driver 18 for SQL Server}'    # ODBC Driver for SQL Server on Azure
connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;'


# Connect to the SQL Server database
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()



# Implement the Greeter service
class Statistics(service_pb2_grpc.StatisticsServicer):
    def Get_Prices_Graph(self, request, context):

        print("\nFetching prices data for...")
        product_id = request.id
        print(f"ID: {product_id}")


        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM ProductPriceHistory WHERE ProductID = ?", (product_id,))
        rows = cursor.fetchall()
        print("\nRecieved data from SQL:")
        print(rows[:3])

        # Extract dates and prices
        dates = [row[3] for row in rows]  # Extract dates (datetime objects)
        prices = [float(row[2]) for row in rows]  # Extract prices (converted to float)

        # Plotting the data
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dates, prices, marker='o', linestyle='-', color='b', label='Price')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title('Price vs Date')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        ax.legend()

        # Save the plot to a BytesIO object
        img_stream = BytesIO()
        plt.savefig(img_stream, format='png')
        img_stream.seek(0)  # Reset the pointer to the beginning of the stream
        image_data = img_stream.read()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the image as a byte stream in the response
        return service_pb2.GraphReply(image=image_data)


    def Get_all_products(self, request, context):
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Execute the SQL query to fetch distinct ProductID and ProductName
        cursor.execute("SELECT DISTINCT ProductID, ProductName FROM ProductPriceHistory;")
        rows = cursor.fetchall()
        print(rows)

        # Prepare a list of products as (ProductName, ProductID) pairs
        products = []
        for row in rows:
            product_name = row[1]
            product_id = row[0]
            products.append(service_pb2.Product(id=product_id, name=product_name))

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the list of products
        return service_pb2.AllProductsReply(products=products)


# Create and start the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_StatisticsServicer_to_server(Statistics(), server)
    
    # Listen on port 50051
    print("Server started on port 50051...")
    server.add_insecure_port('[::]:50051')
    server.start()
    
    try:
        while True:
            time.sleep(60 * 60 * 24)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()