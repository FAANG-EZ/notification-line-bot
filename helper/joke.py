import jokekappa

from logger.logger import logger


class Joke:
    def __init__(self):
        pass

    def generate_joke(self, custom_message=""):
        try:
            joke = jokekappa.get_joke()
            return custom_message + joke['content']
        except Exception as e:
            error_message = "An unexpected error occurred on grnerate joke: " + str(e)
            logger.error(error_message)