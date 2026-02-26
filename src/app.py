"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Schachclub": {
        "description": "Lerne Strategien und nimm an Schachturnieren teil",
        "schedule": "Freitags, 15:30 - 17:00 Uhr",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programmierkurs": {
        "description": "Lerne Programmiergrundsätze und entwickle Softwareprojekte",
        "schedule": "Dienstags und Donnerstags, 15:30 - 16:30 Uhr",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Sportunterricht": {
        "description": "Sportunterricht und Sportaktivitäten",
        "schedule": "Montags, Mittwochs, Freitags, 14:00 - 15:00 Uhr",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketballmannschaft": {
        "description": "Trete unserem Wettkampf-Basketballteam bei und nimm an regionalen Turnieren teil",
        "schedule": "Montags und Mittwochs, 16:00 - 17:30 Uhr",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennisclub": {
        "description": "Lerne Tennisfähigkeiten und nimm an freundlichen Spielen teil",
        "schedule": "Dienstags und Donnerstags, 16:00 - 17:00 Uhr",
        "max_participants": 10,
        "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
    },
    "Kunststudio": {
        "description": "Erkunde Mal-, Zeichen- und Mischtechniken",
        "schedule": "Mittwochs, 15:30 - 17:00 Uhr",
        "max_participants": 18,
        "participants": ["lucy@mergington.edu"]
    },
    "Musikband": {
        "description": "Lerne Instrumente und tritt in Schulkonzerten auf",
        "schedule": "Montags und Donnerstags, 15:30 - 16:30 Uhr",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "grace@mergington.edu"]
    },
    "Debattierclub": {
        "description": "Entwickle Argumentationsfähigkeiten und nimm an Debattenwettbewerben teil",
        "schedule": "Freitags, 16:00 - 17:30 Uhr",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu"]
    },
    "Wissenschaftsclub": {
        "description": "Führe Experimente durch und erkunde wissenschaftliche Entdeckungen",
        "schedule": "Dienstags, 15:30 - 17:00 Uhr",
        "max_participants": 20,
        "participants": ["henry@mergington.edu", "amelia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
