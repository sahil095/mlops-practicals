import logging

logging.basicConfig(
    # filename='app.log',
    # filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s -%(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app1.log'),
        logging.StreamHandler()  # logs to console as well
    ]
)

logger = logging.getLogger('ArithemeticApp')

def add(a, b):
    result = a + b
    logging.debug(f"Adding {a} + {b} = {result}")
    return result

def subtract(a, b):
    result = a - b
    logging.debug(f"Subtracting {a} - {b} = {result}")
    return result

def multiply(a, b):
    result = a * b
    logging.debug(f"Multiplying {a} * {b} = {result}")
    return result

def divide(a, b):
    try:
        result = a / b
        logging.debug(f"Dividing {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        logger.error("Cannot divide by 0")
        return None
    

add(2, 3)
subtract(3, 2)
multiply(10, 5)
divide(16, 11)