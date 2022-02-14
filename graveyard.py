
# Do event based on time passed from last time the event ran
time_since += clock.tick(frames)
        if time_since > simple_clickers/60:
            cookie_count += simple_clickers * 0.016
            time_since = 0
