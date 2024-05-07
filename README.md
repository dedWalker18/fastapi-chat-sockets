<h2 align="center">  Quahog Chatterbox: A Family Guy Themed Real Time Chat App  </h2>

<h1 align="center">

   ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
   ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
   ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
   ![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
   ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)


</h1>

<p align="center">   
   
   <img src="frontend/src/assets/logo.png" alt="LIVrary Logo" width="400" height="400" style='text-align:center;'>
   
</p>

**Welcome to Quahog Chatterbox!! An End-TO-End Encrypted Real Time Chat Application using FastAPI & VueJS**

**Key Features**

* **User Actions:**

    * Users have JWT-based auth.
    * Connect with friends (social-media functionalities).
    * have real-time chats using web sockets. 
    * Maintane Favorite friends list.
    * Join groups with  text boards and group chat (inspired by Discord).
    * Choose a colorful avatar to personalize their experience.
    * Receive email alerts if they don't log in daily to stay engaged (optional).
   
* **Admin Management:**

    * Computer Vision model that looks for profanities in the global text board.
    * Bans a user after three strikes!! Unless you are Peter Griffin obviously.. 

* **Advanced Functionalities:**

    * **Asynchronous Tasks:** Leverage Celery and Redis for background tasks, ensuring a smooth user experience. 
    * **Email Notifications:** An integrated mail client sends automated email alerts and reports. 
    * **End-To-End Encrypted Messages:** Uses pair of usernames plus secret salt for encryption.
    * **HTTPS:** Both backend and frontend run on HTTPS self-signed certificates.

**Technical Stack**

* Backend:
    * FastAPI  - API framework for robust backend development.
    * Swagger UI - User-friendly interface for API documentation.
    * SQLAlchemy - Powerful object-relational mapper (ORM) for database interactions.
    * Custom SMTP Server - Handles email communication.
    * JWT Tokens - Secure user authentication and RBAC.
   
* Frontend:
    * Vue.js 2 - Modern JavaScript framework for a dynamic and interactive user interface.
    * Bootstrap - Popular CSS framework for responsive design.
    * Axios/Fetch - The chat application gotta chat with the backend too!

* Security:
    * HTTPS enforced using self-signed certificates for secure communication.

---

**Getting Started (For Developers)**


1.  Clone this repository
   
   ```
      git clone https://github.com/dedWalker18/livbrary.git
   ```

2.  Install Prerequisites

   ```
      pip install -r requirements.txt
   ```

3. Navigate to Backend and run the following command in a terminal. (certificates optional)

```
   flask run --host=0.0.0.0 --debug

   flask run --host=0.0.0.0 --debug --cert=cert.pem --key=key.pem
```

4.  Run Celery and Connect to a Redis-Server. Run each command in a separate terminal.
   
   ```
      redis-server
    
      celery -A app.celery worker --loglevel=info
    
      celery -A app.celery beat --loglevel=info
   ```

5. Navigate to Frontend and run the following command in a separate terminal.
   
```
   npm i

   npm run serve
```



6. You can use Mailhog inside docker to test the mail client.
   Alternatively, you can use FastMail or other services.

```
   docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

---

*OPTIONAL -  run feeder.py file to feed fodder data to the application.*
   
**Make sure to expose free ports on your network if the predefined ports are already busy.**

**Conclusion**

Football chat outside Drunken Clam? Gossip about recent events in Spooner Street? We got y'all covered!!!

---
