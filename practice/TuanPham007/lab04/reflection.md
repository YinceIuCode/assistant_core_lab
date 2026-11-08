Lab 3 used a direct Python function call service.handle() inside the same code.
Lab 4 turns it into a web endpoint POST /v1/chat that clients call over HTTP.
FastAPI automatically handles JSON data conversion and route matching for us.
This separates the web network layer from the core backend logic.
It allows external web or mobile apps to connect to our service easily.