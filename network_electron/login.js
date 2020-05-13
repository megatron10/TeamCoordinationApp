var loginBtn = document.getElementById("login-btn");
loginBtn.addEventListener("click", function() {
    var username = document.getElementById("usrname").value;
    var password = document.getElementById("pswrd").value;
    check(username, password);
});
 
function check(username, password)
{
    if (username == 'bill' && password == 'cosby')
    {
        location.replace(`file:///home/deeptanshu/Templates/CN_project/networks-electron/html/chat.html`);
    }
    else
    {
        alert("unauthenticated");
    }    
}
