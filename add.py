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
    CREATE TABLE IF NOT EXISTS recruiters (
        id uuid NOT NULL,
        name character varying(100) COLLATE pg_catalog."default" NOT NULL,
        phone_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
        skills text[] COLLATE pg_catalog."default",
        role character varying(50) COLLATE pg_catalog."default" NOT NULL,
        experience integer NOT NULL,
        CONSTRAINT recruiters_pkey PRIMARY KEY (id)
    )
""")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()