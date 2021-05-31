<template>
  <b-container fluid class="mb-3">
      <b-row align-h="center">
        <b-col lg="6">
          <b-card class="signin-box" title="Registrieren">
            <b-form @submit="onSubmit" :novalidate="true">
              <b-form-group label="Benutzername" label-for="userInput">
                <b-form-input type="text" id="userInput" v-model.trim="$v.form.username.$model" :state="validateState('username')"></b-form-input>
                <b-form-invalid-feedback>
                  Kein Benutzername angegeben!
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
              <b-button class="float-right" type="submit" variant="primary">Registrieren</b-button>
            </b-form>
          </b-card>
        </b-col>
      </b-row>
  </b-container>
</template>

<script>
import { required, sameAs } from 'vuelidate/lib/validators'
import { formValidation } from '@/scripts/formValidation'

export default {
  name: "Signin",
  mixins: [formValidation],
  data() {
    return {
      form: {
        username: null,
        password: null,
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
      this.validateSubmit(event)
    }
  }
}
</script>