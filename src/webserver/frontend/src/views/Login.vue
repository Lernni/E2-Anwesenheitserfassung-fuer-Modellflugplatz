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
              <b-form-invalid-feedback v-if="!$v.form.username.maxLength">
                Nutzername zu lang!
              </b-form-invalid-feedback>
              <b-form-invalid-feedback>
                Ungültiger Nutzername!
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-group label="Passwort" label-for="passwordInput">
              <b-form-input type="password" id="passwordInput" class="mb-2" v-model.trim="$v.form.password.$model" :state="validateState('password')"></b-form-input>
              <b-form-invalid-feedback v-if="!$v.form.password.minLength">
                Passwort zu kurz!
              </b-form-invalid-feedback>
              <b-form-invalid-feedback v-if="!$v.form.password.maxLength">
                Passwort zu lang!
              </b-form-invalid-feedback>
              <b-form-invalid-feedback>
                Ungültiges Passwort!
              </b-form-invalid-feedback>
              Noch kein Passwort festgelegt? - <b-link to="/signup">Registrieren</b-link>
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
import { formValidation } from '@/scripts/formValidation'
import { authService } from '@/scripts/auth'
import { required, minLength, maxLength } from 'vuelidate/lib/validators'

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
      username: {
        required,
        maxLength: maxLength(100)
      },
      password: {
        required,
        minLength: minLength(6),
        maxLength: maxLength(50)
      }
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

      this.$store.dispatch("login", loginCredentials)
      .then(() => this.$router.push("/"))
      .catch(error => {
        console.log(error)
        this.loginLoader = false
        this.loginState = false
        this.$v.$reset()
      })
    }
  }
}
</script>