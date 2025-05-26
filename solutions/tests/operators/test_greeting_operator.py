from operators.greeting import GreetingOperator


def test_greeting_operator():
    task = GreetingOperator(
        task_id="greeting",
        greeting="Hello",
        name="World",
    )
    result = task.execute(context={})
    assert result == "Hello, World"