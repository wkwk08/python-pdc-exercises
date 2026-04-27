import time

def order():
    print("Order received")
    time.sleep(1)

def payment():
    print("Payment processed")
    time.sleep(1)

def shipping():
    print("Order shipped")

def test_workflow():
    print("--- Task Workflow Observation ---")
    # Executing the functions in a strict, coordinated order
    order()
    payment()
    shipping()

if __name__ == '__main__':
    test_workflow()