import logging
import webbrowser
import wsgiref.simple_server
import wsgiref.util

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow, _RedirectWSGIApp, _WSGIRequestHandler


class InstalledAppFlow(Flow):
    """Authorization flow helper for installed applications.

    This :class:`Flow` subclass makes it easier to perform the
    `Installed Application Authorization Flow`_. This flow is useful for
    local development or applications that are installed on a desktop operating
    system.

    This flow uses a local server strategy provided by :meth:`run_local_server`.

    Example::

        from google_auth_oauthlib.flow import InstalledAppFlow

        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=['profile', 'email'])

        flow.run_local_server()

        session = flow.authorized_session()

        profile_info = session.get(
            'https://www.googleapis.com/userinfo/v2/me').json()

        print(profile_info)
        # {'name': '...',  'email': '...', ...}


    Note that this isn't the only way to accomplish the installed
    application flow, just one of the most common. You can use the
    :class:`Flow` class to perform the same flow with different methods of
    presenting the authorization URL to the user or obtaining the authorization
    response, such as using an embedded web view.

    .. _Installed Application Authorization Flow:
        https://github.com/googleapis/google-api-python-client/blob/main/docs/oauth-installed.md
    """

    _DEFAULT_AUTH_PROMPT_MESSAGE = (
        "Please visit this URL to authorize this application: {url}\n\n"
        """After that, execute command
        `docker exec <container name> curl "<localhost url that you've been redirected to>"""
    )
    """str: The message to display when prompting the user for
    authorization."""
    _DEFAULT_AUTH_CODE_MESSAGE = "Enter the authorization code: "
    """str: The message to display when prompting the user for the
    authorization code. Used only by the console strategy."""

    _DEFAULT_WEB_SUCCESS_MESSAGE = "The authentication flow has completed. You may close this window."

    def run_local_server(
        self,
        host: str = "localhost",
        bind_addr: str = None,
        port: int = 8080,
        authorization_prompt_message: str = _DEFAULT_AUTH_PROMPT_MESSAGE,
        success_message: str = _DEFAULT_WEB_SUCCESS_MESSAGE,
        open_browser: bool = True,
        redirect_uri_trailing_slash: bool = True,
        timeout_seconds: int = None,
        **kwargs
    ) -> Credentials:
        """Run the flow using the server strategy.

        The server strategy instructs the user to open the authorization URL in
        their browser and will attempt to automatically open the URL for them.
        It will start a local web server to listen for the authorization
        response. Once authorization is complete the authorization server will
        redirect the user's browser to the local web server. The web server
        will get the authorization code from the response and shutdown. The
        code is then exchanged for a token.

        Args:
            host (str): The hostname for the local redirect server. This will
                be served over http, not https.
            bind_addr (str): Optionally provide an ip address for the redirect
                server to listen on when it is not the same as host
                (e.g. in a container). Default value is None,
                which means that the redirect server will listen
                on the ip address specified in the host parameter.
            port (int): The port for the local redirect server.
            authorization_prompt_message (str | None): The message to display to tell
                the user to navigate to the authorization URL. If None or empty,
                don't display anything.
            success_message (str): The message to display in the web browser
                the authorization flow is complete.
            open_browser (bool): Whether or not to open the authorization URL
                in the user's browser.
            redirect_uri_trailing_slash (bool): whether or not to add trailing
                slash when constructing the redirect_uri. Default value is True.
            timeout_seconds (int): It will raise an error after the timeout timing
                if there are no credentials response. The value is in seconds.
                When set to None there is no timeout.
                Default value is None.
            kwargs: Additional keyword arguments passed through to
                :meth:`authorization_url`.

        Returns:
            google.oauth2.credentials.Credentials: The OAuth 2.0 credentials
                for the user.
        """
        wsgi_app = _RedirectWSGIApp(success_message)
        # Fail fast if the address is occupied
        wsgiref.simple_server.WSGIServer.allow_reuse_address = False
        local_server = wsgiref.simple_server.make_server(
            bind_addr or host, port, wsgi_app, handler_class=_WSGIRequestHandler
        )

        redirect_uri_format = "http://{}:{}/" if redirect_uri_trailing_slash else "http://{}:{}"
        self.redirect_uri = redirect_uri_format.format(host, local_server.server_port)
        auth_url, _ = self.authorization_url(**kwargs)

        if open_browser:
            webbrowser.open(auth_url, new=1, autoraise=True)

        if authorization_prompt_message:
            logging.info(authorization_prompt_message.format(url=auth_url))

        local_server.timeout = timeout_seconds
        local_server.handle_request()

        # Note: using https here because oauthlib is very picky that
        # OAuth 2.0 should only occur over https.
        authorization_response = wsgi_app.last_request_uri.replace("http", "https")
        self.fetch_token(authorization_response=authorization_response)

        # This closes the socket
        local_server.server_close()

        return self.credentials
