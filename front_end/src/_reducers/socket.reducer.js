import { socketConstants} from "../_constants/socket.constants";
import React from "react";


let status = 'disconnected';
let payload = 'Not Connected';
let fileUpload = false;
const initialState = {status, payload, fileUpload};

export function socketReducer(state = initialState, action) {
    switch (action.type) {
        case socketConstants.SOCKET_REQUEST:
            return {
                ...state,
                status: 'connecting',
                payload: action.payload,
            };
        case socketConstants.SOCKET_SUCCESS:
            return {
                ...state,
                status: 'connected',
                payload: 'Connected',
                host: action.payload,
            };
        case socketConstants.SOCKET_FAILURE:
            return {
                ...state,
                status: 'failed',
                payload: 'Failed',

            };
        case socketConstants.SOCKET_DISCONNECT:
            return {
                ...state,
                status: 'disconnected',
                payload: 'Disconnected',
                host: '',
            };
        case socketConstants.SOCKET_MESSAGE_STORE:
            return{
                ...state,
                event: action.event,
                payload: action.payload
            };
        case socketConstants.SOCKET_UPLOAD_SUCCESS:
            return{
                ...state,
                fileUpload: true,
            };
        default:
            return state
    }
}
