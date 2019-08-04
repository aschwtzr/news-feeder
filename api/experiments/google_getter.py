from google_alerts import GoogleAlerts

# Create an instance
ga = GoogleAlerts('newssumm0@gmail.com', 'Nine Angry Dwarfs')

# Authenticate your user
ga.authenticate()

# List configured monitors
# ga.list()

# Add a new monitor
ga.create("facial recognition technology", {'delivery': 'RSS'})
ga.create("brooklyn", {'delivery': 'RSS'})
ga.create("eastern seaboard weather", {'delivery': 'RSS'})

# Modify an existing monitor
# ga.modify("89e517961a3148c7:c395b7d271b4eccc:com:en:US", {'delivery': 'RSS', 'monitor_match': 'ALL'})
ga.list()
# Delete a monitor
# ga.delete("89e517961a3148c7:c395b7d271b4eccc:com:en:US")