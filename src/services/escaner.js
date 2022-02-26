import { SerialPort } from "serialport";
const serialport = new SerialPort({
    path: "COM2",
    baudRate: 9600,
    autoOpen: false,
});


serialport.on("data", (data) => {
    console.log(data.toString("ascii").trim());
});

export default {
    connect() {
        serialport.open();
        console.log("Scanner connected");
    },
    printData(data) {
        console.log(data);
    }
}