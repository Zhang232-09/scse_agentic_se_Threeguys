def decide_next_move(state):
    if state['goal_ahead']:
        if not state['front_blocked']:
            return "FORWARD"
        else:
            if not state['left_blocked']:
                return "LEFT"
            elif not state['right_blocked']:
                return "RIGHT"
            else:
                return "STOP"
    elif state['goal_on_left']:
        if not state['left_blocked']:
            return "LEFT"
        else:
            if not state['front_blocked']:
                return "FORWARD"
            elif not state['right_blocked']:
                return "RIGHT"
            else:
                return "STOP"
    elif state['goal_on_right']:
        if not state['right_blocked']:
            return "RIGHT"
        else:
            if not state['front_blocked']:
                return "FORWARD"
            elif not state['left_blocked']:
                return "LEFT"
            else:
                return "STOP"
    else:
        return "STOP"



### 🧠 Notes


