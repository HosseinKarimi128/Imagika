import uuid
import requests
from datetime import datetime

# function to create a new user
def create_user(device_id, email):
    url = "http://116.202.62.198:8001/api/v1/user/signup"
    payload = {
        "device_id": device_id,
        "email": email
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.text.strip()

# function to log in and retrieve the token
def login(device_id):
    url = "http://116.202.62.198:8001/api/v1/user/login"
    payload = {
        "device_id": device_id
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["token"]

# function to create a new topic
def create_topic(title, description, starts_on, active, token):
    url = "http://116.202.62.198:8001/api/v1/topic/create/"
    payload = {
        "title": title,
        "description": description,
        "starts_on": starts_on,
        "active": active
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

# function to upload an image and retrieve the UUID
# def upload_image(image_file, token):
#     url = "http://116.202.62.198:8001/api/v1/file/upload_file/"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         'Content-Type': 'multipart/form-data'
#     }
#     files = {
#         "file": open(image_file, "rb")
#     }
#     response = requests.post(url, headers=headers, files=files)
#     response.raise_for_status()
#     return response.text.strip()

# function to create a new post
def create_post(device_id, shown_name, prompt, n_prompt, image_id, topic_id, token):
    url = "http://116.202.62.198:8001/api/v1/post/create/"
    payload = {
        "user_device_id": device_id,
        "shown_name": shown_name,
        "prompt": prompt,
        "n_prompt": n_prompt,
        "image_id": image_id,
        "topic_id": topic_id
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# open the data file
with open("data.txt") as file:
    # loop over each group of 4 lines
    while True:
        try:
            email = next(file).strip()
            prompt = next(file).strip()
            topic = next(file).strip()
            image_file = next(file).strip()
        except StopIteration:
            # end of file
            break
        print(image_file)
        # create the user with a random device id
        device_id = str(uuid.uuid4())
        user_id = create_user(device_id, email)
        
        # log in to retrieve the token
        token = login(device_id)
        
        # create the topic
        topic_id = create_topic(topic, 'sample desc', datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'), True, token)
        
        # upload the image and retrieve the UUID
        # image_id = upload_image(image_file, token)
        
        # create the post
        create_post(device_id, email.split("@")[0], prompt, "", image_file, topic_id, token)
        
        
