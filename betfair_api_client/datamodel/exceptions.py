
class ErrorCodes:

    JSON_PARSE_FAILURE = 'DSC-0008'
    INVALID_FORMAT_FOR_PARAMETER = 'DSC-0009'
    SECURITY_EXCEPTION = 'DSC-0015'
    PARAMETER_NOT_DEFINED = 'DSC-0018'
    TIMEOUT = 'DSC-0019'
    NO_SUCH_OPERATION = 'DSC-0021'
    NO_SUCH_SERVICE = 'DSC-0023'
    DESERIALISATION_FAILURE = 'DSC-0024'
    UNKNOWN_CALLER = 'DSC-0034'
    UNRECOGNIZED_CREDENTIALS = 'DSC-0035'
    INVALID_CREDENTIALS = 'DSC-0036'
    SUBSCRIPTION_REQUIRED = 'DSC-0037'
    OPERATION_FORBIDDEN = 'DSC-0038'
    TOO_MUCH_DATA = 'ANGX-0001'
    NOT_ENOUGH_FUNDS = 'INSUFFICIENT_FUNDS'


class BetfairException(BaseException):

    def __init__(self, betfairExceptionCode):

        if betfairExceptionCode == ErrorCodes.JSON_PARSE_FAILURE:
            raise JsonParseFailure

        elif betfairExceptionCode == ErrorCodes.INVALID_FORMAT_FOR_PARAMETER:
            raise InvalidFormatForParameter

        elif betfairExceptionCode == ErrorCodes.SECURITY_EXCEPTION:
            raise SecurityException

        elif betfairExceptionCode == ErrorCodes.PARAMETER_NOT_DEFINED:
            raise ParameterNotDefined

        elif betfairExceptionCode == ErrorCodes.TIMEOUT:
            raise TimeoutException

        elif betfairExceptionCode == ErrorCodes.NO_SUCH_OPERATION:
            raise NoSuchOperation

        elif betfairExceptionCode == ErrorCodes.NO_SUCH_SERVICE:
            raise NoSuchService

        elif betfairExceptionCode == ErrorCodes.DESERIALISATION_FAILURE:
            raise DeserializationError

        elif betfairExceptionCode == ErrorCodes.UNKNOWN_CALLER:
            raise UnknownCaller

        elif betfairExceptionCode == ErrorCodes.UNRECOGNIZED_CREDENTIALS:
            raise UnrecognizedCredentials

        elif betfairExceptionCode == ErrorCodes.INVALID_CREDENTIALS:
            raise InvalidCredentials

        elif betfairExceptionCode == ErrorCodes.SUBSCRIPTION_REQUIRED:
            raise SubscriptionRequired

        elif betfairExceptionCode == ErrorCodes.OPERATION_FORBIDDEN:
            raise OperationForbidden

        elif betfairExceptionCode == ErrorCodes.TOO_MUCH_DATA:
            raise TooMuchData

        elif betfairExceptionCode == ErrorCodes.NOT_ENOUGH_FUNDS:
            raise NotEnoughFunds


class JsonParseFailure(Exception):
    pass


class InvalidFormatForParameter(Exception):
    pass


class SecurityException(Exception):
    pass


class ParameterNotDefined(Exception):
    pass


class TimeoutException(Exception):
    pass


class NoSuchOperation(Exception):
    pass


class NoSuchService(Exception):
    pass


class DeserializationError(Exception):
    pass


class UnknownCaller(Exception):
    pass


class UnrecognizedCredentials(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class SubscriptionRequired(Exception):
    pass


class OperationForbidden(Exception):
    pass


class TooMuchData(Exception):
    pass


class NotEnoughFunds(Exception):
    pass
