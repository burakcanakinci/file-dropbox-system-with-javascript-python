import React from 'react'
import {
  CHeader,
  CToggler,
  CHeaderBrand,
  CHeaderNav,
  CHeaderNavItem,
  CHeaderNavLink,
  CSubheader,
  CBreadcrumbRouter,
  CLink,
    CImg
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import store from '../_helpers/store';
import {toggleSidebarAction} from '../_actions/index'
// routes config
import routes from '../routes'

import { 
  TheHeaderDropdown,
  TheHeaderDropdownMssg,
  TheHeaderDropdownNotif,
  TheHeaderDropdownTasks
}  from './index'
import TheHeaderStatus from "./TheHeaderStatus";
import {showSidebar} from "../_actions";

const TheHeader = () => {

  const toggleSidebar = () => {
    store.dispatch(toggleSidebarAction(!store.getState().sidebarReducer.status));
  };

  const toggleSidebarMobile = () => {
    store.dispatch(toggleSidebarAction(!store.getState().sidebarReducer.status));
  };

  return (
    <CHeader withSubheader>
      <CToggler
        inHeader
        className="ml-md-3 d-lg-none"
        onClick={toggleSidebarMobile}
      />
      <CToggler
        inHeader
        className="ml-3 d-md-down-none"
        onClick={toggleSidebar}
      />
      <CHeaderBrand className="mx-auto d-lg-none" to="/">
          {/*<CIcon name="logo" height="48" alt="Logo"/>*/}
          <CImg name="logo" height="48" alt="Logo"/>
      </CHeaderBrand>

      <CHeaderNav className="d-md-down-none mr-auto">
        <CHeaderNavItem className="px-3" >
          <CHeaderNavLink to="/dashboard">Dashboard</CHeaderNavLink>
        </CHeaderNavItem>
        {/*<CHeaderNavItem  className="px-3">*/}
        {/*  <CHeaderNavLink to="/users">Users</CHeaderNavLink>*/}
        {/*</CHeaderNavItem>*/}
        <CHeaderNavItem className="px-3">
          <CHeaderNavLink to="/admin">Admin</CHeaderNavLink>
        </CHeaderNavItem>
      </CHeaderNav>

      <CHeaderNav className="px-3">
        {/*<TheHeaderDropdownNotif/>*/}
        {/*<TheHeaderDropdownTasks/>*/}
        <TheHeaderStatus/>
        <TheHeaderDropdown/>
      </CHeaderNav>

      <CSubheader className="px-3 justify-content-between">
        <CBreadcrumbRouter 
          className="border-0 c-subheader-nav m-0 px-0 px-md-3" 
          routes={routes} 
        />
      </CSubheader>
    </CHeader>
  )
}

export default TheHeader
