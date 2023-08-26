import React, {Component} from 'react'
import { Link, withRouter } from 'react-router-dom'

import {
    CButton,
    CCard,
    CCardBody,
    CCardFooter,
    CCol,
    CContainer,
    CForm,
    CInput,
    CInputGroup,
    CInputGroupPrepend,
    CInputGroupText,
    CRow, CSelect
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

import store from "../../../_helpers/store";
import {callRegister, disconnectSocket, Logout} from "../../../_actions";
import connect from "react-redux/es/connect/connect";

class Register extends Component {
    constructor(props) {
        super(props);
        this.state = {
            UID: 'username',
            role: 'admin',
            redirect : false
        };

        this.handleSubmit = this.handleSubmit.bind(this);

    }
    updateInputValue(evt){
        this.setState({ UID: evt.target.value });
    }

    handleSubmit(event){
        store.dispatch(disconnectSocket())
        store.dispatch(Logout())
        // store.dispatch(callRegister(this.state.UID));
        fetch("http://" + process.env.REACT_APP_HOST_IP + process.env.REACT_APP_AUTHENTICATION_PORT + "/auth/signup", {
            method: "POST",
            crossDomain: true,
            // credentials: 'include',
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify({
                name: this.state.UID,
                role: this.state.role,
            })
        }).then(this.props.history.goBack());

        // .then((response) => console.log(jwt(response['jwt'])['access_token'])) // TODO: pass token

    }

  render() {
      return (
          <div className="c-app c-default-layout flex-row align-items-center">
              <CContainer>
                  <CRow className="justify-content-center">
                      <CCol md="9" lg="7" xl="6">
                          <CCard className="mx-4">
                              <CCardBody className="p-4">
                                  <CForm onSubmit={this.handleSubmit}>
                                      <h1>Register</h1>
                                      <p className="text-muted">Create your account</p>
                                      <CInputGroup className="mb-3">
                                          <CInputGroupPrepend>
                                              <CInputGroupText>
                                                  <CIcon name="cil-user"/>
                                              </CInputGroupText>
                                          </CInputGroupPrepend>
                                          <CInput value={this.state.UID} onChange={evt => this.updateInputValue(evt)} type="text"/>
                                      </CInputGroup>
                                      <CInputGroup className="mb-3">
                                          <CInputGroupPrepend>
                                              <CInputGroupText>@</CInputGroupText>
                                          </CInputGroupPrepend>
                                          <CSelect value={this.state.role} onChange={evt => this.setState({role: evt.target.value})}>
                                              <option value="admin">admin</option>
                                              <option value="developer">developer</option>
                                              <option value="user">user</option>
                                          </CSelect>
                                      </CInputGroup>
                                      {/*<CInputGroup className="mb-3">*/}
                                          {/*<CInputGroupPrepend>*/}
                                              {/*<CInputGroupText>*/}
                                                  {/*<CIcon name="cil-lock-locked"/>*/}
                                              {/*</CInputGroupText>*/}
                                          {/*</CInputGroupPrepend>*/}
                                          {/*<CInput type="password" placeholder="Password" autoComplete="new-password"/>*/}
                                      {/*</CInputGroup>*/}
                                      {/*<CInputGroup className="mb-4">*/}
                                          {/*<CInputGroupPrepend>*/}
                                              {/*<CInputGroupText>*/}
                                                  {/*<CIcon name="cil-lock-locked"/>*/}
                                              {/*</CInputGroupText>*/}
                                          {/*</CInputGroupPrepend>*/}
                                          {/*<CInput type="password" placeholder="Repeat password"*/}
                                                  {/*autoComplete="new-password"/>*/}
                                      {/*</CInputGroup>*/}
                                      <CButton type="submit" color="success" block>Create Account</CButton>
                                  </CForm>
                              </CCardBody>
                              <CCardFooter className="p-4">
                                  <Link to="/dashboard">
                                      <CButton block color="secondary">Back</CButton>
                                  </Link>
                              </CCardFooter>
                          </CCard>
                      </CCol>
                  </CRow>
              </CContainer>
          </div>
      )
  }
}
connect()(Register);
Register = withRouter(Register);
export {Register};
