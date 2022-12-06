# Learn-API-Explorer

The code can be definetively *better* however, for this demonstration is enough and pretty capable.

To use it, please make sure your credentials are updated in the "Credentials" file.

Make a call using the test.py file

Make sure to provide the following information: 

1. Instantiate the Caller object first, in my case I called it make.
2. use request method from Caller as such make.request()
3. make.request() expects different values according to the endpoint you pass, it expects them in this order:

* endpoint
* method
* payload (optional)
* url variables based on the endpoint requirements (It only accepts pk1s with the form of _###_1 or #### as strings.

