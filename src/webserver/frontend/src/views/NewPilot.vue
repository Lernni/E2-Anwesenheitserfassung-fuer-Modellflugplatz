<template>
  <div class="new-pilot">
    <h2>Pilot erstellen</h2>
    <b-container class="w-75">
      <b-alert variant="success" :show="submitState" dismissible>
        Pilot wurde erfolgreich angelegt!
      </b-alert>

      <b-alert variant="danger" :show="submitState == false" dismissible>
        Pilot konnte nicht angelegt werden!<br>
        {{submitErrorMsg}}
      </b-alert>

    
      <b-form @submit="onSubmit" @reset="onReset" :novalidate="true">

        <h4>Pilotendaten</h4>
        <b-row cols="2">
          <b-col>
            <b-form-group label="Nachname" label-for="pilot-surname-input">
              <b-form-input id="pilot-surname-input" v-model.trim="$v.form.pilot_surname.$model" :state="validateState('pilot_surname')"></b-form-input>
              <b-form-invalid-feedback>
                Ungültiger Nachname
              </b-form-invalid-feedback>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Vorname" label-for="pilot-name-input">
              <b-form-input id="pilot-name-input" v-model.trim="$v.form.pilot_name.$model" :state="validateState('pilot_name')"></b-form-input>
              <b-form-invalid-feedback>
                Ungültiger Vorname
              </b-form-invalid-feedback>
            </b-form-group>
          </b-col>
          <b-col>
            <RfidList @selectedRfid='form.rfid_code = $event'/>
          </b-col>
        </b-row>

        <h4>Login-Informationen</h4>
        <b-row cols="2">
          <b-col>
            <b-form-group label="Nutzername" label-for="pilot-username-input" description="Der Pilot vergibt das Passwort beim ersten Anmeldeversuch selbst.">
              <b-form-input id="pilot-username-input" v-model.trim="$v.form.pilot_username.$model" :state="validateState('pilot_username')"></b-form-input>
              <b-form-invalid-feedback>
                Ungültiger Nutzername
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-checkbox id="admin-checkbox" v-model="form.is_admin" name="admin-checkbox">
              Pilot hat Adminrechte
            </b-form-checkbox>
          </b-col>
        </b-row>
        
        <b-button class="mt-3" type="submit" variant="primary" :disabled="submitLoader">
          <b-spinner v-show="submitLoader" small></b-spinner>
          Speichern
        </b-button>
      </b-form>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
import { required, helpers } from 'vuelidate/lib/validators'
import RfidList from '@/components/RfidList.vue'

const surname_regex = helpers.regex("surname_regex", /^([a-z]+ )*([A-Z][a-zöäüß]+)([-]([A-Z][a-zöäüß]+))*$/)
const name_regex = helpers.regex("name_regex", /^([A-Z][a-zöäüß]+)([- ]([A-Z][a-zöäüß]+))*$/)
const username_regex = helpers.regex("username_regex", /^[a-z][a-z0-9_-]{2,15}$/)

export default {
  name: "NewPilot",
  components: {
    RfidList
  },
  data() {
    return {
      form: {
        pilot_surname: null,
        pilot_name: null,
        rfid_code: null,
        pilot_username: null,
        is_admin: false,
      },

      submitLoader: false,
      submitState: null,
      submitErrorMsg: null
    }
  },
  validations: {
    form: {
      pilot_surname: {
        required,
        surname_regex
      },
      pilot_name: {
        required,
        name_regex
      },
      pilot_username: {
        required,
        username_regex
      },
      rfid_code: {
        // TODO: show invalid message
        required
      }
    }
  },
  methods: {
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name];
      return $dirty ? !$error : null;
    },
    onSubmit(event) {
      event.preventDefault()
      this.$v.form.$touch()
      if (!this.$v.form.$anyError) {
        this.postNewPilot()
      }
    },
    // TODO: access reset event
    onReset(event) {
      event.preventDefault()
      this.form.pilot_surname = null
      this.form.pilot_name = null
      this.form.rfid_code = null
      this.form.is_admin = false
    },

    async postNewPilot() {
      this.submitLoader = true

      const newPilot = {
        pilot_name: this.form.pilot_name,
        pilot_surname: this.form.pilot_surname,
        rfid_code: this.form.rfid_code,
        pilot_username: this.form.pilot_username,
        is_admin: this.form.is_admin
      }

      await axios.post("http://localhost:5000/pilots", newPilot)
        .then(() => {
          this.submitLoader = false
          this.submitState = true
        })
        .catch(error => {
          console.error(error);
          this.submitLoader = false
          this.submitState = false
          this.submitErrorMsg = error
      });
    }
  }
}
</script>

<style>

</style>