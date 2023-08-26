import React, {Component} from 'react'
import { Link, Redirect, withRouter } from 'react-router-dom'
import { connect } from 'react-redux';
import {callLogin, createSocket, Logout, setLogin, setLoginfail} from "../../../_actions";
import store from "../../../_helpers/store";
import jwt from 'jwt-decode';
// import history from "../../../_helpers/history"

import {
    CButton,
    CCard,
    CCardBody, CCardFooter,
    CCardGroup,
    CCol,
    CContainer,
    CForm,
    CInput,
    CInputGroup,
    CInputGroupPrepend,
    CInputGroupText,
    CRow
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {
      UID: 'hello',
    }

  }
  updateInputValue(evt){
    this.setState({ UID: evt.target.value });
  }
  handleClick(){
      store.dispatch(Logout())
      store.dispatch(callLogin(this.state.UID));
    fetch("http://" + process.env.REACT_APP_HOST_IP + process.env.REACT_APP_AUTHENTICATION_PORT + "/auth/login/" + this.state.UID, {
      method: "PUT",
      crossDomain: true,
      // credentials: 'include',
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
      body: JSON.stringify({
        UID: this.state.UID,
      })
    }).then((response) => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error("Login")
            }
        }
    ).then((response) => {
        // console.log(jwt(response['jwt'])['user_id']);
        store.dispatch(setLogin(this.state.UID, jwt(response['jwt'])['access_token'], jwt(response['jwt'])['user_id']));
        store.dispatch(createSocket())
    }).catch((error) => {
        store.dispatch(setLoginfail());
        console.log(error)
    })

        // .then((response) => console.log(jwt(response['jwt'])['access_token'])) // TODO: pass token
        .then(this.props.history.goBack())

  }
  render()
  {
    return (
        <div className="c-app c-default-layout flex-row align-items-center">
          <CContainer>
            <CRow className="justify-content-center">
              <CCol md="8">
                <CCardGroup>

                  <CCard className="p-4">
                    <CCardBody>
                      <CForm>
                        <h1>Login</h1>
                        <p className="text-muted">Sign In to your account</p>
                        <CInputGroup className="mb-3">
                          <CInputGroupPrepend>
                            <CInputGroupText>
                              <CIcon name="cil-user"/>
                            </CInputGroupText>
                          </CInputGroupPrepend>
                          <CInput value={this.state.UID} onChange={evt => this.updateInputValue(evt)} type="text"/>
                        </CInputGroup>
                        <CRow>
                          <CCol xs="6">
                            <Link to="/">
                              <CButton type="submit" onClick={() => this.handleClick()} color="primary" className="px-4">Login</CButton>
                            </Link>
                          </CCol>

                        </CRow>
                      </CForm>
                    </CCardBody>
                  </CCard>
                  <CCard className="text-white bg-primary py-5 d-md-down-none" style={{width: '44%'}}>
                    <CCardBody className="text-center">
                      <div>
                        <h2>Sign up</h2>
                        <Link to="/register">
                          <CButton color="primary" className="mt-3" active tabIndex={-1}>Register Now!</CButton>
                        </Link>
                      </div>
                    </CCardBody>
                  </CCard>
                </CCardGroup>
                  <CCardFooter className="p-4">
                      <Link to="/dashboard">
                          <CButton block color="secondary" >Back</CButton>
                      </Link>
                  </CCardFooter>
              </CCol>
            </CRow>
          </CContainer>
        </div>
    )
  }
}
connect()(Login);

export {Login}