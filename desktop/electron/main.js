const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 840,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  win.loadURL('http://127.0.0.1:8787');
}

app.whenReady().then(createWindow);
