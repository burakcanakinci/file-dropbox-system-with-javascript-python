import io from 'socket.io-client';
import store from '../_helpers/store'
import {storeSocketMessage, successSocket, failedSocket, successSocketFile} from "../_actions";

// Example conf. You can move this to your config file.
// const host = 'http://54.154.129.30:5000/';
const host = ("http://" + process.env.REACT_APP_HOST_IP + process.env.REACT_APP_SOCKET_PORT + "/");
const chunk_size = 64 * 1024;

export default class socketAPI {
    socket;



    connect() {

        let reattempts = 2;

        this.socket = io.connect(host, {
            secure: true,
            query: {access_token: store.getState().authentication.token, user_id: store.getState().authentication.user_id},
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax : 5000,
            reconnectionAttempts: reattempts

        });
        this.socket.on('connect_error', function() {
            reattempts = reattempts - 1;
            if (reattempts === 0){
                store.dispatch(failedSocket());
            }
        });
    }

    connected() {
        return new Promise((resolve, reject) => {
            if (!this.socket) return reject('No socket connection.');

            this.socket.on('alive', (response) => {if(response['alive']) {store.dispatch(successSocket(host))}});

            return this.socket.emit("alive", {
                user_id: store.getState().authentication.user_id
            }, response => {
                return resolve();
            });

        }).catch(e =>{
            console.log(e)
        });
    }

    disconnect() {
        return new Promise((resolve, reject) => {
            if (!this.socket) return reject('No socket connection.');

            this.socket.disconnect(() => {
                this.socket = null;
                resolve();
            });
        }).catch(e =>{
            console.log(e)
        });
    }

    send(event, data) {
        return new Promise((resolve, reject) => {
            if (!this.socket) return reject('No socket connection.');

            return this.socket.emit(event, data,{
                extraHeaders: {
                    Authorization: "Bearer " + store.getState().authentication.token
                }
            }, response => {
                this.socket.on(event, response => store.dispatch(storeSocketMessage(event, response['data'])));
                // console.log(store.getState().socketReducer.payload);

                return resolve();
            });
        }).catch(e =>{
            console.log(e)
        });
    }

    on(event, fun) {
        // No promise is needed here, but we're expecting one in the middleware.
        return new Promise((resolve, reject) => {
            if (!this.socket) return reject('No socket connection.');

            this.socket.on(event, (response) =>{
                store.dispatch(storeSocketMessage(event, response['data']))});
                // console.log(response['data'])});
            return resolve();
        }).catch(e =>{
            console.log(e)
        });
    }

    off(event) {
        // No promise is needed here, but we're expecting one in the middleware.
        return new Promise((resolve, reject) => {
            if (!this.socket) return reject('No socket connection.');

            this.socket.off(event);
            // console.log(response['data'])});
            return resolve();
        }).catch(e =>{
            console.log(e)
        });
    }

    onReadSuccess(file_id, file, offset, length, data) {
        this.socket.emit('write-chunk', file_id, offset, data, function(offset, ack) {
            if (!ack)
                this.onReadError(file_id, file, offset, 0, 'Transfer aborted by server')
        }.bind(this, offset));
        let end_offset = offset + length;
        if (end_offset < file.size)
            this.readFileChunk(file_id, file, end_offset, chunk_size,
                this.onReadSuccess.bind(this),
                this.onReadError.bind(this));
        else {
            this.done = true;
        }
        if (this.done) {
            this.socket.on('complete-upload', response => {
                if (response['data'] === true){
                    store.dispatch(successSocketFile());
                }
            });
            this.socket.emit('complete-upload', file_id, store.getState().authentication.user, store.getState().authentication.user_id, response => {
            });
        }
    }

    onReadError(file_id, file, offset, length, error) {
        console.log('Upload error for ' + file.name + ' | ' + file_id + ': ' + error);
        this.done = true;
    }

    readFileChunk(file_id, file, offset) {

        let success = this.onReadSuccess.bind(this);
        let error = this.onReadError.bind(this);

        let end_offset = offset + chunk_size;
        if (end_offset > file.size)
            end_offset = file.size;
        var r = new FileReader();
        r.onload = function (file, offset, chunk_size, e) {
            if (e.target.error != null)
                error(file_id, file, offset, chunk_size, e.target.error);
            else
                success(file_id, file, offset, chunk_size, e.target.result);
        }.bind(r, file, offset, chunk_size);
        r.readAsArrayBuffer(file.slice(offset, end_offset));
    }
    fileUpload(file, offset){
        return new Promise((resolve, reject) => {
            if (!this.socket) return reject('No socket connection.');
            this.done = false;

            this.socket.on('start-transfer', response => {
                let file_id = response['id'];
                this.readFileChunk(file_id, file, offset)
                this.socket.off('start-transfer');
            });
            this.socket.emit('start-transfer', file.name, file.size);

        }).catch(e =>{
            console.log(e)
        });
    }

}