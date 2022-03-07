import { SerialPort } from "serialport";
const serialport = new SerialPort({
    path: "COM2",
    baudRate: 9600,
    autoOpen: false,
});


// serialport.on("data", (data) => {
//     console.log(data.toString("ascii").trim());
// });

export default {
    init() {
        serialport.open();
        return serialport;
    },

}