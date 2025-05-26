import json
import argparse
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str, help='Enter a GitHub username')

    args = parser.parse_args()
    fetch_activity(args.username)

def fetch_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            print("No recent activity found for user: {username}")

        print(f"Recent GitHub activity for {username}: ")
        for event in data[:5]:
            event_type = event.get("type")
            repo = event.get("repo", {}).get("name","Unknown repo")
            print(f"- {event_type} in {repo}")

    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400:
                print("Bad request:\nPlease check your input.")
            case 403:
                print("Forbidden:\nAccess is denied (rate limit may be hit).")
            case 404:
                print(f"User '{username}' not found.")
            case 500:
                print("Internal Server Error:\nPlease try again later.")
            case 502:
                print("Bad Gateway:\nInvalid response from the server.")
            case 503:
                print("Service Unavailable:\nServer is down.")
            case 504:
                print("Gateway Timeout:\nNo response from server.")
            case _:
                print(f"HTTP error occurred:\n{http_error}")
    except requests.exceptions.ConnectionError:
        print("Connection Error:\nCheck your internet connection.")
    except requests.exceptions.Timeout:
        print("Timeout Error:\nRequest timed out.")
    except requests.exceptions.TooManyRedirects:
        print("Too many Redirects:\nCheck the URL.")
    except requests.exceptions.RequestException as req_error:
        print(f"Request Error:\n{req_error}")

if __name__ == "__main__":
    main()

