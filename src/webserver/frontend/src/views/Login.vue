<template>
  <b-container fluid class="mb-3">
    <b-alert variant="danger" :show="loginState == false">
      Nutzername oder Passwort falsch!
    </b-alert>

    <b-row align-h="center">
      <b-col lg="6">
        <b-card class="login-box" title="Login">
          <b-form @submit="onSubmit" :novalidate="true">
            <b-form-group label="Nutzername" label-for="userInput">
              <b-form-input type="text" id="userInput" v-model.trim="$v.form.username.$model" :state="validateState('username')"></b-form-input>
              <b-form-invalid-feedback>
                Kein Nutzername angegeben!
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-group label="Passwort" label-for="passwordInput">
              <b-form-input type="password" id="passwordInput" class="mb-2" v-model.trim="$v.form.password.$model" :state="validateState('password')"></b-form-input>
              <b-form-invalid-feedback>
                Kein Passwort angegeben!
              </b-form-invalid-feedback>
              Noch kein Passwort festgelegt? - <b-link to="signup">Registrieren</b-link>
            </b-form-group>
            <b-button class="float-right" type="submit" variant="primary" :disabled="loginLoader">
              <b-spinner v-show="loginLoader" small></b-spinner>
              Anmelden
            </b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import { formValidation } from '@/scripts/formValidation'
import { authService } from '@/scripts/auth'
import { required } from 'vuelidate/lib/validators'

export default {
  name: "Login",
  mixins: [formValidation, authService],
  data() {
    return {
      loginLoader: false,
      loginState: null
    }
  },
  validations: {
    form: {
      username: { required },
      password: { required }
    }
  },
  methods: {
    onSubmit(event) {
      if (this.validateSubmit(event)) this.postLogin()
    },

    async postLogin() {
      this.loginLoader = true

      var loginCredentials = {
        username: this.form.username,
        password: this.form.password
      }

      await axios.post("http://localhost:5000/login", loginCredentials)
      .then(() => {
        // login successful
        this.$router.push("/") // go to homepage
      }).catch(error => {
        // login failed (either network error or wrong credentials)
        console.log(error)
        this.$v.$reset()
        this.loginState = false
        this.loginLoader = false
      });
    }
  }
}
</script>