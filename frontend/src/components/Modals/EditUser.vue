<template>
  <b-modal title="Edit user" class="modal-info" v-model="modal" @hide="closedModal" @ok="submitModal" ok-variant="info" hide-footer>
    <b-form>
      <b-form-group label="Name" :label-cols="3" :horizontal="true">
        <b-form-input id="fullname" v-model="fullname" type="text" disabled></b-form-input>
      </b-form-group>
      <b-form-group label="Username" :label-cols="3" :horizontal="true">
        <b-form-input id="username" v-model="username" type="text" disabled></b-form-input>
      </b-form-group>
      <b-form-group label="Email" :label-cols="3" :horizontal="true">
        <b-form-input id="email" v-model="email" type="text" disabled></b-form-input>
      </b-form-group>
      <b-form-group label="Password" :label-cols="3" :horizontal="true">
        <b-form-input id="password" v-model="password" type="password" aria-describedby="passwordIncorrect" :state="!$v.password.$invalid"></b-form-input>
        <b-form-invalid-feedback id="passwordIncorrect">
          This is a required field and must be at least 8 characters
        </b-form-invalid-feedback>
      </b-form-group>
      <b-button block variant="success" @click='submitModal' :disabled="$v.$invalid">Save</b-button>
    </b-form>
  </b-modal>
</template>

<script>
import axios from 'axios'
import store from '@/store'
import { validationMixin } from 'vuelidate'
import { minLength } from 'vuelidate/lib/validators'
export default {
  props: ['userModal'],
  methods: {
    closedModal: function () {
      this.cleanModal()
      this.$emit('closed-modal')
    },
    submitModal (evt) {
      if (!this.$v.$invalid) {
        const data = {
          username: this.username,
          password: this.password
        }
        axios.post(store.getters.baseUrl + '/users/postUserInfo', data, { headers: { Authorization: `${store.getters.jwt}` } })
          .then((response) => {
            this.$toast.success({
              title: 'Success',
              message: 'Password saved'
            })
          })
          .catch(() => {
            console.log('failed to save!')
            this.$toast.error({
              title: 'Error',
              message: 'Something went wrong saving the password'
            })
          })
        // this.$refs.userInfoModal.hide()
        this.$emit('closed-modal')
      } else {
        evt.preventDefault()
      }
    },
    fetchUserInfo: function () {
      axios.get(store.getters.baseUrl + '/users/getUserInfo', { headers: { Authorization: `${store.getters.jwt}` } })
        .then((response) => {
          store.commit('SET_USER_INFO', {data: response.data})
          this.fullname = response.data.firstname + ' ' + response.data.lastname
          this.username = response.data.username
          this.email = response.data.email
        })
        .catch(() => {
          this.$toast.error({
            title: 'Error',
            message: 'Couldn\'t fetch information. Session expired'
          })
          store.commit('LOGOUT_SESSION')
        })
    },
    cleanModal: function () {
      this.password = ''
    }
  },
  watch: {
    userModal (v) {
      this.modal = v
      if (this.modal) {
        this.fetchUserInfo()
      }
    }
  },
  data: function () {
    return {
      modal: this.userModal,
      fullname: '',
      username: '',
      email: '',
      password: ''
    }
  },
  mixins: [
    validationMixin
  ],
  validations: {
    password: {
      minLenght: minLength(8)
    }
  }
}
</script>
