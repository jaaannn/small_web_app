from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
import requests
import os

BACKEND_URL = os.environ["BACKEND_URL"]
PORT = os.environ['PORT']


def fetch_users():
    response = requests.get(BACKEND_URL + '/users')
    if response.status_code == 200:
        return response.json()  # Assuming the backend returns a list of users
    else:
        toast("Failed to fetch users", color='red')
        return []


def main():
    while True:
        # Display the table of users
        users = fetch_users()
        if users:  # Only display if we actually got some data
            # Assuming the user object has 'name', 'lastName', and 'username' keys
            user_table_data = [[user['name'], user['lastName'], user['username']] for user in users]
            put_table([
                ['Name', 'Last Name', 'Username'],  # Table header
                *user_table_data  # Table rows
            ])
        # Input group to gather user data and action choice
        user_data = input_group("User Management", [
            input('Name', name='name', required=True),
            input('Last Name', name='lastName', required=True),
            input('Username', name='username', required=True),
            actions('Choose action:', [
                {'label': 'Save', 'value': 'save'},
                {'label': 'Delete', 'value': 'delete'}
            ], name='action')
        ])

        response = None  # Initialize response to None to ensure it's always defined

        # Check the user's chosen action and make the appropriate request
        if user_data['action'] == 'save':
            response = requests.post(BACKEND_URL + "user", json=user_data)
        elif user_data['action'] == 'delete':
            response = requests.delete(f"{BACKEND_URL}user/{user_data['username']}")

        # Check if the response is not None and display appropriate toast message
        if response:
            if response.status_code in [200, 201]:
                toast(response.json()['message'], color='green')
            else:
                error_message = response.json().get('error', 'An unknown error occurred')
                toast(f"Error: {error_message}", color='red')
        else:
            # This should never happen if all actions are handled correctly
            toast("An unknown error occurred. Please try again.", color='red')


if __name__ == '__main__':
    start_server(main, port=PORT, host='0.0.0.0')
