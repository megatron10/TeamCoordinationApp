var content = {}; // channel name to message list dict
var currentsel = ""
let uid = localStorage.getItem('uid');
let sid = localStorage.getItem('sid');
onlines = new Set()

function setfocus(channelname){

  //console.log(currentsel);
  if (currentsel === ""){
    //pass
  }
  else {
    content[currentsel].style.display = "none";
  }
  content[channelname].style.display = "block";
  currentsel = channelname
  span = '<span class="glyphicon glyphicon-comment"></span>'
  document.getElementById('topheading').innerHTML = span +
    ' Messages for ' + channelname; 

}
function hover(element) {
  username = element.innerHTML.split(" ")[0]
  if (onlines.has(username)){
    status = username+' is online'
  }
  else {
    status = username + ' is offline'
  }
  element.setAttribute('title', 
  status + ' and this message was sent at '+ element.getAttribute('data-time'));
}

function packagemsg(by, msg, on){
  var node = document.createElement("LI");
  node.setAttribute('onmouseover', 'hover(this)')
  node.setAttribute('data-time', on);
  var textnode = document.createTextNode(by + ' : '+ msg); 
  node.appendChild(textnode);
  node.setAttribute("class", "list-group-item");
  return node
}

function getmsg(channel) {
  //console.log(channel)
  
  content[channel] = document.createElement("UI");
  content[channel].setAttribute("id", "channel-list");
  content[channel].setAttribute("class", "list-group");
  content[channel].style.display = "none";

  let socket = getHistoryServiceConnection();
  socket.onopen = function(e) {
    // TODO update uid and sid
    data = {'uid': uid, 'sid': sid, 'channel':channel}
    socket.send(JSON.stringify(data));
  };

  socket.onmessage = function(event) {
    msglist = JSON.parse(event.data)['ret']
    for (var i = msglist.length -1 ; i >=0 ; i--) {
      content[channel].appendChild(packagemsg(msglist[i][0], msglist[i][1], msglist[i][2]));
    }
  };

  // socket.onclose = function(event) {
  //   if (event.wasClean) {console.log(` ch-msg[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);}
  //   else { console.log(' ch-msg[close] Connection died');}
  // };

  // socket.onerror = function(error) {
  //   console.log(` ch-msg[error] ${error.message}`);
  // };
}

function chonclick(element) {
  //console.log();
  setfocus(element.children[0].textContent);
}

function getchannels() {
  let channelsocket = getChannelServiceConnection();

  channelsocket.onopen = function(e) {
    data = {'uid': uid, 'sid': sid}
    channelsocket.send(JSON.stringify(data));
  };
  
  channelsocket.onmessage = function(event) {
    
    channellist = JSON.parse(event.data)['list']
    for (var i = 0; i < channellist.length; i++) {
      content[channellist[i]] = []
      var button = document.createElement('button')
      var node = document.createElement("LI");
      var textnode = document.createTextNode(channellist[i]); 
      node.appendChild(textnode);
      node.setAttribute("style", "text-align: center;");
      node.setAttribute("class", "list-group-item");
      button.appendChild(node)
      button.setAttribute('onclick', 'chonclick(this)')
      document.getElementById("channel-list").appendChild(button);
      getmsg(channellist[i])
      document.getElementById("msg-box").appendChild(content[channellist[i]]);
    }
    setfocus(channellist[0])
    // content[channellist[0]].style.display = "block";
    // currentsel = channellist[0]
  };
  
  // channelsocket.onclose = function(event) {
  //   if (event.wasClean) {
  //     console.log(`[close] Connection closed cleanly,
  //     code=${event.code} reason=${event.reason}`);
  //   } else {
  //     console.log('[close] Connection died');
  //   }
  // };
  
  // channelsocket.onerror = function(error) {
  //   console.log(`[error] ${error.message}`);
  // };
}

function sendMessage() {
    message = document.getElementById('inpmsg').value;
    // send message to currentsel channel
    document.getElementById('inpmsg').value = "";
}

getchannels()


let onlinesocket = getOnlineServiceConnection();
onlines.add(uid)

  onlinesocket.onopen = function(e) {
    data = {'uid': uid, 'sid': sid, 'action': 'connect'}
    console.log(data)
    onlinesocket.send(JSON.stringify(data));
  };
  
  onlinesocket.onmessage = function(event) {
    data =  JSON.parse(event.data)
    console.log(data)
    if (data['action'] === 'list'){
      onlinelist = data['message']
      console.log(onlinelist)
      for (var i = 0; i < onlinelist.length; i++) {
        console.log('online '+ onlinelist[i]);
        onlines.add(onlinelist[i]);
      }
    }
    if(data['action'] === 'update') {
      if (data['status'] === 'offline'){
        onlines.delete(data['uid'])
      }
      if (data['status'] === 'online'){
         onlines.add(data['uid'])
      }
    }
  };