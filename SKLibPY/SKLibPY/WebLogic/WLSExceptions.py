class WLSException(Exception):
    """Superclass for exceptions thrown by this module"""
    print(Exception)
    pass


class BadRequestException(WLSException):
    """
    A REST method returns 400 (BAD REQUEST) if the request failed because
    something is wrong in the specified request, for example, invalid argument values.
    """
    pass


class UnauthorizedException(WLSException):
    """
    A REST method returns 401 (UNAUTHORIZED) if the user does not have permission
    to perform the operation. 401 is also returned if the user supplied incorrect
    credentials (for example, a bad password).
    """
    pass


class ForbiddenException(WLSException):
    """
    A REST method returns 403 (FORBIDDEN) if the user is not in the ADMIN,
    OPERATOR, DEPLOYER or MONITOR role.
    """
    pass


class NotFoundException(WLSException):
    """
    A REST method returns 404 (NOT FOUND) if the requested URL does not refer to an
    existing entity.
    """
    pass


class MethodNotAllowedException(WLSException):
    """
    A REST method returns 405 (METHOD NOT ALLOWED) if the resource exists but
    does not support the HTTP method, for example, if the user tries to create a server by
    using a resource in the domain configuration tree (only the edit tree allows
    configuration editing).
    """
    pass


class NotAcceptableException(WLSException):
    """
    The resource identified by this request is not capable of generating a representation
    corresponding to one of the media types in the Accept header of the request. For
    example, the client's Accept header asks for XML but the resource can only return
    JSON.
    """
    pass


class ServerErrorException(WLSException):
    """
    A REST method returns 500 (INTERNAL SERVER ERROR) if an error occurred that
    is not caused by something wrong in the request. Since the REST layer generally
    treats exceptions thrown by the MBeans as BAD REQUEST, 500 is generally used for
    reporting unexpected exceptions that occur in the REST layer. These responses do not
    include the text of the error or a stack trace, however, generally they are logged in the
    server log.
    """
    pass


class ServiceUnavailableException(WLSException):
    """
    The server is currently unable to handle the request due to temporary overloading or
    maintenance of the server. The WLS REST web application is not currently running.
    """
    pass