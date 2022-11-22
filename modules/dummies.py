

def generate_dummypage(page_activity_name):
    """Generates dummy-page for some activity"""
    if len(page_activity_name) == 0:
        page_activity_name = 'page for something important'
    return f"<h2>Welcome to {page_activity_name} page!</h2>"

def generate_notadmin_page():
    """Generates template for page showing that current user is not an administrator"""
    return "<h2>You aren't an administrator! You may not use admin panel!</h2>"
