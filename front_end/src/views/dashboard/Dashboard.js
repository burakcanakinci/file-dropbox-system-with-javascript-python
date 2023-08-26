import React, {Component, lazy, useState} from 'react';
import store from '../../_helpers/store'
import {
    CButton,
    CCard,
    CCardBody,
    CCardFooter,
    CCardHeader,
    CCol,
    CRow,
    CForm,
    CFormGroup,
    CLabel,
    CInput,
    CFormText,
    CSelect,
    CInputFile,
    CToast,
    CToastHeader,
    CToastBody,
    CToaster,
    CModalHeader, CModalTitle, CModalBody, CModalFooter, CModal

} from '@coreui/react';
import CIcon from '@coreui/icons-react'
import {
    sendSocketMessage,
    receiveSocketMessage,
    uploadSocketFile,
    stopSocketMessage,
    storeSocketMessage
} from "../../_actions";



class Dashboard extends Component {
    constructor(props){
        super(props);
        this._isMounted = false;
        this.state = {
            modal: store.getState().socketReducer.fileUpload,
            payload: store.getState().socketReducer.payload,
            socketStatus: "On",
            file: '',
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        // this.getHistory = this.getHistory.bind(this);
        // this.getHistory();
    }
    uploadListen(){
        store.dispatch(receiveSocketMessage("complete-upload"));
        this.unsubscribeFile = store.subscribe(()=>{
            const fileUpload = store.getState().socketReducer.fileUpload;
            if (fileUpload !== this.state.fileUpload){
                this._isMounted && this.setState({fileUpload});
            }
        });
    };
    startSubscribe(){
        this.unsubscribe = store.subscribe(()=>{
            const payload = store.getState().socketReducer.payload;
            if (payload !== this.state.payload){
                this._isMounted && this.setState({payload});
            }
        });
    }

    componentDidMount(){
        store.dispatch(storeSocketMessage(""));
        this._isMounted = true;
        this._isMounted && this.startSubscribe();
        this._isMounted && this.uploadListen();


    } // TODO: Not remounting and subscribing on refresh...
    componentWillUnmount(){
        this.unsubscribe();
        this.unsubscribeFile();
        store.dispatch(storeSocketMessage(""));
        this._isMounted = false;
    }
    handleListen = () => {
        // store.dispatch(receiveSocketMessage("test", {'data':'none'}));
        store.dispatch(stopSocketMessage("admin"));
        store.dispatch(receiveSocketMessage("admin", {'data':'none'}));

    };
    handleEmit=()=>{
        if(this.state.socketStatus==="On"){
            store.dispatch(sendSocketMessage("message", {'data':'Stop Sending', 'status':'Off'}));
            this.setState({'socketStatus':"Off"})
        }
        else{
            store.dispatch(sendSocketMessage("message", {'data':'Start Sending', 'status':'On'}));
            this.setState({'socketStatus':"On"})
        }
        console.log("Emit Clicked")
    };

    handleSubmit(e){
        // TODO: add multli file support:
        // https://github.com/miguelgrinberg/socketio-examples/blob/master/uploads/static/uploads/main.js

        // console.log(this.state.file['0']);
        if(this.state.file['0'] !== undefined) {
            store.dispatch(uploadSocketFile(this.state.file['0']));
        }
        // store.dispatch(sendSocketMessage("upload", {'data': this.state.file}));
    }

    render () {


        const user = store.getState().authentication.user;
        return (

            <>
                {/*<React.Fragment>*/}
                {/*    <CCol xs="12" sm="6" style={{padding: "5px"}}>*/}
                {/*    <CRow className="align-items-center" style={{padding: "5px"}}>*/}
                {/*        /!*<CCol col="6" sm="4" md="2" xl className="mb-3 mb-xl-0">Connection: </CCol>*!/*/}
                {/*        <CCol>*/}
                {/*            <h1>Socket Testing: {this.state.payload}</h1>*/}
                {/*        </CCol>*/}
                {/*    </CRow>*/}
                {/*    <CRow>*/}
                {/*        <CCol>*/}
                {/*        /!*<div onClick={this.handleEmit}> Start/Stop</div>*!/*/}
                {/*        <CButton onClick={this.handleListen} color="info" size="md" block>Listen</CButton>*/}
                {/*        </CCol>*/}
                {/*        /!*<div onClick={this.handleListen}> Listen</div>*!/*/}
                {/*    </CRow>*/}
                {/*    </CCol>*/}
                {/*    <CCol xs="12" sm="6">*/}
                {/*    </CCol>*/}

                {/*</React.Fragment>*/}
                {this.state.fileUpload
                ?<CToaster
                        position={'top-right'}
                        key={'toaster' + 1}
                    >
                        {
                            <CToast
                                key={'toast' + 1}
                                show={true}
                                autohide={true && 3000}
                                fade={true}
                            >
                                <CToastHeader closeButton={this.state.modal}>
                                    File Upload
                                </CToastHeader>
                                <CToastBody>
                                    {`File Uploaded successfully`}
                                </CToastBody>
                            </CToast>
                        }
                    </CToaster>
                :<div></div>}


                <CCard>
                    <CCardBody>
                        <CRow>
                            <CCol xs="12">
                                <CCard>
                                    <CCardHeader>
                                        Upload File(s)
                                        <small> Elements</small>
                                    </CCardHeader>
                                    <CCardBody>
                                        <CForm action="" method="post" encType="multipart/form-data"
                                               className="form-horizontal">
                                            <CFormGroup row>
                                                <CCol md="3">
                                                    <CLabel>Username</CLabel>
                                                </CCol>
                                                <CCol xs="12" md="9">
                                                    <p className="form-control-static">{ user
                                                        ? user
                                                        : 'Username'}</p>
                                                </CCol>
                                            </CFormGroup>
                                            <CFormGroup row>
                                                <CCol md="3">
                                                    <CLabel htmlFor="text-input">Text Input</CLabel>
                                                </CCol>
                                                <CCol xs="12" md="9">
                                                    <CInput id="text-input" name="text-input" placeholder="Text"/>
                                                    <CFormText>This is a help text</CFormText>
                                                </CCol>
                                            </CFormGroup>
                                            {/*<CFormGroup row>*/}
                                                {/*<CCol md="3">*/}
                                                    {/*<CLabel htmlFor="date-input">Date Input</CLabel>*/}
                                                {/*</CCol>*/}
                                                {/*<CCol xs="12" md="9">*/}
                                                    {/*<CInput type="date" id="date-input" name="date-input"*/}
                                                            {/*placeholder="date"/>*/}
                                                {/*</CCol>*/}
                                            {/*</CFormGroup>*/}
                                            <CFormGroup row>
                                                <CCol md="3">
                                                    <CLabel htmlFor="select">Select</CLabel>
                                                </CCol>
                                                <CCol xs="12" md="9">
                                                    <CSelect custom name="select" id="select">
                                                        <option value="0">Please select</option>
                                                        <option value="1">Option #1</option>
                                                        <option value="2">Option #2</option>
                                                        <option value="3">Option #3</option>
                                                    </CSelect>
                                                </CCol>
                                            </CFormGroup>
                                            {/*<CFormGroup row>*/}
                                                {/*<CCol md="3">*/}
                                                    {/*<CLabel>Multiple File input</CLabel>*/}
                                                {/*</CCol>*/}
                                                {/*<CCol xs="12" md="9">*/}
                                                    {/*<CInputFile*/}
                                                        {/*id="file-multiple-input"*/}
                                                        {/*name="file-multiple-input"*/}
                                                        {/*multiple*/}
                                                        {/*custom*/}
                                                    {/*/>*/}
                                                    {/*<CLabel htmlFor="file-multiple-input" variant="custom-file">*/}
                                                        {/*Choose Files...*/}
                                                    {/*</CLabel>*/}
                                                {/*</CCol>*/}
                                            {/*</CFormGroup>*/}
                                            <CFormGroup row>
                                                <CLabel col md={3}>Custom file input</CLabel>
                                                <CCol xs="12" md="9">
                                                    {/*<CInputFile value={this.state.file} onChange={evt => this.setState({file: evt.target.value})} type="file" custom id="custom-file-input"/>*/}
                                                    {/*<CLabel htmlFor="custom-file-input" variant="custom-file">*/}
                                                        {/*{this.state.file*/}
                                                            {/*? this.state.file*/}
                                                            {/*: 'Choose file...'*/}
                                                        {/*}*/}
                                                    {/*</CLabel>*/}
                                                    <input type="file" onChange={(e) => this.setState(this.state.file = e.target.files)} />
                                                </CCol>
                                            </CFormGroup>

                                        </CForm>
                                    </CCardBody>
                                    <CCardFooter>
                                        {user
                                            ?
                                            <div>
                                                <CButton type="submit" onClick={() => this.handleSubmit()} size="sm" color="primary"><CIcon
                                                name="cil-scrubber"/> Submit</CButton>
                                                <CButton type="reset" size="sm" color="danger"><CIcon
                                                name="cil-ban"/> Reset</CButton>
                                            </div>
                                            :
                                            <div>
                                                <CButton type="submit" size="sm" color="primary" disabled><CIcon
                                                    name="cil-scrubber"/> Submit</CButton>
                                                < CButton type="reset" size="sm" color="danger" disabled><CIcon
                                                name="cil-ban"/> Reset</CButton>
                                            </div>
                                        }
                                    </CCardFooter>
                                </CCard>

                            </CCol>
                        </CRow>
                    </CCardBody>
                </CCard>



            </>
        )
    }
}

export default Dashboard
