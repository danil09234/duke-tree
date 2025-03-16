class SessionNotFoundError(Exception):
    """Raised when a session cannot be found by its ID."""
    pass

class InvalidAnswerError(Exception):
    """Raised when an answer provided does not match available options."""
    pass

class NodeNotFoundError(Exception):
    """Raised when a node ID is not found in the tree mapping."""
    pass

class HistoryEmptyError(Exception):
    """Raised when attempting to access history that is empty."""
    pass

class AnswerTokenNotFound(Exception):
    """Raised when an answer token is not found in the tree mapping."""
    pass
