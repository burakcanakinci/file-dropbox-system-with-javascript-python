    export default [
    {
    _tag: 'CSidebarNavItem',
    name: 'Dashboard',
    to: '/dashboard',
    icon: 'cil-speedometer',
    },
    {
    _tag: 'CSidebarNavTitle',
    _children: ['Uploads']
    },
    {
    _tag: 'CSidebarNavItem',
    name: 'Active',
    to: '/active',
    icon: 'cil-drop',
    },
    {
    _tag: 'CSidebarNavItem',
    name: 'History',
    to: '/history',
    icon: 'cil-pencil',
    },
    {
        _tag: 'CSidebarNavDivider'
    },
    {
        _tag: 'CSidebarNavTitle',
        _children: ['User'],
    },
    {
        _tag: 'CSidebarNavItem',
        name: 'Login',
        to: '/login',
        icon: 'cil-pencil',

    },
    {
        _tag: 'CSidebarNavItem',
        name: 'Register',
        to: '/register',
        icon: 'cil-pencil',

    },
    {
    _tag: 'CSidebarNavDivider'
    },
    // {
    // _tag: 'CSidebarNavTitle',
    // _children: ['Extras'],
    // },
    // {
    // _tag: 'CSidebarNavDropdown',
    // name: 'Pages',
    // route: '/pages',
    // icon: 'cil-star',
    // _children: [
    //   {
    //     _tag: 'CSidebarNavItem',
    //     name: 'Login',
    //     to: '/login',
    //   },
    //   {
    //     _tag: 'CSidebarNavItem',
    //     name: 'Register',
    //     to: '/register',
    //   },
    //   {
    //     _tag: 'CSidebarNavItem',
    //     name: 'Error 404',
    //     to: '/404',
    //       addLinkClass: 'c-disabled',
    //       'disabled': true
    //   },
    //   {
    //     _tag: 'CSidebarNavItem',
    //     name: 'Error 500',
    //     to: '/500',
    //       addLinkClass: 'c-disabled',
    //       'disabled': true
    //   },
    // ],
    // },

    ]

