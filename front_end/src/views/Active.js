import React, {Component} from 'react'
import {
  CBadge,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CDataTable,
  CRow
} from '@coreui/react'

import usersData from './users/UsersData'
import store from "../_helpers/store";
import {receiveSocketMessage, sendSocketMessage, stopSocketMessage, storeSocketMessage} from "../_actions";

const getBadge = status => {
  switch (status) {
    case 'Active': return 'success'
    case 'Inactive': return 'secondary'
    case 'Pending': return 'warning'
    case 'Banned': return 'danger'
    default: return 'primary'
  }
}
const fields = ['name','registered', 'role', 'status']
const fields1 = ["user_name", 'user_id', 'id','file_name', 'status', "event_timestamp"]


class Active extends Component {
    constructor(props){
        super(props);
        this._isMounted = false;
        this.state = {
            event: "admin",
            payload: "",
            socketStatus: "On",
            data: [
                // {id: 0, name: 'John POE', registered: '2018/01/01', role: 'Guest', status: 'Pending'},
                // {id: 1, name: 'Samppa Nori', registered: '2018/01/01', role: 'Member', status: 'Active'},
                // {id: 42, name: 'Ford Prefect', registered: '2001/05/25', role: 'Alien', status: 'Don\'t panic!'}
            ],
        };
    }
    startSubscribe(){
        this.unsubscribe = store.subscribe(()=>{
            const payload = store.getState().socketReducer.payload;
            const event = store.getState().socketReducer.event;
            if (event === this.state.event) {
                if (payload !== this.state.payload && (payload !== "" || payload !== undefined)) {
                    // console.log(JSON.parse(JSON.stringify(payload)));
                    this._isMounted && this.setState({data: [JSON.parse(JSON.stringify(payload))].concat(this.state.data)});
                }
            }
        });
    }
    componentDidMount() {
        store.dispatch(storeSocketMessage("",""));
        this._isMounted = true;
        this._isMounted && this.startSubscribe();
        store.dispatch(receiveSocketMessage(this.state.event, {'user_id': store.getState().authentication.user_id}));
    }
    componentWillUnmount() {
        this.unsubscribe();
        store.dispatch(storeSocketMessage("",""));
        this._isMounted = false;
        store.dispatch(stopSocketMessage(this.state.event));
    }

    render() {
        return (
            <>
                <CRow>
                    <CCol>
                        <CCard>
                            <CCardHeader>
                                Active Uploads
                            </CCardHeader>
                            <CCardBody>
                                <CDataTable
                                    items={this.state.data}
                                    fields={fields1}
                                    hover
                                    striped
                                    bordered
                                    size="sm"
                                    itemsPerPage={10}
                                    pagination
                                    scopedSlots = {{
                                        'status':
                                            (item)=>(
                                                <td>
                                                    <CBadge color={getBadge(item.status)}>
                                                        {item.status}
                                                    </CBadge>
                                                </td>
                                            )
                                    }}
                                />
                            </CCardBody>
                        </CCard>
                    </CCol>
                </CRow>
                {/*<CRow>*/}
                {/*    <CCol xs="12" lg="6">*/}
                {/*        <CCard>*/}
                {/*            <CCardHeader>*/}
                {/*                Node 1*/}
                {/*            </CCardHeader>*/}
                {/*            <CCardBody>*/}
                {/*                <CDataTable*/}
                {/*                    items={this.state.data}*/}
                {/*                    fields={fields1}*/}
                {/*                    itemsPerPage={5}*/}
                {/*                    pagination*/}
                {/*                    scopedSlots={{*/}
                {/*                        'status':*/}
                {/*                            (item) => (*/}
                {/*                                <td>*/}
                {/*                                    <CBadge color={getBadge(item.status)}>*/}
                {/*                                        {item.status}*/}
                {/*                                    </CBadge>*/}
                {/*                                </td>*/}
                {/*                            )*/}

                {/*                    }}*/}
                {/*                />*/}
                {/*            </CCardBody>*/}
                {/*        </CCard>*/}
                {/*    </CCol>*/}

                {/*    <CCol xs="12" lg="6">*/}
                {/*        <CCard>*/}
                {/*            <CCardHeader>*/}
                {/*                Node 2*/}
                {/*            </CCardHeader>*/}
                {/*            <CCardBody>*/}
                {/*                <CDataTable*/}
                {/*                    items={usersData}*/}
                {/*                    fields={fields}*/}
                {/*                    itemsPerPage={5}*/}
                {/*                    pagination*/}
                {/*                    scopedSlots={{*/}
                {/*                        'status':*/}
                {/*                            (item) => (*/}
                {/*                                <td>*/}
                {/*                                    <CBadge color={getBadge(item.status)}>*/}
                {/*                                        {item.status}*/}
                {/*                                    </CBadge>*/}
                {/*                                </td>*/}
                {/*                            )*/}

                {/*                    }}*/}
                {/*                />*/}
                {/*            </CCardBody>*/}
                {/*        </CCard>*/}
                {/*    </CCol>*/}
                {/*</CRow>*/}

                {/*<CRow>*/}

                {/*    <CCol xs="12" lg="6">*/}
                {/*        <CCard>*/}
                {/*            <CCardHeader>*/}
                {/*                Node 3*/}
                {/*            </CCardHeader>*/}
                {/*            <CCardBody>*/}
                {/*                <CDataTable*/}
                {/*                    items={usersData}*/}
                {/*                    fields={fields}*/}
                {/*                    itemsPerPage={5}*/}
                {/*                    pagination*/}
                {/*                    scopedSlots={{*/}
                {/*                        'status':*/}
                {/*                            (item) => (*/}
                {/*                                <td>*/}
                {/*                                    <CBadge color={getBadge(item.status)}>*/}
                {/*                                        {item.status}*/}
                {/*                                    </CBadge>*/}
                {/*                                </td>*/}
                {/*                            )*/}

                {/*                    }}*/}
                {/*                />*/}
                {/*            </CCardBody>*/}
                {/*        </CCard>*/}
                {/*    </CCol>*/}

                {/*    <CCol xs="12" lg="6">*/}
                {/*        <CCard>*/}
                {/*            <CCardHeader>*/}
                {/*                Node 4*/}
                {/*            </CCardHeader>*/}
                {/*            <CCardBody>*/}
                {/*                <CDataTable*/}
                {/*                    items={usersData}*/}
                {/*                    fields={fields}*/}
                {/*                    itemsPerPage={5}*/}
                {/*                    pagination*/}
                {/*                    scopedSlots={{*/}
                {/*                        'status':*/}
                {/*                            (item) => (*/}
                {/*                                <td>*/}
                {/*                                    <CBadge color={getBadge(item.status)}>*/}
                {/*                                        {item.status}*/}
                {/*                                    </CBadge>*/}
                {/*                                </td>*/}
                {/*                            )*/}

                {/*                    }}*/}
                {/*                />*/}
                {/*            </CCardBody>*/}
                {/*        </CCard>*/}
                {/*    </CCol>*/}

                {/*</CRow>*/}

            </>
        )
    }
}

export default Active
