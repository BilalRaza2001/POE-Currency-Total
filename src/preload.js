// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { contextBridge, ipcRender} = require("electron")

contextBridge.exposeInMainWorld("api",{
    close: () => ipcRender.send("close-app")
})