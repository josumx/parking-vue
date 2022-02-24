const SerialPort = require("serialport");


// list serial ports:
SerialPort.list().then(
    ports => ports.forEach(port => console.log(port.path)),
    err => console.log(err)
)