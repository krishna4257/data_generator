import json
import random
import time
from datetime import datetime
import boto3
from faker import Faker

# Initialize Faker
fake = Faker()

# AWS S3 Configuration
s3 = boto3.client('s3', region_name='us-east-2')  # Change region as needed
bucket_name = 'dtatstore'# Replace with your actual S3 bucket

# Generate Fake Users
def generate_users(num_users=100):
    users = []
    for _ in range(num_users):
        users.append({
            "user_id": fake.uuid4(),
            "user_name": fake.name(),
            "user_dob": str(fake.date_of_birth(minimum_age=18, maximum_age=80)),
            "city": fake.city(),
            "state": fake.state(),
            "zipcode": fake.zipcode(),
            "order_history": [fake.uuid4() for _ in range(random.randint(1, 5))]
        })
    return users

# Generate Fake Orders
def generate_orders(users, num_orders=200):
    orders = []
    for _ in range(num_orders):
        user = random.choice(users)
        order_total = round(random.uniform(10, 500), 2)
        order_date = fake.date_time_between(start_date="-30d", end_date="now").isoformat()

        orders.append({
            "order_id": fake.uuid4(),
            "user_id": user["user_id"],
            "items": [
                {"name": fake.word(), "quantity": random.randint(1, 3), "price": round(random.uniform(5, 100), 2)}
            ],
            "order_total": order_total,
            "order_date": order_date
        })
    return orders

# Upload Data to AWS S3
def upload_to_s3(data, filename):
    try:
        s3.put_object(Bucket=bucket_name, Key=filename, Body=json.dumps(data))
        print(f"Uploaded {filename} to S3.")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

# Main Function to Run Data Generation
def run_data_generation():
    while True:
        users = generate_users(100)
        orders = generate_orders(users, 200)

        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')
        upload_to_s3(users, f'users_{timestamp}.json')
        upload_to_s3(orders, f'orders_{timestamp}.json')

        print(f"Generated and uploaded data at {timestamp}")
        time.sleep(900)  # Run every 15 minutes

if __name__ == "__main__":
    run_data_generation()
