from fastapi import FastAPI
from pydantic import BaseModel
import psycopg #for Python access to PostgreSQL
from fastapi import HTTPException
from typing import Literal #part of Python's typing system, lets you restrict a variable to specific allowed values
from datetime import datetime

app = FastAPI() #FastAPI app

#---------------------------------------------------------
#Pydantic Model (for users)
#---------------------------------------------------------

class UserCreate(BaseModel): #Request Model

    full_name: str
    email: str
    role: str #user system role for the MVP, such as (reporter, dev, or admin)

class UserResponse(BaseModel): #Response Model
    user_id: int #generated primary key
    full_name: str #user provided data
    email: str #user provided data
    role: str #controlled value
    created_at: datetime #library timestamp function generated

#This is the foundation for our /users enpoint


#---------------------------------------------------------
#Pytdantic Model (for Issues)
#---------------------------------------------------------

class IssueCreate(BaseModel): #Request Issue Body
    #This is the request body for Post /issues
    title: str
    description: str
    issue_type: str
    priority: str
    status: str
    created_by: int
    assigned_to: int | None = None #basically states it may be an integer user id or None
    #and if omitted, defaults to None

class IssueResponse(BaseModel): #Response issue body
    #This is the full issue record returned by the API
    issue_id: int
    title: str
    description: str
    issue_type: str
    priority: str
    status: str
    created_by: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime


#---------------------------------------------------------
#Root Enpoint (existing)
#---------------------------------------------------------


@app.get("/")
def read_root(): 
    return {"message": "Incident Tracking System API is running"}


#---------------------------------------------------------
#Create the first working POST /users endpoint
#----------------------------------------------------------

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):


    conn = get_db_connection() #opening connection to PostgreSQL
    cur = conn.cursor() #create cursor
 

    cur.execute(
        """
        INSERT INTO users (full_name, email, role)
        VALUES (%s, %s, %s)
        RETURNING user_id, full_name, email, role, created_at
        """,

        (user.full_name, user.email, user.role)
    )

    new_user = cur.fetchone()
    if new_user is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to create user")

    conn.commit()

    cur.close()
    conn.close()


    return UserResponse(
        user_id = new_user[0],
        full_name = new_user[1],
        email = new_user[2],
        role = new_user[3],
        created_at = new_user[4]
    )

#----------------------------------------------------
#Add basic PostgreSQL connection code
#----------------------------------------------------

"""
Adding connection helper function
"""
def get_db_connection():
    conn = psycopg.connect(
        dbname="issue_tracker_proj",
        user="postgres",
        password="Dreamsmadereal1!",
        host="localhost",
        port="5432"
    )
    return conn


#-------------------------------------------
#GET /users
#-------------------------------------------


@app.get("/users", response_model=list[UserResponse])
def get_users(): 
    #pass #temp placeholder to the function is syntacially valid until we add real code

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT user_id, full_name, email, role, created_at
        FROM users
        ORDER BY user_id; 
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    users = []

    for row in rows:
        #for each row build UserResponse(...)
        users.append(
            UserResponse(
                user_id= row[0],
                full_name = row[1],
                email = row[2],
                role = row[3],
                created_at= row[4]
            )
        )

    return users #return list of users


#-------------------------------------------
#Mental model for Get /users/{user_id}
#-------------------------------------------


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    # "/users/{user_id}" : defines a dynamic URL
    # "user_id: int" : tells FastAPI to extract that value from the path and treat it
        # as an integer
    # "response_model = UserResponse" : means this enpoint should return one user object 
    #pass #temp placeholder

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT user_id, full_name, email, role, created_at
        FROM users
        WHERE user_id = %s;
        """,
        (user_id,)
    )

    row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="user not found")

    cur.close()
    conn.close()

    """
    (user_id,) 
    - important because it must be a tuple
    - should NOT be (user_id), this = just an int
    """

    #if row exists
    return UserResponse(
        user_id=row[0],
        full_name = row[1],
        email = row[2],
        role = row[3],
        created_at = row[4]
    )
    


#-------------------------------------------
#Adding route skeleton for POST /issues
#-------------------------------------------

@app.post("/issues", response_model=IssueResponse, status_code=201)
def create_issue(issue: IssueCreate):
    """
    What this does
    - registers a new endpoint at: POST /issues
    - tells FastAPI the request body should match: IssueCreate
    - tellsFastAPI the response should match: IssuesResponse

    So FastAPI will eventually take incoming JSON, validate it against IssueCreate,
    and hand us an issue object with attributes like:
    - issue.title
    - issue.description
    - issue.issue_type
    - issue.priority
    ...
    """
    #pass

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO issues(
            title,
            description,
            issue_type,
            priority,
            status,
            created_by,
            assigned_to
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING
            issue_id,
            title,
            description,
            issue_type,
            priority,
            status,
            created_by,
            assigned_to,
            created_at,
            updated_at
        """,
        (
            issue.title,
            issue.description,
            issue.issue_type,
            issue.priority,
            issue.status,
            issue.created_by,
            issue.assigned_to
        )
    )

    new_issue = cur.fetchone()

    if new_issue is None:
        cur.close()
        conn.close()
        raise ValueError("Insert failed: no issues row was returned from PostgreSQL.")

    conn.commit() #saves the transaction, must happen before closing the connection

    cur.close() #close cursoe (query interface)
    conn.close() #close DB connection (network + session)

    return IssueResponse(
        issue_id = new_issue[0],
        title = new_issue[1],
        description = new_issue[2],
        issue_type = new_issue[3],
        priority = new_issue[4],
        status = new_issue[5],
        created_by = new_issue[6],
        assigned_to = new_issue[7],
        created_at = new_issue[8],
        updated_at = new_issue[9]
    )

