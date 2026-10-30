Calling `service.handle()` in Lab 3 was a local, in-process Python function execution restricted to the same runtime environment[cite: 1, 2]. 

In contrast, `POST /v1/chat` in Lab 4 exposes the service over HTTP using standardized JSON data contracts[cite: 1, 2]. 

This HTTP API architecture decouples backend business logic from client implementations, allowing any platform (React, mobile apps, or curl) to communicate with the service[cite: 1, 2]. 

Teams prefer this approach because it enables independent development and deployment of frontend and backend applications[cite: 1, 2]. 

Additionally, it provides automatic request validation and standardized HTTP status codes for robust error handling across distributed systems[cite: 1, 2].