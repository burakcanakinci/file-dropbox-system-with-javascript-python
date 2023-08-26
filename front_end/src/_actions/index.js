import {userConstants} from "../_constants/user.constants";
import {socketConstants} from "../_constants/socket.constants";
import {sidebarConstants} from "../_constants/sidebar.constants";

export const callLogin = (UID) => {
    return{
        type: userConstants.LOGIN_REQUEST,
        UID: UID,
    }
};
export const setLogin = (UID, token, user_id) => {
    return{
        type: userConstants.LOGIN_SUCCESS,
        UID: UID,
        user_id: user_id,
        token: token
    }
};
export const Logout = () => {
    return{
        type: userConstants.LOGOUT,
    }
};
export const callRegister = (UID) => {
    return{
        type: userConstants.REGISTER_REQUEST,
        UID: UID,
    }
};
export const setLoginfail = () => {
    return{
        type: userConstants.LOGIN_FAILURE,
        UID: '',
        token: ''
    }
};
export const createSocket = () => {
    return{
        type: socketConstants.SOCKET_REQUEST,
    }
};
export const successSocket = (host) => {
    return{
        type: socketConstants.SOCKET_SUCCESS,
        payload: host,
    }
};
export const failedSocket = () => {
    return{
        type: socketConstants.SOCKET_FAILURE,
    }
};
export const disconnectSocket = () => {
    return{
        type: socketConstants.SOCKET_DISCONNECT,
    }
};
export const sendSocketMessage = (ev, message) => {
    return{
        type: socketConstants.SEND_WEBSOCKET_MESSAGE,
        event: ev,
        payload: message,
    }
};
export const receiveSocketMessage = (ev, message) => {
    return{
        type: socketConstants.SOCKET_MESSAGE_RECEIVE,
        event: ev,
        payload: message,
    }
};
export const storeSocketMessage = (ev, message) => {
    return{
        type: socketConstants.SOCKET_MESSAGE_STORE,
        event: ev,
        payload: message,
    }
};
export const stopSocketMessage = (ev) => {
    return{
        type: socketConstants.SOCKET_MESSAGE_STOP,
        event: ev
    }
};
export const uploadSocketFile = (file) => {
    return{
        type: socketConstants.SOCKET_UPLOAD,
        file: file,
    }
};
export const successSocketFile = () => {
    return{
        type: socketConstants.SOCKET_UPLOAD_SUCCESS,
    }
};
export const toggleSidebarAction = (status) => {
    return{
        type: sidebarConstants.SIDEBAR_TOGGLE,
        payload: status,
    }
};