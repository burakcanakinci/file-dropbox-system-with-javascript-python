import React, {Component} from 'react'
import {
  CBadge, CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CDataTable, CForm, CInput, CInputGroup,
  CRow
} from '@coreui/react'

import usersData from './users/UsersData'
import store from "../_helpers/store";
import {receiveSocketMessage, sendSocketMessage, stopSocketMessage, storeSocketMessage} from "../_actions";
import {Link} from "react-router-dom";

const getBadge = status => {
  switch (status) {
    case 'Active': return 'success'
    case 'Inactive': return 'secondary'
    case 'Pending': return 'warning'
    case 'Banned': return 'danger'
    default: return 'primary'
  }
}
const fields = ['clientName', 'clientId', 'filename', 'activity', 'created', 'file_metadata']

class History extends Component {
  constructor(props){
    super(props);
    this._isMounted = false;
    this.state = {
      event: "get-history",
      user_id: store.getState().authentication.user_id,
      payload: "",
      socketStatus: "On",
      data: [],
    };
    this.getHistory = this.getHistory.bind(this);
    this.downloadFile = this.downloadFile.bind(this);
    this.getHistory();
  }
  startSubscribe(ev){
    this.unsubscribe = store.subscribe(()=>{
      const payload = store.getState().socketReducer.payload;
      const event = store.getState().socketReducer.event;
      if (event === ev) {
        if (payload !== this.state.payload && (payload !== "" || payload !== undefined)) {
          if(event === this.state.event) {
            this._isMounted && this.setState({data: JSON.parse(JSON.stringify(payload))});
            // console.log(this.state.data);
          }
          if(event === 'download-file') {
            // this._isMounted && this.setState({data: JSON.parse(JSON.stringify(payload))});
            console.log(payload);
            var blob = new Blob([payload], { type: "text/npy" });
            var url = URL.createObjectURL(blob);
            // store.dispatch(stopSocketMessage("download-file"));

            window.open(url);
          }
        }
      }
    });
  }
  componentDidMount() {
    store.dispatch(storeSocketMessage("", ""));
    this._isMounted = true;
    this._isMounted && this.startSubscribe(this.state.event);
    this._isMounted && this.startSubscribe("download-file");
    // store.dispatch(receiveSocketMessage(this.state.event, {'user_id': this.state.user_id}));
    store.dispatch(sendSocketMessage(this.state.event, {'user_id': this.state.user_id}));

  }
  componentWillUnmount() {
    this.unsubscribe();
    store.dispatch(storeSocketMessage("", ""));
    this._isMounted = false;
    store.dispatch(stopSocketMessage(this.state.event));
  }
  getHistory(){
    store.dispatch(sendSocketMessage(this.state.event, {'user_id': this.state.user_id}));
  };
  updateInputValue(evt){
    this.setState({ user_id: evt.target.value });
  }
  downloadFile(file_id){

    store.dispatch(sendSocketMessage("download-file", {'file_id': file_id}));

  }

  render () {
    return(
    <>
      <CRow>
        <CCol>
          <h3>UserID:</h3>
        </CCol>
      </CRow>
      <CRow style={{padding: "5px"}}>
        <CCol>
          <CInput value={this.state.user_id} onChange={evt => this.updateInputValue(evt)} type="text"/>
        </CCol>
        <CCol>
          <CButton onClick={() => this.getHistory()} color="primary" className="px-4">Get history</CButton>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          <CCard>
            <CCardHeader>
              History
            </CCardHeader>
            <CCardBody>
              <CDataTable
                  items={this.state.data}
                  fields={fields}
                  hover
                  striped
                  bordered
                  size="sm"
                  itemsPerPage={15}
                  pagination
                  scopedSlots={{
                    'activity':
                        (item) => (
                            <td>
                              <CBadge color={getBadge(item.filename)} onClick={() => this.downloadFile(item.filename)}>
                                {"Download"}
                              </CBadge>
                            </td>
                        )
                  }}
              />
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>

    </>
    )
  }
}

export default History
