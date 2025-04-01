import psycopg2
import uuid

# Source data (the data you provided)
employee_data = [
    ("37df6286-9fb0-4274-86bb-e5ad552d6df2", "Jessica Lang", "(123) 456-7890", ["SQL and NoSQL databases"], "Senior Data Engineer,", 2),
    ("3fcb5543-1352-413f-9694-e0470b75bda1", "Joseph Corbin", "(123) 456-7890", ["AWS cloud services"], "Data Engineer", 3),
    ("4e794bac-6516-46e9-81b9-147e33a23ee0", "Joseph Corbin", "(123) 456-7890", ["Project management"], "ABC Warehousing", 4),
    ("d26dac96-82d9-44ec-af43-5a8e509e774c", "Jasmine Brown", "(123) 456-7890", ["Data security and compliance", "Google Cloud Platform (GCP)", "Machine learning model implementation", "Python", "Java"], "Senior Data Engineer", 7),
    ("fe778311-43a6-4d70-bc72-03ff8a1bf5a6", "Mina Sayed", "(123) 456-7890", ["AWS data services", "Data migration", "Data pipeline management", "Data warehousing", "ETL processes", "Python", "SQL and NoSQL databases"], "Senior Data Engineer", 4)
]

# Connect to target database (fasthire)
conn = psycopg2.connect(
    dbname="fasthire",
    user="postgres",
    password="Temp1234",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Insert data into the employees table
for employee in employee_data:
    employee_id, name, phone_number, skills, role, experience = employee
    
    # No need to convert the UUID string - PostgreSQL will handle it
    
    cursor.execute("""
        INSERT INTO recruiters (id, name, phone_number, skills, role, experience)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE 
        SET name = EXCLUDED.name,
            phone_number = EXCLUDED.phone_number,
            skills = EXCLUDED.skills,
            role = EXCLUDED.role,
            experience = EXCLUDED.experience
    """, (employee_id, name, phone_number, skills, role, experience))

# Commit the transaction
conn.commit()
print("Data migration completed successfully!")

# Close the connection
cursor.close()
conn.close()
