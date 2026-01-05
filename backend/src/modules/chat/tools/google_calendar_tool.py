from langchain_google_community import CalendarToolkit

# Assuming credentials.json is in the same directory or configured properly
toolkit = CalendarToolkit()

# Get all available tools
google_calendar_tools = toolkit.get_tools()
