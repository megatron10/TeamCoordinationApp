function chattingSystem() {
    let conn;
    try {
        conn = getChattingConnection();
    } catch (e) {
        console.error("[ChatRoom] Security Error", e);
    }

    function createChattingObject(uid, sid, channel, action, message) {
        return JSON.stringify({ 'uid': uid, 'sid': sid, 'channel': channel, 'action': action, 'message': message })
    }

    function parseChattingResponse(response) {
        return JSON.parse(response);
    }


    conn.onopen = function (ev) {
        console.log("[ChatRoom] Connection established with ChatRoom");
        // Creating a connect query
        let uid = localStorage.getItem('uid');
        let sid = localStorage.getItem('sid');

        data = createChattingObject(uid, sid, "channel0", "connect", "messageNull");
        conn.send(data);
        console.log("[ChatRoom] Sent connect for initial connection");

    }


    let echoBack = true;
    conn.onmessage = function (ev) {
        console.debug("[ChatRoom] Message received from Chat Server", ev);
        if (echoBack) {
            echoBack = false;
            console.debug("[ChatRoom] Received echoBack", ev);
        }
        else {
            response = parseChattingResponse(ev.data);
            // Updating channel with the message

            content[response['channel']].appendChild(packagemsg(
                response['from_uid'], response['message']
            ));

        }
    }

    conn.onerror = function (ev) {
        console.error("[ChatRoom] WebSocket error observed:", ev);
        console.error("[ChatRoom] Server endpoint is down or inactive");
    }

    conn.onclose = function (ev) {
        console.log("[ChatRoom] WebSocket is closed now.", ev);
    }

    
    let sendBtn = document.getElementById("send-button");
    sendBtn.addEventListener("click", function () {
        var input = document.getElementById("inpmsg");
        var msg = input.value
        console.log("[Chatroom] Send button fired", msg);
        if(msg != "") {
            console.log("[Chatroom] Sending message to server:", msg, "Channel:", currentsel);
            content[currentsel].appendChild(packagemsg(
                uid, msg
            ));
            data = createChattingObject(uid, sid, currentsel, "send", msg);
            conn.send(data);
            input.value = "";
        }
    });


    document.getElementById("inpmsg")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        document.getElementById("send-button").click();
    }
    });
}

chattingSystem();
 