'use strict';

// var host = "ws://127.0.0.1";
var host = "ws://13.70.2.44";
var authenticator_host = host;
var chatting_host = host;


var history_service_port = "9001";
var online_service_port = "9002";
var chatting_port = "9003";
var channel_service_port = "9005";
var authenticator_port = "9006";

function getAuthenticatorConnection() {
    return (new WebSocket(authenticator_host + ":" + authenticator_port));
}


function getChattingConnection() {
    return (new WebSocket(chatting_host + ":" + chatting_port));
}


function getOnlineServiceConnection() {
    return (new WebSocket(host + ":" + online_service_port));
}

function getHistoryServiceConnection() {
    return (new WebSocket(host + ":" + history_service_port));
}

function getChannelServiceConnection() {
    return (new WebSocket(host + ":" + channel_service_port));
}
