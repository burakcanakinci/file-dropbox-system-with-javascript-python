import React, {Component} from 'react'
import store from "../_helpers/store";

import {
    CButton,
    CCol,
    CRow
} from '@coreui/react'
import {createSocket, disconnectSocket} from "../_actions";

class TheHeaderStatus extends Component {
    constructor(props){
        super(props);
        this._isMounted = false;
        this.state = {
            status: store.getState().socketReducer.status };
        TheHeaderStatus.handleClickConnect = TheHeaderStatus.handleClickConnect.bind(this);
    }
    startSubscribe(){
        this.unsubscribe = store.subscribe(()=>{
            const status = store.getState().socketReducer.status;
            if (status !== this.state.status){
                this._isMounted && this.setState({status});
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


    static handleClickConnect(){
        if (store.getState().authentication.loggedIn){
            store.dispatch(createSocket())
        }
    }

    ButtonRender(props){
        if(props.status === 'connected'){
            return <CButton onClick={() => store.dispatch(disconnectSocket())} color="success" size="md" block>Connected</CButton>
        }
        if(props.status === 'connecting'){
            return <CButton color="warning" size="md" block>Connecting</CButton>
        }
        if(props.status === 'failed'){
            return <CButton onClick={() => TheHeaderStatus.handleClickConnect()} color="danger" size="md" block>Failed</CButton>
        }
        return <CButton onClick={() => TheHeaderStatus.handleClickConnect()} variant="outline" color="danger" size="md" block>Disconnected</CButton>


    }
    render () {
        return (
                <CRow className="align-items-center" style={{padding: "5px"}}>
                    {/*<CCol col="6" sm="4" md="2" xl className="mb-3 mb-xl-0">Connection: </CCol>*/}
                    <CCol>
                        {/*{(function (){*/}
                            {/*switch (socketStatus){*/}
                                {/*case 'connected':*/}
                                    {/*return <CButton color="success" size="md" block>Connected</CButton>;*/}
                                {/*case 'disconnected':*/}
                                    {/*return <CButton variant="outline" color="danger" size="md" block>Disconnected</CButton>;*/}
                                {/*default:*/}
                                    {/*return <div>Error</div>*/}
                            {/*} })()}*/}
                        <this.ButtonRender status={this.state.status}/>
                    </CCol>
                </CRow>
        )
    }
}


export default TheHeaderStatus
