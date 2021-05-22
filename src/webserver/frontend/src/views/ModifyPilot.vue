<template>
  <div class="modify-pilot">
    <h2>Pilot bearbeiten</h2>
    <b-container class="w-75">
      <b-alert variant="success" :show="submitState" dismissible>
        Pilot wurde erfolgreich bearbeitet!<br/><br/>
        Weiterleitung zur Pilotenübersicht...
      </b-alert>

      <b-alert variant="danger" :show="submitState == false" dismissible>
        Pilot konnte nicht bearbeitet werden!<br>
        {{submitErrorMsg}}
      </b-alert>

      <b-alert variant="danger" :show="pilotError">
        Der angeforderte Pilot konnte nicht geladen werden!
      </b-alert>
      
      <b-overlay :show="pilotLoader">
        <b-form v-show="!pilotError" @submit="onSubmit" @reset="onReset" :novalidate="true">

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
              <b-form-group label="Nutzername" label-for="pilot-username-input">
                <b-form-input id="pilot-username-input" v-model.trim="$v.form.pilot_username.$model" :state="validateState('pilot_username')"></b-form-input>
                <b-form-invalid-feedback>
                  Ungültiger Nutzername
                </b-form-invalid-feedback>
              </b-form-group>
              <b-form-checkbox class="mb-2" id="reset-pwd-checkbox" v-model="form.reset_password" name="reset-pwd-checkbox">
                Passwort zurücksetzen
              </b-form-checkbox>
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
      </b-overlay>
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
  name: "ModifyPilot",
  components: {
    RfidList
  },
  data() {
    return {
      form: {
        pilot_id: this.$route.query.id,
        pilot_surname: null,
        pilot_name: null,
        rfid_code: null,
        pilot_username: null,
        is_admin: false,
        reset_password: false
      },

      pilotLoader: false,
      pilotError: false,

      submitState: null,
      submitError: false,
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
  async mounted() {

    this.form.pilot_id = this.$route.query.id
    this.pilotLoader = true 

    await axios.get("http://localhost:5000/pilots?id=" + this.form.pilot_id)
      .then(response => {
        this.pilotLoader = false

        var pilot = response.data['pilots'][0]
        console.log(pilot)

        this.form.pilot_surname = pilot.pilot_surname
        this.form.pilot_name = pilot.pilot_name
        this.form.rfid_code = pilot.rfid_code
        this.form.pilot_username = pilot.pilot_username
        this.form.is_admin = pilot.is_admin
      })
      .catch(error => {
        this.pilotLoader = false
        this.pilotError = true
        console.error(error);
    });
  },
  // TODO: Vorauswahl für eigenen Ausweis
  methods: {
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name];
      return $dirty ? !$error : null;
    },
    onSubmit(event) {
      event.preventDefault()
      this.$v.form.$touch()
      if (!this.$v.form.$anyError) {
        this.updatePilot()
      }
    },
    // TODO: access reset event
    onReset(event) {
      event.preventDefault()
      this.form.pilot_surname = null
      this.form.pilot_name = null
      this.form.rfid_code = null
      this.form.is_admin = false
      this.form.reset_password = false
    },

    async updatePilot() {
      this.submitLoader = true

      const newPilot = {
        pilot_id: this.form.pilot_id,
        pilot_name: this.form.pilot_name,
        pilot_surname: this.form.pilot_surname,
        rfid_code: this.form.rfid_code,
        pilot_username: this.form.pilot_username,
        reset_password: this.form.reset_password,
        is_admin: this.form.is_admin,
      }

      await axios.put("http://localhost:5000/pilots", newPilot)
        .then(() => {
          this.submitLoader = false
          this.submitState = true
          setTimeout(() => {this.$router.go(-1)}, 3000)
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