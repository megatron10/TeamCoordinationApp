# Team Coordination App
To help plan and execute projects remotely. Several similar applications have been made that are used as references including Slack, Microsoft teams, etc...

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites


* ```npm```

* python **websocket** package


### Running the server side of the code.

Follow the following steps to get the server up and running.

* Go to the **server source directory** i.e. **scb**

  ``` cd scb ```
* Let **addr** be the address where you want to host the server on.
  
* Replace the **url** variable at line 4/5 in **main.py** with **addr**. 

* Make sure the port from **9001** to **9006** are available at the **addr**.

* Setup the database, execute in the **server source directory**:

  ```python3 db.py```

* To start the server, execute in the **server source directory**:

  ```python3 main.py```


## On successful startup, you should see the message like:
```
ID of main process: 25143
ID of process running process4: 25147
ID of process running process1: 25144
ID of process running process6: 25149
ID of process running process2: 25145
ID of process running process5: 25148
ID of process running process3: 25146
```


## Quick Instructions

```
git clone https://github.com/dhananjayraut/scb
git clone https://github.com/Deeptanshu-sankhwar/computer-networks

pip install websockets

python scb/db.py   # Setup db
python scb/main.py # Start server
```

Follow instructions on https://github.com/Deeptanshu-sankhwar/computer-networks to login


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






