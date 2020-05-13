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

function check(username, password)
{
    if (username == 'bill' && password == 'cosby')
    {
        loc = absolute(absFileLoc("login.js"), "html/chat.html")
        location.replace(loc);
    }
    else
    {
        alert("unauthenticated");
    }    
}
