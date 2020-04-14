var memberLoginBtn = document.getElementById('member-login-btn');
memberLoginBtn.addEventListener("click", function() {
    document.getElementById('id01').style.display='block';
});

var closeModalBtn = document.getElementById('close-modal-btn');
closeModalBtn.addEventListener("click", function()  {
    document.getElementById('id01').style.display='none';
});

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
        alert("Login successful");
    }
    else
    {
        alert("Faulty username or Password");
    }
}