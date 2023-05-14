import os
import csv
import random
import importlib
from celestial.models import *


def generate_data(model_name: str):
    
    # Define the file name and path where you want to save the CSV file
    filename = model_name + ".csv"
    filepath = "/sample_data/" + filename

    if model_name == 'Post':
        model_class = Post
    elif model_name == 'Topic':
        model_class = Topic
    elif model_name == 'User':
        model_class = UserProfile


    # Get the attribute names and types of the model
    fields = model_class._meta.get_fields()
    field_names = [field.name for field in fields]
    field_types = [field.get_internal_type() for field in fields]

    # Define a mapping of field types to random value generators
    value_generators = {
        "AutoField": lambda: None,
        "BigAutoField": lambda: None,
        "BooleanField": lambda: random.choice([True, False]),
        "CharField": lambda: "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        "DateField": lambda: random.choice(["2022-01-01", "2022-02-01", "2022-03-01"]),
        "DateTimeField": lambda: random.choice(["2022-01-01 00:00:00", "2022-02-01 00:00:00", "2022-03-01 00:00:00"]),
        "DecimalField": lambda: round(random.uniform(1.0, 100.0), 2),
        "FloatField": lambda: round(random.uniform(1.0, 100.0), 2),
        "IntegerField": lambda: random.randint(1, 100),
        "PositiveIntegerField": lambda: random.randint(1, 100),
        "PositiveSmallIntegerField": lambda: random.randint(1, 100),
        "SmallIntegerField": lambda: random.randint(1, 100),
        "TextField": lambda: "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=50)),
        "TimeField": lambda: random.choice(["00:00:00", "01:00:00", "02:00:00"])
    }

    # Generate random data for each field in the CSV file
    data = []
    for i in range(10):
        row = []
        for field_type in field_types:
            value = value_generators[field_type]()
            row.append(value)
        data.append(row)

    # Open the CSV file and write the headers and data
    with open(filepath, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(field_names)
        writer.writerows(data)

    print("CSV file created successfully!")
