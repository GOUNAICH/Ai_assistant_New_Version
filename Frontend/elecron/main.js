const { app, BrowserWindow, ipcMain, Menu } = require("electron");
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

    // Create a minimal menu with just the shortcuts you need
    const template = [
        {
            label: 'View',
            submenu: [
                {
                    label: 'Toggle Fullscreen',
                    accelerator: 'F11',
                    click: () => {
                        mainWindow.setFullScreen(!mainWindow.isFullScreen());
                    }
                },
                {
                    label: 'Toggle Developer Tools',
                    accelerator: 'F12',
                    click: () => {
                        mainWindow.webContents.toggleDevTools();
                    }
                },
                {
                    label: 'Reload',
                    accelerator: 'CmdOrCtrl+R',
                    click: () => {
                        mainWindow.webContents.reload();
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);

    mainWindow.loadURL("http://localhost:5173");

    // Start Python process with 'electron' argument
    pythonProcess = spawn("python", ["C:\\Users\\Morus\\Desktop\\Ai_assistant_New_Version\\Backend\\main.py", "electron"], {
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