def is_goal_ahead():
    return True  # Simulated

def is_obstacle_ahead():
    return False  # Simulated

def is_obstacle_left():
    return False  # Simulated

def is_obstacle_right():
    return False  # Simulated

def move_forward():
    print("Moving forward")

def turn_left():
    print("Turning left")

def turn_right():
    print("Turning right")

def stop_robot():
    print("Stopping robot")

def navigate_robot():
    while True:
        if is_goal_ahead() and not is_obstacle_ahead():
            move_forward()
            stop_robot()
            break
        elif is_obstacle_ahead():
            if not is_obstacle_left():
                turn_left()
            elif not is_obstacle_right():
                turn_right()
        else:
            move_forward()