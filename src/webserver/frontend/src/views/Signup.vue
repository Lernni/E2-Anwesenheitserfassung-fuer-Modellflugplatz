<template>
  <b-container fluid class="mb-3">

    <b-alert variant="success" :show="signupState">
      Pilot wurde erfolgreich registriert!<br/><br/>
      <b-button variant="success" to="login">
        Weiter zum Login
      </b-button>
    </b-alert>

    <b-alert variant="danger" :show="signupState == false">
      Pilot konnte nicht registriert werden! Das Passwort wurde bereits vergeben!
    </b-alert>

    <b-row align-h="center">
      <b-col lg="6">
        <b-card class="signup-box" title="Registrieren">
          <b-form @submit="onSubmit" :novalidate="true">
            <b-form-group label="Nutzername" label-for="userInput">
              <b-form-input type="text" id="userInput" v-model.trim="$v.form.username.$model" :state="validateState('username')"></b-form-input>
              <b-form-invalid-feedback>
                Kein Nutzername angegeben!
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-group label="Passwort" label-for="passwordInput">
              <b-form-input type="password" id="passwordInput" v-model.trim="$v.form.password.$model" :state="validateState('password')"></b-form-input>
              <b-form-invalid-feedback>
                Kein Passwort angegeben!
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-group label="Passwort bestätigen" label-for="passwordInput">
              <b-form-input type="password" id="passwordRepeatInput" v-model.trim="$v.form.repeatPassword.$model" :state="validateState('repeatPassword')"></b-form-input>
              <b-form-invalid-feedback>
                Die Passwörter müssen identisch sein!
              </b-form-invalid-feedback>
            </b-form-group>
            <b-button class="float-right" type="submit" variant="primary" :disabled="signupLoader">
              <b-spinner v-show="signupLoader" small></b-spinner>
              Registrieren
            </b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'
import { authService } from '@/scripts/auth'
import { formValidation } from '@/scripts/formValidation'
import { required, sameAs } from 'vuelidate/lib/validators'

export default {
  name: "Signup",
  mixins: [authService, formValidation],
  data() {
    return {
      signupLoader: false,
      signupState: null,

      form: {
        repeatPassword: null
      }
    }
  },
  validations: {
    form: {
      username: { required },
      password: { required },
      repeatPassword: {
        required,
        sameAsPassword: sameAs('password')
      }
    }
  },
  methods: {
    onSubmit(event) {
      if (this.validateSubmit(event)) this.postSignup()
    },

    async postSignup() {
      this.signupLoader = true

      var signupCredentials = {
        username: this.form.username,
        password: this.encryptPassword(this.form.password)
      }

      await axios.post("http://localhost:5000/signup", signupCredentials)
      .then(() => {
        // signup successful
        this.signupLoader = false
        this.signupState = true
      }).catch(error => {
        // signup failed (either network error or password already set)
        console.log(error)
        this.$v.$reset()
        this.signupLoader = false
        this.signupState = false
      });
    }
  }
}
</script>