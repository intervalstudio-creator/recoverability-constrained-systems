const { app, BrowserWindow, shell, dialog } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const http = require("http");

let backendProcess = null;

function getBackendCommand() {
  const resources = process.resourcesPath;

  if (process.platform === "win32") {
    return {
      cmd: path.join(resources, "backend", "win", "boundary-backend", "boundary-backend.exe"),
      args: [],
      cwd: path.join(resources, "backend", "win", "boundary-backend")
    };
  }

  if (process.platform === "darwin") {
    return {
      cmd: path.join(resources, "backend", "mac", "boundary-backend", "boundary-backend"),
      args: [],
      cwd: path.join(resources, "backend", "mac", "boundary-backend")
    };
  }

  return {
    cmd: "python3",
    args: [path.join(resources, "api", "server.py")],
    cwd: resources
  };
}

function waitForBackend(url, timeoutMs = 30000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const attempt = () => {
      const req = http.get(url, (res) => {
        res.resume();
        resolve(true);
      });
      req.on("error", () => {
        if (Date.now() - start > timeoutMs) {
          reject(new Error("Backend did not start in time"));
        } else {
          setTimeout(attempt, 800);
        }
      });
      req.setTimeout(2000, () => {
        req.destroy();
        if (Date.now() - start > timeoutMs) {
          reject(new Error("Backend did not start in time"));
        } else {
          setTimeout(attempt, 800);
        }
      });
    };
    attempt();
  });
}

function startBackend() {
  const spec = getBackendCommand();
  backendProcess = spawn(spec.cmd, spec.args, {
    cwd: spec.cwd,
    windowsHide: true
  });

  backendProcess.stdout.on("data", (data) => {
    console.log("[backend]", data.toString());
  });

  backendProcess.stderr.on("data", (data) => {
    console.error("[backend]", data.toString());
  });

  backendProcess.on("exit", (code) => {
    console.log("Backend exited with code", code);
  });
}

async function createWindow() {
  startBackend();

  try {
    await waitForBackend("http://127.0.0.1:8787/api/runtime-status");
  } catch (err) {
    await dialog.showMessageBox({
      type: "error",
      title: "Boundary backend failed",
      message: "The packaged backend did not start automatically.",
      detail: String(err)
    });
  }

  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1100,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  win.loadURL("http://127.0.0.1:8787");

  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (backendProcess) backendProcess.kill();
  if (process.platform !== "darwin") app.quit();
});

app.on("before-quit", () => {
  if (backendProcess) backendProcess.kill();
});
