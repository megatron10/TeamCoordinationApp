console.log('main process woking ');

const { BrowserWindow, app } = require('electron');
const path = require("path");
const url = require("url");

let winone;
let win;

function createWindow() {
    winone = new BrowserWindow({
        width: 800,
        height: 720, 
        webPreferences: {
            nativeWindowOpen: true,
            nodeIntegration: true,
            enableRemoteModule: true
        },
    });
    
    winone.loadURL(`file://${__dirname}/html/login.html`);
    
    // winone.webContents.openDevTools();
    
    winone.on('closed', () => {
        winone = null;
    })  
    
    
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')  {
        app.quit()
    }
});

app.on('activate', () => {
    if (winone === null)   {
        createWindow()
    }
});  
