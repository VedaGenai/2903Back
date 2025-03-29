import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="fasthire",
    user="postgres",
    password="Temp1234",
    host="localhost",  # Change if using a remote server
    port="5432"
)

cursor = conn.cursor()

# Execute the query
cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_analyses (
        id SERIAL PRIMARY KEY,
        roles JSONB,
        skills_data JSONB,
        content TEXT,
        selection_threshold FLOAT,
        rejection_threshold FLOAT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
""")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
