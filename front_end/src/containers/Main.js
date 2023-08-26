import React, { Component } from 'react'
import {
  TheContent,
  TheSidebar,
  TheFooter,
  TheHeader
} from './index'
import connect from "react-redux/lib/connect/connect";

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    componentDidMount() {
        // const { cookies } = this.props;
        // cookies.set('token','123456789', { path: '/' , SameSite: 'None', Secure: true}); // TODO: Place this in a better place
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
)(Main);
export default Main
