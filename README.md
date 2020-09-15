# Team Coordination App
To help plan and execute projects remotely. Several similar applications have
been made that are used as references including Slack, Microsoft teams, etc...

## Getting Started

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes. 

### Prerequisites


* ```npm```

* python **websocket** package


### Running the client side of the code.

Follow the following steps to get the client up and running.

* Make sure the server is up and running. Otherwise the client won't be able to connect and authenticate the user.
* Go to the **client source directory** i.e. computer-networks

  ``` cd computer-networks ```
* Execute the following command to install all the client-side dependencies.  

  ``` npm install ```
* Replace the **host** variable at line 4/5 in **./scripts/util.js** with server **address**. 
* To launch the app in **browser** mode, open **./html/login.html** in any browsers.
* To launch the app in **Desktop** mode, execute in the **client source directory**:

  ```npm start```


## Login info
by default there are 9 users
"dhananjay","sahil","vijay","anjani"
,"jatin","anupam","tungadri","deeptanshu","phoenix"
and passwords for them are "pass"+username

## Built With

* [WebSockets](https://pypi.org/project/websockets/) - Python WebSocket package
* [npm](https://www.npmjs.com/) - Node package manager

## Authors

* **Anjani Kumar** - [Github](https://github.com/anjani-1)  
* **Dhananjay Raut** - [Github](https://github.com/dhananjayraut)
* **Deeptanshu Sankhwar** - [Github](https://github.com/Deeptanshu-sankhwar)
* **Sahil Shah** - [Github](https://github.com/megatron10/)
* **Vijay Tadikamalla** - [Github](https://github.com/vijayphoenix)
* **Anupam Saini** - [Github](https://github.com/anupamsaini98)
* **Tungadri Mandal**
* **Jatin Sharma**
