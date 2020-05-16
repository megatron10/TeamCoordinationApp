let loginBtn = document.getElementById("login-btn");

loginBtn.addEventListener("click", function() {
    let username = document.getElementById("usrname").value;
    let password = document.getElementById("pswrd").value;

    login(username, password);
});


function absolute(base, relative) {
    let stack = base.split("/"),
        parts = relative.split("/");
    stack.pop(); // remove current file name (or empty string)
    for (var i=0; i<parts.length; i++) {
        if (parts[i] == ".")
            continue;
        if (parts[i] == "..")
            stack.pop();
        else
            stack.push(parts[i]);
    }
    return stack.join("/");
}


function createLoginObject(username, password) {
    return JSON.stringify({'username': username, 'transformed_password': password })
}

function parseLoginResponse(response) {
    return JSON.parse(response);
}

function login(username, password){
    console.log("[login] Making logging request");
    let conn;
    try {
        conn = getAuthenticatorConnection();
    } catch (e) {
        console.error("[login] Security Error", e);
    }

    conn.onopen = function(ev) {
        console.log("[login] Connection established with authenticator");
        let loginObject = createLoginObject(username, password);
        console.log("[login] Sending login credentials");
        conn.send(loginObject);
        console.log("[login] Credential sent");
    }

    conn.onmessage = function (ev) {
        console.debug("[login] Message received from authenticator", ev);
        
        let response = parseLoginResponse(ev.data);
        // Case when credentials are wrong
        if(response['status'] == 0) {
            ///TODO: Invalid credentials
            console.debug("[login] Invalid Credentials");
        }
        else {
            localStorage.setItem('uid', username);
            localStorage.setItem('sid', response['sid']);
            console.debug('[login] Login successful, saving cookie');

            console.log("[login] Closing connection with authenticator");
            conn.close();

            // Promoting to user's page
            let loc = absolute(window.location.href, "chat.html");
            location.assign(loc);
        }
    }
    
    conn.onerror = function(ev) {
        console.error("[login] WebSocket error observed:", ev);
        console.error("[login] Server endpoint is down or inactive");
    }
    
    conn.onclose = function(ev) {
        console.log("[login] WebSocket is closed now.", ev);
    }

}

