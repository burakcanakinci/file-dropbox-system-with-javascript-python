import React, { Component } from 'react'
import {
  TheContent,
  TheSidebar,
  TheFooter,
  TheHeader
} from './index'
import connect from "react-redux/lib/connect/connect";

class TheLayout extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render()
    {
        return (
            <div className="c-app c-default-layout">
                <TheSidebar/>
                <div className="c-wrapper">
                    <TheHeader/>
                    <div className="c-body">
                        <TheContent/>
                    </div>
                    <TheFooter/>
                </div>
            </div>
        )
    }
}
const mapStateToProps = (state, ownProps) => {
    return({
        state: state,
        cookies: ownProps.cookies,
    });
};
export const Layout = connect(
    mapStateToProps,
    null
)(TheLayout);
export default TheLayout
