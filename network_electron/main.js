console.log('main process wokign ');

const { BrowserWindow,app } = require('electron');
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
            nodeIntegration: true
        },
    });
    
    winone.loadURL(url.format({
        pathname: path.join(__dirname, 'html/index.html'),
        protocol: 'file',
        slashes: true 
    }));
    
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