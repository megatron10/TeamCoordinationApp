// let ChatRoomBtn = document.getElementById("ChatRoom-btn");

// ChatRoomBtn.addEventListener("click", function () {
//     let username = document.getElementById("usrname").value;
//     let password = document.getElementById("pswrd").value;

//     ChatRoom(username, password);
// });

let uid = localStorage.getItem('uid');
let sid = localStorage.getItem('sid');
let conn;
try {
    conn = getChattingConnection();
} catch (e) {
    console.error("[ChatRoom] Security Error", e);
}

function createChattingObject(uid, sid, channel, action, message) {
    return JSON.stringify({ 'uid': uid, 'sid': sid, 'channel': channel, 'action': action, 'message': message })
}



conn.onopen = function (ev) {
    console.log("[ChatRoom] Connection established with ChatRoom");
    // Creating a connect query
    createChattingObject(uid, sid, "channelX", "connect", "messageNull");
    console.log("[ChatRoom] Sent connect for initial connection");

    // let ChatRoomObject = createChatRoomObject(username, password);
    // console.log("[ChatRoom] Sending ChatRoom credentials");
    // conn.send(ChatRoomObject);
    // console.log("[ChatRoom] Credential sent");
}


conn.onmessage = function (ev) {
    console.debug("[ChatRoom] Message received from authenticator", ev);

    // Updating channel with the message
    
    // let response = parseChatRoomResponse(ev.data);
    // // Case when credentials are wrong
    // if (response['status'] == 0) {
    //     ///TODO: Invalid credentials
    //     console.debug("[ChatRoom] Invalid Credentials");
    // }
    // else {
    //     localStorage.setItem('uid', username);
    //     localStorage.setItem('sid', response['sid']);
    //     console.debug('[ChatRoom] ChatRoom successful, saving cookie');

    // console.log("[ChatRoom] Closing connection with authenticator");
    // conn.close();

    // Promoting to user's page
    // let loc = absolute(window.location.href, "chat.html");
    // location.assign(loc);
    // }
}

conn.onerror = function (ev) {
    console.error("[ChatRoom] WebSocket error observed:", ev);
    console.error("[ChatRoom] Server endpoint is down or inactive");
}

conn.onclose = function (ev) {
    console.log("[ChatRoom] WebSocket is closed now.", ev);
}



function absolute(base, relative) {
    let stack = base.split("/"),
        parts = relative.split("/");
    stack.pop(); // remove current file name (or empty string)
    for (var i = 0; i < parts.length; i++) {
        if (parts[i] == ".")
            continue;
        if (parts[i] == "..")
            stack.pop();
        else
            stack.push(parts[i]);
    }
    return stack.join("/");
}


function createChattingObject(uid, sid, channel, action, message) {
    return JSON.stringify({ 'uid': uid, 'sid': sid, 'channel': channel, 'action':action, 'message':message })
}

function parseChattingResponse(response) {
    return JSON.parse(response);
}

function registerForUpdate() {
    console.log("[ChatRoom] Making logging request");
    let conn;
    try {
        conn = getChattingConnection();
    } catch (e) {
        console.error("[ChatRoom] Security Error", e);
    }

    conn.onopen = function (ev) {
        console.log("[ChatRoom] Connection established with authenticator");
        // Creating a connect query

        // let ChatRoomObject = createChatRoomObject(username, password);
        // console.log("[ChatRoom] Sending ChatRoom credentials");
        // conn.send(ChatRoomObject);
        // console.log("[ChatRoom] Credential sent");
    }

    conn.onmessage = function (ev) {
        console.debug("[ChatRoom] Message received from authenticator", ev);

        // let response = parseChatRoomResponse(ev.data);
        // // Case when credentials are wrong
        // if (response['status'] == 0) {
        //     ///TODO: Invalid credentials
        //     console.debug("[ChatRoom] Invalid Credentials");
        // }
        // else {
        //     localStorage.setItem('uid', username);
        //     localStorage.setItem('sid', response['sid']);
        //     console.debug('[ChatRoom] ChatRoom successful, saving cookie');

            // console.log("[ChatRoom] Closing connection with authenticator");
            // conn.close();

            // Promoting to user's page
            // let loc = absolute(window.location.href, "chat.html");
            // location.assign(loc);
        // }
    }

    conn.onerror = function (ev) {
        console.error("[ChatRoom] WebSocket error observed:", ev);
        console.error("[ChatRoom] Server endpoint is down or inactive");
    }

    conn.onclose = function (ev) {
        console.log("[ChatRoom] WebSocket is closed now.", ev);
    }

}

