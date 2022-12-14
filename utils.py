from get_token import Token
from credentials import application_key, secret, your_institution_url
import requests
from datetime import time,timedelta,datetime
import re
import json

# This object name is probably temporary
class Caller:
    def __init__(self):
        self.token = self.instantiate_token()
        self.returned_headers = {}
        # used to determine the variables on an endpoint
        self.regex = "\{(.*?)\}"
        self.remaining = {}

# Instantiate the token object.
    def instantiate_token(self):
        connection = Token(application_key=application_key,
                        secret=secret, url=your_institution_url)
        token = connection.create_token()
        return token

# Returns a list of variables within an endpoint
    def endpoint_arguments(self, endpoint):
        arguments = re.findall(self.regex, endpoint)
        return arguments

# This function returns an url with the arguments passed
# It organizes the values accordingly in same order they are received
# Names in kwargs should match the same in the {argument} url format
# eg: /learn/api/public/v1/courses/{courseId}/users/{userId} has two courseId and userId

    def build_request_url(self, endpoint, **arguments):
        endpoint_args = self.endpoint_arguments(endpoint)
        received_arguments = arguments
        if len(received_arguments) == len(endpoint_args):
            url = endpoint
            for args in endpoint_args:
                url = url.replace("{" + args + "}", received_arguments.get(args))
            return url
        else:
            return (" error: the number of arguments is not correct, make sure to pass the following:", endpoint_args)

# reviews if the method string passed when calling request is valid
    def is_method_valid(self,method):
        method = method.lower()
        valid_methods = ["get", "post", "delete", "patch", "put"]
        if method in valid_methods:
            return True
        return False

# Calculates the date of reset of the calls for the api limits
    def calculate_date_of_reset(self,epoch_seconds):
        date_of_reset = datetime.now() + timedelta(seconds=epoch_seconds)
        return str(date_of_reset)

# returns the rate limit
    def rate_limits(self):
        self.remaining = {
            "Total-limit":self.returned_headers.get("X-Rate-Limit-Limit"),
            "Remaining-calls":self.returned_headers.get("X-Rate-Limit-Remaining"),
            "date-of-reset": self.calculate_date_of_reset(int(self.returned_headers.get("X-Rate-Limit-Reset")))
        }
        return self.remaining

# Main function
# Receives minimum 2 arguments (endpoint, method) payload is optional since not all methods require it
# and arguments can have as many as the endpoint requires
    def request(self, endpoint, method, payload="", **arguments):
        if self.is_method_valid(method):
            new_url = self.build_request_url(endpoint,**arguments)
            url = (your_institution_url + new_url)
            data = {}
            match method:
                case "get":
                    data = requests.get(url, headers=self.token)
                case "post":
                    data = requests.post(url, headers=self.token, json=payload)
                case "delete":
                    data = requests.delete(url, headers=self.token)
                case "patch":
                    data = requests.patch(url, headers=self.token, json=payload)
                case "put":
                    data = requests.put(url, headers=self.token, json=payload)

            self.returned_headers = data.headers
            return json.dumps({"status_code": data.status_code, "result": json.loads(data.text)})
        return {"error": "method entered is not valid, please use get, put ,post ,patch or delete in lowercase"}

# to use this, you can instantiate Call()
# Then use your instance.request(arguments) to make a call.
# Since this instantiates the object Token for you, you do not need to re-make the call.
# eg: 
# make.request(endpoint="/learn/api/public/v1/courses/{courseId}/users",
#             method="get",
#              courseId="_912_1"
