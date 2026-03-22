# Existing code of database/db.py is kept the same

# New tables and functions

tables = {
    "goals": ["id INTEGER PRIMARY KEY", "description TEXT", "deadline DATE", "status TEXT"],
    "fsm_state": ["id INTEGER PRIMARY KEY", "state TEXT"],
    "goal_history": ["id INTEGER PRIMARY KEY", "goal_id INTEGER", "date_completed DATE", "status TEXT"]
}

def add_goal(description, deadline, status):
    # Implementation here
    pass

def get_today_goals():
    # Implementation here
    pass

def complete_goal(goal_id):
    # Implementation here
    pass

def get_goal_stats():
    # Implementation here
    pass

def add_fsm_state(state):
    # Implementation here
    pass

def get_fsm_state(state_id):
    # Implementation here
    pass

def delete_fsm_state(state_id):
    # Implementation here
    pass

def add_user_settings(user_id, settings):
    # Implementation here
    pass

def get_user_settings(user_id):
    # Implementation here
    pass
