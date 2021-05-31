<template>
  <b-container fluid class="mb-3">
    <b-row align-h="center">
      <b-col lg="6">
        <b-card class="login-box" title="Login">
          <b-form @submit="onSubmit" :novalidate="true">
            <b-form-group label="Benutzername" label-for="userInput">
              <b-form-input type="text" id="userInput" v-model.trim="$v.form.username.$model" :state="validateState('username')"></b-form-input>
              <b-form-invalid-feedback>
                Kein Benutzername angegeben!
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-group label="Passwort" label-for="passwordInput">
              <b-form-input type="password" id="passwordInput" class="mb-2" v-model.trim="$v.form.password.$model" :state="validateState('password')"></b-form-input>
              <b-form-invalid-feedback>
                Kein Passwort angegeben!
              </b-form-invalid-feedback>
              Noch kein Passwort festgelegt? - <b-link to="signin">Registrieren</b-link>
            </b-form-group>
            <b-button class="float-right" type="submit" variant="primary">Anmelden</b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import { formValidation } from '@/scripts/formValidation'

export default {
  name: "Login",
  mixins: [formValidation],
  data() {
    return {
      form: {
        username: null,
        password: null
      }
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
      this.validateSubmit(event)
    }
  }
}
// POST /login?username=''?password=''
// Rückgabe: Bestätigung des Anmeldevorgangs
// Submit Request -> Verschlüsselung des Passworts
</script>

<style>

</style>