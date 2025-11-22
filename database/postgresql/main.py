import faker
import pandas as pd
import time
from sqlalchemy import create_engine
import pendulum

engine = create_engine("postgresql://postgres:pg1234@localhost:5432/postgres")
fake = faker.Faker()

def create_table():

    with engine.connect() as conn:
        conn.execute("""
            CREATE TABLE customers (
                customer_id UUID PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(50),
                address TEXT,
                segment VARCHAR(50),
                join_date TIMESTAMP,
                loyalty_points INTEGER
            );
        """)
        print("Table created successfully.")

def generate_customers(num_customers):
    customers = []
    for _ in range(num_customers):
        customer = {
            'customer_id': fake.uuid4(),
            'name': fake.name(),
            'email': fake.email(), 
            'phone': fake.phone_number(),
            'address': fake.address(),
            'segment': fake.random_element(['Retail', 'Wholesale', 'Online', 'In-Store']),
            'join_date': pendulum.now('Asia/Bangkok'),
            'loyalty_points': fake.random_int(min=0, max=1000)
        }
        customers.append(customer)
    return customers


create_table()


# สร้างข้อมูลลูกค้า
for _ in range(20):
    customers = generate_customers(5)
    customer_df = pd.DataFrame(customers)
    customer_df.to_sql('customers', engine, if_exists='append', index=False)
    print(f"Created {len(customers)} customers to Postgres at {time.strftime('%H:%M:%S')}")
    time.sleep(5)