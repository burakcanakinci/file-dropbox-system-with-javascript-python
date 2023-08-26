import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';
import allReducers from '../_reducers';
import { composeWithDevTools } from 'redux-devtools-extension';
import socketMiddleware from "../_middleware/socketMiddleware";
import SocketClient from "./SocketClient"

const socket = new SocketClient();

const store = createStore(allReducers,
    composeWithDevTools(
        applyMiddleware(
        thunkMiddleware, socketMiddleware(socket)),
    ));
export default store