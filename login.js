var loginBtn = document.getElementById("login-btn");
loginBtn.addEventListener("click", function() {
    var username = document.getElementById("usrname").value;
    var password = document.getElementById("pswrd").value;
    check(username, password);
});

function absFileLoc(filename) {
    var scriptElements = document.getElementsByTagName('script');
    for (var i = 0; i < scriptElements.length; i++) {    
        var source = scriptElements[i].src;
        if (source.indexOf(filename) > -1) {
            var location = source.substring(0, source.indexOf(filename)) + filename;
            return location;
        }
    }
    return false;
}

function absolute(base, relative) {
    var stack = base.split("/"),
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

//function check(username, password)
//{
//    document.cookie = "username=John Smith; expires=Thu, 18 Dec 2023 12:00:00 UTC; path=/";
//    if (username == 'bill' && password == 'cosby')
//    {
//        loc = absolute(absFileLoc("login.js"), "html/chat.html")
//        location.replace(loc);
//    }
//    else
//    {
//        alert("unauthenticated");
//    }
//}

function check(username, password){
    let socket = new WebSocket("ws://127.0.0.1:9006");
    var data = {'username':username, 'transformed_password': password}
    socket.onopen = function(e) {
      //alert("[open] Connection established");
      //alert("Sending to server");
      socket.send(JSON.stringify(data)); 
      console.log(data);
        //socket.send("My name is John");
    };

    socket.onmessage = function(event) {
      data = JSON.parse(event.data)
      console.log(`[message] Data received from server: ${event.data}`);
      if (data['status'] == 1)
      {
         cookie =  {'sid':data['sid'], 'uid':username}
         // TODO cookie
         loc = absolute(absFileLoc("login.js"), "html/chat.html")
         location.replace(loc);
      }
      else
      {
         alert("unauthenticated");
      }
    };

    socket.onclose = function(event) {
      if (event.wasClean) {
        alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
      } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        alert('[close] Connection died');
      }
    };

    socket.onerror = function(error) {
      alert(`[error] ${error.message}`);
    };
}
