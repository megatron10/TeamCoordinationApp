alert("hi");

var content = {}; // channel name to message list dict

let uid = localStorage.getItem('uid');
let sid = localStorage.getItem('sid');

let channelsocket = new WebSocket("ws://localhost:9005");
channelsocket.onopen = function(e) {
  console.log("[open] Connection established");
  console.log("Sending to server");
  data = {'uid': 'dhananjay', 'sid': 'asdasd'}
  channelsocket.send(JSON.stringify(data));
};

channelsocket.onmessage = function(event) {
  //console.log(`[message] Data received from server: ${event.data}`);
  channellist = JSON.parse(event.data)['list']
  console.log(channellist)
  for (var i = 0; i < channellist.length; i++) {
    content[channellist[i]] = []
    var node = document.createElement("LI");
    var textnode = document.createTextNode(channellist[i]); 
    node.appendChild(textnode);
    node.setAttribute("style", "text-align: center;");
    node.setAttribute("class", "list-group-item");
    document.getElementById("channel-list").appendChild(node);
}
  console.log(content);
};

channelsocket.onclose = function(event) {
  if (event.wasClean) {
    console.log(`[close] Connection closed cleanly,
    code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    console.log('[close] Connection died');
  }
};

channelsocket.onerror = function(error) {
  console.log(`[error] ${error.message}`);
};