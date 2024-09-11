# Homework #4

## Task Overview

Your goal is to implement a simple web application. Use the following files as a base.

### Requirements:

1. Create a web application with routing for two HTML pages: `index.html` and `message.html`.

2. Additionally:
   - Serve static resources at startup: `style.css`, `logo.png`.
   - Organize form handling on the `message.html` page.
   - In case of a `404 Not Found` error, return the `error.html` page.
   - Your web application should run on port **3000**.
   - To work with the form, create a **Socket server** running on port **5000**. The workflow is as follows:
     - You enter data into the form on `message.html`.
     - The data is sent to your web application.
     - The web application forwards the data to the Socket server using the UDP protocol.
     - The Socket server processes the received byte string, converts it into a dictionary, and saves it into the `data.json` file located in the `storage` folder.

### JSON File Format (`data.json`):

```json
{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  },
  "2022-10-29 20:21:11.812177": {
    "username": "Krabat",
    "message": "Second message"
  }
}
```

The key for each message is the time it was received (`datetime.now()`), meaning that each new message from the web application is added to the `storage/data.json` file with the timestamp of its receipt.

### Implementation Details:
- **One file:** Use a single `main.py` file for the entire web application.
- **Multithreading:** Run the HTTP server and Socket server in separate threads.

---

## Additional Task (Optional)
This is an optional task and is not required to complete the homework.

- Create a `Dockerfile` and run your application as a Docker container.
- Using the **volumes** mechanism, store the data from the `storage/data.json` file outside the container.

### HINT:
To implement the volumes mechanism, at the start of the application, check for the existence of the `storage` directory and the `data.json` file. If they don't exist, create them.

Good luck!