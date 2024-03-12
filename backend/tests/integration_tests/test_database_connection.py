from db import db
from sqlalchemy import text
from main import app

# Check the database connection
def check_db_connection():
    with app.app_context():
        try:
            # Obtain a connection from the engine
            conn = db.engine.connect()
            print("CONN", conn)
            
            # Execute a simple query against one of the tables
            query = text("SELECT TOP 1 * FROM dbo.InfrastructureConfig ORDER BY ServerName")
            result = conn.execute(query)
            
            # Close the connection
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")
            return False

def test_db_connection_success():
    # assertions
    assert check_db_connection() == True

