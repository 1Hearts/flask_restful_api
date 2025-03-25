# Flask RESTful API Project

##  Team
Chanho Kim

##  About This Project
Hey! This is a simple RESTful API project I made using Flask.  
Basically, it lets you do stuff like signing up, logging in, uploading files, and managing items (creating, reading, updating, and deleting them).  
I used MySQL for storing all the data, and I also made sure there’s some error handling so the app doesn't just crash randomly.  

---

##  What This App Can Do
1. User Authentication (Logging in and getting a token to access private stuff)
2. Uploading and Viewing Files
3. CRUD Operations (Create, Read, Update, Delete items)
4. Error Handling (For stuff like 400, 401, 404, and 500 errors)
5. Public and Protected Routes (Some things you can access without logging in, some you can't)

---

##  How To Set Up and Run This App (Step-by-step Guide)
Here's how you can set up everything and get it running.

###  1. Setting Up The Virtual Environment
1. First, open your terminal (VSCode, CMD, or PowerShell) and go to your project folder (`flask_restful_api`).  
2. Then, make a virtual environment and activate it like this:

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# For Windows
venv\Scripts\activate

# For Mac/Linux
source venv/bin/activate

