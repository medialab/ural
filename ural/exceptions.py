class UralError(Exception):
    pass


class TLDUpgradeError(UralError):
    def __init__(self, message, reason):
        super(TLDUpgradeError, self).__init__(message)
        self.reason = reason
