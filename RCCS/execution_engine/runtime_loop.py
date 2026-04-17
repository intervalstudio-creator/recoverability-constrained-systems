from rccs_adapter import evaluate_message

def demo():
    result = evaluate_message(
        state_visible=True,
        time_to_irreversibility=60,
        time_to_detection=5,
        time_to_response=10,
        time_to_recovery=10,
        dependencies_ok=True,
        challengeable=True,
        correctable=True,
    )
    print(result)

if __name__ == "__main__":
    demo()
