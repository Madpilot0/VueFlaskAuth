<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <b-row class="justify-content-center">
        <b-col md="8">
          <b-card-group>
            <b-card no-body class="p-4">
              <b-card-body>
                <b-form>
                  <h1>Login</h1>
                  <p class="text-muted">Sign in to your account</p>
                  <b-input-group class="mb-3">
                    <b-input-group-prepend><b-input-group-text><i class="icon-user"></i></b-input-group-text></b-input-group-prepend>
                    <b-form-input v-focus type="text" class="form-control" v-model='username' placeholder="Username" @keyup.enter.native='login'/>
                  </b-input-group>
                  <b-input-group class="mb-4">
                    <b-input-group-prepend><b-input-group-text><i class="icon-lock"></i></b-input-group-text></b-input-group-prepend>
                    <b-form-input type="password" class="form-control" v-model='password' placeholder="Password" @keyup.enter.native='login'/>
                  </b-input-group>
                  <b-form-group label-for="stayauth">
                      <b-form-checkbox id="stayauth" v-model='stayin'>Stay logged in</b-form-checkbox>
                  </b-form-group>
                  <b-row>
                    <b-col cols="6">
                      <b-button variant="primary" class="px-4" @click='login'>Login</b-button>
                    </b-col>
                    <b-col cols="6" class="text-right">
                      <b-button variant="link" class="px-0" disabled>Forgot Password?</b-button>
                    </b-col>
                  </b-row>
                </b-form>
              </b-card-body>
            </b-card>
            <b-card no-body class="text-white bg-primary py-5 d-md-down-none" style="width:44%">
              <b-card-body class="text-center">
                <div>
                  <img src="https://via.placeholder.com/300x60?text=Logo+here"/>
                </div>
                <p>
                  Intro text here
                </p>
              </b-card-body>
            </b-card>
          </b-card-group>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import store from '@/store'
export default {
  data () {
    return {
      username: '',
      password: '',
      stayin: false
    }
  },
  methods: {
    login: function () {
      store.dispatch('LOGIN', {username: this.username, password: this.password, stayin: this.stayin})
    }
  }
}
</script>
