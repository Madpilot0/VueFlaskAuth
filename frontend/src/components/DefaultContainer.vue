<template>
  <div class="app">
    <AppHeader fixed>
      <SidebarToggler class="d-md-down-none" display="lg"/>
      <b-navbar-nav class="ml-auto">
        <b-nav-item class="d-md-down-none">
          <i class="icon-bell"></i>
          <b-badge pill variant="danger">5</b-badge>
        </b-nav-item>
        <b-nav-item class="d-md-down-none">
          <i class="icon-list"></i>
        </b-nav-item>
        <b-nav-item class="d-md-down-none">
          <i class="icon-location-pin"></i>
        </b-nav-item>
        <b-nav-item class="d-md-down-none" @click='logout'>
          Logout
        </b-nav-item>
      </b-navbar-nav>
    </AppHeader>
    <div class="app-body">
      <AppSidebar fixed>
        <SidebarHeader/>
        <SidebarForm/>
        <center>
          <b-link class='userInfo text-secondary' href="#" @click="userModal=true">
            {{ firstlastname }} <br/>
            <img src='https://via.placeholder.com/100x100'><br/>
          </b-link>
        </center>
        <SidebarNav :navItems="nav"></SidebarNav>
      </AppSidebar>
      <main class="main">
        <Breadcrumb :list="list"/>
        <div class="container-fluid">
          <router-view></router-view>
        </div>
      </main>
    </div>
    <TheFooter>
      <div>
        <a href='https://example.org'>VueDash</a>
        <span class="ml-1">&copy; 2018 Sander Wegter</span>
      </div>
      <div class="ml-auto">
        <span class="mr-1">Powered By</span>
        <a href="https://sanderwegter.nl">The internet</a>
      </div>
    </TheFooter>
    <EditUser :userModal="userModal" @closed-modal='closedModal()'/>
  </div>
</template>

<script>
import nav from '@/_nav'
import store from '@/store'
import SidebarNav from '@/components/SidebarNav'
import EditUser from '@/components/Modals/EditUser'
import { Header as AppHeader, SidebarToggler, Sidebar as AppSidebar, SidebarFooter, SidebarForm, SidebarHeader, SidebarMinimizer, Aside as AppAside, AsideToggler, Footer as TheFooter, Breadcrumb } from '@coreui/vue'
export default {
  components: {
    AsideToggler,
    AppHeader,
    AppSidebar,
    AppAside,
    TheFooter,
    Breadcrumb,
    SidebarForm,
    SidebarFooter,
    SidebarToggler,
    SidebarHeader,
    SidebarNav,
    SidebarMinimizer,
    EditUser
  },
  data () {
    return {
      nav: nav.items,
      userModal: false
    }
  },
  methods: {
    logout: function () {
      this.$toast.success({
        title: 'Success',
        message: 'Logged out.'
      })
      store.dispatch('LOGOUT')
    },
    closedModal: function () {
      this.userModal = false
    }
  },
  computed: {
    name () {
      return this.$route.name
    },
    list () {
      return this.$route.matched.filter((route) => route.name || route.meta.label)
    },
    firstlastname () {
      return store.getters.firstlastname
    },
    group () {
      return store.getters.group
    },
    role () {
      return store.getters.role
    }
  }
}
</script>

<style scoped>
.userInfo > img {
  border-radius: 50%
}
.centerimg {
  margin-left:130px;
  width:50%;
}
</style>
