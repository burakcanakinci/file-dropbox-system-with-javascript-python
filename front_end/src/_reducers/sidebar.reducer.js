import React from "react";
import {sidebarConstants} from "../_constants/sidebar.constants";


let status = true;
const initialState = {status};

export function sidebarReducer(state = initialState, action) {
    switch (action.type) {
        case sidebarConstants.SIDEBAR_TOGGLE:
            return {
                status: action.payload,
            };
        default:
            return state
    }
}
