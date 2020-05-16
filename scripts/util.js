'use strict';

var authenticator_host = "ws://127.0.0.1";
var authenticator_port = "9006";

function getAuthenticatorConnection() {
    return (new WebSocket(authenticator_host + ":" + authenticator_port));
}

var chatting_host = "ws://127.0.0.1";
var chatting_post = "9002";

function getChattingConnection() {
    return (new WebSocket(chatting_host + ":" + chatting_post));
}
