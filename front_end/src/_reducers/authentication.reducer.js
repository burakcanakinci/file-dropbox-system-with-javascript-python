import { userConstants } from '../_constants/user.constants';

let user = '';
let token = '';
const initialState = {loggedIn: false, user, token};

export function authentication(state = initialState, action) {
    switch (action.type) {
        case userConstants.LOGIN_REQUEST:
            return {
                ...state,
                user: action.UID,
            };
        case userConstants.LOGIN_SUCCESS:
            return {
                ...state,
                loggedIn: true,
                user: action.UID,
                user_id: action.user_id,
                token: action.token
            };
        case userConstants.LOGIN_FAILURE:
            return {
                loggedIn: false,
            };
        case userConstants.REGISTER_REQUEST:
            return {
                ...state,
                user: action.UID,
            };
        case userConstants.LOGOUT:
            return {
                loggedIn: false,
                user: '',
                user_id: '',
                token: ''
            };
        default:
            return state
    }
}
