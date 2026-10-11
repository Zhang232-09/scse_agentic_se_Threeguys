def decide_next_move(state):
    if state['goal_ahead'] and not state['front_blocked']:
        return "FORWARD"
    elif state['goal_on_left'] and not state['left_blocked']:
        return "LEFT"
    elif state['goal_on_right'] and not state['right_blocked']:
        return "RIGHT"
    else:
        if not state['front_blocked'] or not state['left_blocked'] or not state['right_blocked']:
            # Try to move toward the goal if any direction is unblocked
            if not state['front_blocked']:
                return "FORWARD"
            elif not state['left_blocked']:
                return "LEFT"
            elif not state['right_blocked']:
                return "RIGHT"
        else:
            return "STOP"



### 📌 Explanation of Key Decisions




