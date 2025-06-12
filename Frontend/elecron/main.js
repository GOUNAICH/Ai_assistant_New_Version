const { app, BrowserWindow, ipcMain, globalShortcut } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let mainWindow;
let pythonProcess;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 1320,
        height: 680,
        icon: path.join(__dirname, '../../Frontend/react/src/assets/Happy2.png'),
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            nodeIntegration: true,
            contextIsolation: true,
        },
    });

    // Remove the menu completely
    mainWindow.setMenuBarVisibility(false);

    // Register global shortcuts
    globalShortcut.register('F11', () => {
        if (mainWindow) {
            mainWindow.setFullScreen(!mainWindow.isFullScreen());
        }
    });

    globalShortcut.register('F12', () => {
        if (mainWindow) {
            mainWindow.webContents.toggleDevTools();
        }
    });

    globalShortcut.register('Ctrl+R', () => {
        if (mainWindow) {
            mainWindow.webContents.reload();
        }
    });

    globalShortcut.register('Ctrl+Shift+R', () => {
        if (mainWindow) {
            mainWindow.webContents.reloadIgnoringCache();
        }
    });

    mainWindow.loadURL("http://localhost:5173");

    // Start Python process with 'electron' argument
    pythonProcess = spawn("python", ["../../Backend/main.py", "electron"], {
        stdio: ["pipe", "pipe", "pipe"]
    });

    // Set up IPC communication
    ipcMain.on('electron-ready', () => {
        pythonProcess.stdin.write('window_ready\n');
    });

    pythonProcess.stdout.on("data", (data) => {
        const response = data.toString().trim();
        console.log(` ${response}`);
        if (mainWindow) {
            mainWindow.webContents.send("python-response", response);
        }
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Python error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        console.log(`Python process exited with code ${code}`);
    });

    mainWindow.on("closed", () => {
        if (pythonProcess) {
            pythonProcess.kill();
        }
        mainWindow = null;
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});

// Clean up global shortcuts when app is quitting
app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});