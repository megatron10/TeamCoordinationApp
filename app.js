var content = {}; // channel name to message list dict
var currentsel = ""

function setfocus(channelname){
  if (currentsel != ""){
    content[channelname].style.display = "hidden";
  }
  content[channelname].style.display = "block";
  currentsel = channelname

}

function packagemsg(by, msg){
  var node = document.createElement("LI");
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

  let socket = new WebSocket("ws://localhost:9001");
  socket.onopen = function(e) {
    // TODO update uid and sid
    data = {'uid': 'dhananjay', 'sid': 'asdasd', 'channel':channel}
    socket.send(JSON.stringify(data));
  };

  socket.onmessage = function(event) {
    msglist = JSON.parse(event.data)['ret']
    for (var i = 0; i < msglist.length; i++) {
      console.log(msglist[i])
      content[channel].appendChild(packagemsg(msglist[i][0], msglist[i][1]));
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

function getchannels() {
  let channelsocket = new WebSocket("ws://localhost:9005");

  channelsocket.onopen = function(e) {
    data = {'uid': 'dhananjay', 'sid': 'asdasd'}
    channelsocket.send(JSON.stringify(data));
  };
  
  channelsocket.onmessage = function(event) {
    
    channellist = JSON.parse(event.data)['list']
    for (var i = 0; i < channellist.length; i++) {
      content[channellist[i]] = []
      var node = document.createElement("LI");
      var textnode = document.createTextNode(channellist[i]); 
      node.appendChild(textnode);
      node.setAttribute("style", "text-align: center;");
      node.setAttribute("class", "list-group-item");
      document.getElementById("channel-list").appendChild(node);
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

getchannels()