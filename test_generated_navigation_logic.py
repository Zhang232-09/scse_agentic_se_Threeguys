import sys
sys.path.insert(0, "./artifacts")
from navigation_logic import decide_next_move

VALID_ACTIONS = {"FORWARD", "LEFT", "RIGHT", "STOP"}

test_cases = [
    (
        {"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
         "front_blocked": False, "left_blocked": False, "right_blocked": False},
        "FORWARD"
    ),
    (
        {"goal_ahead": False, "goal_on_left": True, "goal_on_right": False,
         "front_blocked": True, "left_blocked": False, "right_blocked": False},
        "LEFT"
    ),
    (
        {"goal_ahead": False, "goal_on_left": False, "goal_on_right": True,
         "front_blocked": True, "left_blocked": False, "right_blocked": False},
        "RIGHT"
    ),
    (
        {"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
         "front_blocked": True, "left_blocked": True, "right_blocked": True},
        "STOP"
    )
]

def run_behavior_tests():
    passed = 0
    failed = 0
    print("===== Behavioral test for decide_next_move(state) =====")
    for idx, (state, expect) in enumerate(test_cases):
        try:
            actual = decide_next_move(state)
        except Exception as e:
            print(f"Test {idx+1} CRASHED: {e}")
            failed +=1
            continue

        if actual not in VALID_ACTIONS:
            print(f"Test {idx+1} FAIL: return invalid action '{actual}'")
            failed +=1
        elif actual == expect:
            print(f"Test {idx+1} PASS: expect={expect}, got={actual}")
            passed +=1
        else:
            print(f"Test {idx+1} FAIL: expect={expect}, got={actual}")
            failed +=1

    print(f"\nSummary: passed={passed}, failed={failed}")
    return failed

if __name__ == "__main__":
    run_behavior_tests()