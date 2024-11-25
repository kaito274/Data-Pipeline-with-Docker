import requests
import os
import time
import json
import random
from kafka import KafkaProducer

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

# Fetch list of rated users from Codeforces who participated in rated contest during the last month
def get_rated_users():
    url = "https://codeforces.com/api/user.ratedList?activeOnly=true&includeRetired=true"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        # return [user['handle'] for user in data["result"]]
        user_details = []
        for user in data["result"]:
            # Extract relevant attributes
            user_data = {
                "handle": user['handle'],
                "rating": user['rating'],
                "rank": user['rank'],
                "max_rating": user['maxRating'],
                "max_rank": user['maxRank'],
                "last_online_time": user['lastOnlineTimeSeconds'],
                "registration_time": user['registrationTimeSeconds'],
                "contribution": user['contribution'],
                "country": user.get('country', None),
            }
            user_details.append(user_data)
        random.shuffle(user_details) 
        return user_details
    else:
        return []

def run():
    rated_user = get_rated_users()
    iterator = 0
    print("Setting up Codeforces producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )
    i = 0
    while True:
        # Fetch a new list of rated users if the iterator exceeds the current list size
        if i >= len(rated_user):
            print("Iterator exceeded bounds. Fetching new data.")
            rated_user = get_rated_users()
            i = 0  

        sendit = rated_user[i]
        # adding prints for debugging in logs
        print("Sending new codeforces user data iteration - {}".format(iterator))
        producer.send(TOPIC_NAME, value=sendit)
        print("New codeforces user data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1
        i += 1


if __name__ == "__main__":
    run()