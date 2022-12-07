from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from datetime import datetime, timedelta
import json
import os

token_endpoint = "/learn/api/public/v1/oauth2/token"


class Token:
    def __init__(self, application_key, secret, url):
        self.application_key = application_key
        self.secret = secret
        self.url = url
        self.now = datetime.now()
        self.token = ""
        self.token_expires_in = 0
        self.token_expiration_date = ""
        self.current_dir = os.getcwd()

# Main function
    def create_token(self):
        if self.token_file_exist():
            if self.is_token_date_valid(self.extract_date()):
                return self.token_headers(self.token)
            else:
                self.remove_file()
        self.generate_token()
        return self.token_headers(self.token)

# Does the file already exist?
    def token_file_exist(self):
        path = self.current_dir + "/token"
        exists = os.path.exists(path)
        return exists

# is the token date "valid"
    def is_token_date_valid(self, token_date):
        # a token date is valid when the date in the file is bigger than now()
        token_end_date = datetime.strptime(
            token_date, "%Y-%m-%d %H:%M:%S.%f")
        if token_end_date > self.now:
            return True
        return False

# generate a new token
    def generate_token(self):
        try:
            client = BackendApplicationClient(
                client_id=self.application_key)
            oauth = OAuth2Session(client=client)
            token_payload = oauth.fetch_token(
                token_url=self.url + token_endpoint, client_id=self.application_key, client_secret=self.secret)
            self.token = "Bearer " + token_payload["access_token"]
            self.token_expires_in = token_payload["expires_in"]
            self.create_token_tmp_file()
            if self.token_file_exist():
                return self.token_headers(self.token)
            else:
                print("There seems to be an error when creating the token temporary file, please make sure the application can create, remove files")
        except:
            return False

# Define the date on which the token will expire
    def set_token_expiration_date(self):
        # token expt date has to be changed to str to be dumped in json to the external file
        token_expiration_date = self.now + \
            timedelta(seconds=int(self.token_expires_in))
        self.token_expiration_date = token_expiration_date
        return str(token_expiration_date)

# Generates the token temporary file
    def create_token_tmp_file(self):
        file_content = self.token_headers(self.token)
        file_content.update(
            {"token_expiration_date": self.set_token_expiration_date()})
        file_content = json.dumps(file_content)
        file_token = open("token", "x")
        file_token.write(file_content)
        file_token.close()
        return file_content

# Creates the token authorization dictionary
    def token_headers(self, token):
        token_data = {
            "authorization": token,
        }
        return token_data

# Reads the file
    def read_file(self):
        # assumes the file is always called token
        token_file = open("token")
        file_content = token_file.read()
        file_content = json.loads(file_content)
        token_file.close()
        return file_content

# Reads the date on the token file
    def extract_date(self):
        file_content = self.read_file()
        date_string = file_content["token_expiration_date"]
        self.token = file_content["authorization"]
        return date_string

# removes the file when the token is no longer valid
    def remove_file(self):
        try:
            path = self.current_dir + "/token"
            os.remove(path)
            return True
        except FileNotFoundError:
            ("The file no longer exists")


# First you need to instance the token to start the process
# you can see the token itself by printing it, you have to call create_token() after instantiating the object
