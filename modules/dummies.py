

def generate_dummypage(page_activity_name):
    """Generates dummy-page for some activity"""
    if len(page_activity_name) == 0:
        page_activity_name = 'page for something important'
    return f"<h2>Welcome to {page_activity_name} page!</h2>"
