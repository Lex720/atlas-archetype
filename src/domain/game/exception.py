class GameNotFoundError(Exception):
    """Custom exception class for game not found errors.

    Note:
        GameNotFoundError is an error that occurs when a game does not exist.
    """

    message = "Game does not exist."

    def __str__(self) -> str:
        """This method sets the error message taht need to be returned.

        Returns:
            Error message in string type form.
        """
        return GameNotFoundError.message
