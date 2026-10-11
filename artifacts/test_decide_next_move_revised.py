import pytest
from navigation_logic import decide_next_move

def test_forward():
    state = {'goal_ahead': True, 'front_blocked': False, 'goal_on_left': False, 'left_blocked': False, 'goal_on_right': False, 'right_blocked': False}
    assert decide_next_move(state) == "FORWARD"

def test_left():
    state = {'goal_ahead': False, 'front_blocked': False, 'goal_on_left': True, 'left_blocked': False, 'goal_on_right': False, 'right_blocked': False}
    assert decide_next_move(state) == "LEFT"

def test_right():
    state = {'goal_ahead': False, 'front_blocked': False, 'goal_on_left': False, 'left_blocked': False, 'goal_on_right': True, 'right_blocked': False}
    assert decide_next_move(state) == "RIGHT"

def test_stop_goal_not_found():
    state = {'goal_ahead': False, 'front_blocked': False, 'goal_on_left': False, 'left_blocked': False, 'goal_on_right': False, 'right_blocked': False}
    assert decide_next_move(state) == "STOP"

def test_stop_path_blocked():
    state = {'goal_ahead': True, 'front_blocked': True, 'goal_on_left': False, 'left_blocked': False, 'goal_on_right': False, 'right_blocked': False}
    assert decide_next_move(state) == "STOP"