from typing import Optional

from requests import Session


# pylint: disable=too-few-public-methods
class ConnectionHandler:
    """
    This class is a singleton class that returns a session object
    """

    def __init__(self):
        """
        Initialize the ConnectionHandler object
        """
        self.session = Session()

    @staticmethod
    def get_instance() -> Session:
        """
        Get the session object
        :return: The session object
        """
        global _connection_handler_instance  # pylint: disable=global-statement
        if _connection_handler_instance is None:
            _connection_handler_instance = ConnectionHandler()
        return _connection_handler_instance.session

    @staticmethod
    def set_instance(session: Session):
        """
        Set the session object
        :param session: The session object
        """
        global _connection_handler_instance  # pylint: disable=global-statement
        if _connection_handler_instance is None:
            _connection_handler_instance = ConnectionHandler()
        _connection_handler_instance.session = session


_connection_handler_instance: Optional[ConnectionHandler] = None  # pylint: disable=invalid-name
