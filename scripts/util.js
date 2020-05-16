'use strict';

var authenticator_host = "ws://127.0.0.1";
var authenticator_port = "9006";

function getAuthenticatorConnection() {
    return (new WebSocket(authenticator_host + ":" + authenticator_port));
}

// var 