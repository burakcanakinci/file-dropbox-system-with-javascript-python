import React, {Component} from 'react'

import {
    CCreateElement,
    CSidebar,
    CSidebarBrand,
    CSidebarNav,
    CSidebarNavDivider,
    CSidebarNavTitle,
    CSidebarMinimizer,
    CSidebarNavDropdown,
    CSidebarNavItem, CImg,
} from '@coreui/react'

import store from '../_helpers/store'

// sidebar nav config
import navigation from './_nav'

class TheSidebar extends Component {
    constructor(props){
        super(props);
        this._isMounted = false;
        this.state = {
          show: store.getState().sidebarReducer.status
        };
    }
    startSubscribe(){
        this.unsubscribe = store.subscribe(()=>{
            const show = store.getState().sidebarReducer.status;
            if (show !== this.state.show){
                this._isMounted && this.setState({show});
            }
        });
    }
    componentDidMount(){
        this._isMounted = true;
        this._isMounted && this.startSubscribe();

    } // TODO: Not remounting and subscribing on refresh...
    componentWillUnmount(){
        this.unsubscribe();
        this._isMounted = false;
    }

    render() {
        return (
            <CSidebar
                show={this.state.show}
            >
                <CSidebarBrand className="d-md-down-none" to="/">
                    <CImg name="logo" height={35} alt="Logo"/>
                    {/*<CImg name="logo" height={35} alt="Logo" src={logo}/>*/}
                </CSidebarBrand>
                <CSidebarNav>

                    <CCreateElement
                        items={navigation}
                        components={{
                            CSidebarNavDivider,
                            CSidebarNavDropdown,
                            CSidebarNavItem,
                            CSidebarNavTitle
                        }}
                    />
                </CSidebarNav>
                <CSidebarMinimizer className="c-d-md-down-none"/>
            </CSidebar>
        )
    }
}

export default React.memo(TheSidebar)
