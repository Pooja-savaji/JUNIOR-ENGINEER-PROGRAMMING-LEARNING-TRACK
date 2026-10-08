import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def divide_numbers(a, b):
    logger.info("Dividing %s by %s", a, b)

    try:
        result = a / b
        logger.info("Division successful: %s", result)
        return result

    except ZeroDivisionError:
        logger.error("Cannot divide by zero")
        return None

def main():
    logger.info("Application started")

    divide_numbers(10, 2)
    divide_numbers(10, 0)

    logger.info("Application finished")

main()