#-----------------------------------------------------------
# Adding GET /issues endpoint with optional query parameters 
#       -> adding filtering + query parameters
#-----------------------------------------------------------

@app.get("/issues", response_model = list[IssueResponse])
def get_issues(
    status: Literal["open", "in_progress", "closed"] | None = None, 
    priority: Literal["low", "medium", "high"] | None = None
    
    ):
    pass


    #Build the SQL logic for 0, 1, or 2 filters 


    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT issue_id, title, description, issue_type, priority, status,
    created_by, assigned_to, created_at, updated_at
    FROM issues
    """

    params = [] 

    if status is not None and priority is not None:
        query += " WHERE status = %s AND priority = %s"
        params.extend([status,priority])

    elif status is not None: 
        query += " WHERE status = %s"
        params.append(status)

    elif priority is not None:
        query += " WHERE priority = %s"
        params.append(priority)

    query += " ORDER BY issue_id;"

    cur.execute(query, tuple(params)) #runs the correct version of the SQL code
    rows = cur.fetchall()

    issues = []

    for row in rows: 
        issue =  IssueResponse(
            issue_id = row[0],
            title = row[1],
            description = row[2],
            issue_type = row[3],
            priority = row[4],
            status = row[5],
            created_by = row[6],
            assigned_to = row[7],
            created_at = row[8],
            updated_at = row[9]
        )
        issues.append(issue)

    return issues


#-------------------------------------------
# Adding GET /issues/{issue_id} endpoint
#-------------------------------------------

"""
Data Flow

client -> FastAPI rout with parameter -> SQL SELECT .... WHERE ... -> PostgreSQL
-> one row -> JSON response
"""

@app.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int):
    

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT issue_id, title, description, issue_type, priority, status, created_by, assigned_to, created_at, updated_at
        FROM issues
        WHERE issue_id = %s;
        """,
        (issue_id,)
    
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    return IssueResponse(
        issue_id = row[0],
        title = row[1],
        description = row[2],
        issue_type = row[3],
        priority = row[4],
        status = row[5],
        created_by = row[6],
        assigned_to = row[7],
        created_at = row[8],
        updated_at = row[9]
    )

#-------------------------------------------
# Adding PUT /issue/{issue_id} for Updating an Issue 
#-------------------------------------------

"""
Data Flow
- client -> FastAPI route with issue_id -> SQL UPDATE -> PostgreSQL -> updated
  row saved -> response returned
"""

@app.put("/issues/{issue_id}", response_model=IssueResponse)
def update_issue(issue_id: int, issue: IssueCreate):
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE issues
        SET title = %s,
            description = %s,
            issue_type = %s,
            priority = %s, 
            status = %s,
            created_by = %s, 
            assigned_to = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE issue_id = %s
        RETURNING issue_id, title, description, issue_type, priority, status,
                  created_by, assigned_to, created_at, updated_at;   
        """,
        (
            issue.title,
            issue.description,
            issue.issue_type,
            issue.priority,
            issue.status,
            issue.created_by,
            issue.assigned_to,
            issue_id
        )
    )

    row = cur.fetchone()

    if row is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code = 404, detail = "Issue not found")
    
    conn.commit() #commit changes/save changes to issues table in DB

    cur.close()

    return IssueResponse(
        issue_id = row[0],
        title = row[1],
        description = row[2],
        issue_type = row[3],
        priority = row[4],
        status = row[5],
        created_by = row[6],
        assigned_to = row[7],
        created_at = row[8],
        updated_at = row[9]
    )


#---------------------------------------------------------------
# Adding DELETE /issue/{issue_id} endpoint for Deleting an Issue 
#---------------------------------------------------------------

#Goal: Remove a row from the DB safely


@app.delete("/issues/{issue_id}", response_model=IssueResponse)
def delete_issue(issue_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM issues
        WHERE issue_id = %s
        RETURNING issue_id, title, description, issue_type, priority, status,
                  created_by, assigned_to, created_at, updated_at; 
        """,
        (issue_id,)
    )

    row = cur.fetchone()

    if row is None: 
        cur.close()
        conn.close()
        raise HTTPException(status_code = 404, detail = "Issue not found")
    
    conn.commit()
    cur.close()
    conn.close()

    return IssueResponse(
        issue_id = row[0],
        title = row[1],
        description = row[2],
        issue_type = row[3],
        priority = row[4],
        status = row[5],
        created_by = row[6],
        assigned_to = row[7],
        created_at = row[8],
        updated_at = row[9]
    )

