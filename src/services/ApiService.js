import axios from "axios"
const apiClient = axios.create({
    baseURL: 'http://172.16.0.50:5000',
    timeout: 1000,
    withCredentials: false,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
    }

})
const apiServer = axios.create({
    baseURL: 'http://172.16.0.245',
    withCredentials: false,
    timeout: 1000,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
    }

})

export default {

    getSensors() {
        return apiClient.get('/').then(response => {
            return response;
        })
            .catch(error => {
                console.log("Error" + error);
                return false;
            })
    },
    open() {
        return apiClient.get('/open')
    },
    getBoleto() {
        return apiServer.get('/api/public/boletos');
    }
}