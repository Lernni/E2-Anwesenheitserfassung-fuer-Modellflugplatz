<template>
  <div class="edit-session">
    <h2>Flugsession bearbeiten</h2>

    <b-alert variant="danger" :show="submitState == false" dismissable>
      Flugsession konnte nicht bearbeitet werden!
    </b-alert>

    <b-alert variant="success" :show="submitState">
      Flugession wurde erfolgreich bearbeitet!<br/><br/>
      Weiterleitung zur Protokollübersicht...
    </b-alert>

    <b-alert variant="danger" :show="sessionState == false">
      Die angeforderte Flugsession konnte nicht geladen werden!
    </b-alert>

    <b-overlay :show="sessionLoader">
      <b-form v-show="sessionState" @submit="onSubmit" :novalidate="true">
        <h4>Informationen</h4>
        <b-table-simple>
          <b-tbody>
            <b-tr>
              <b-th class="text-right">Pilot</b-th>
              <b-td>{{ form.pilotName }}</b-td>
            </b-tr>
            <b-tr>
              <b-th class="text-right">Datum</b-th>
              <b-td>{{ form.date }}</b-td>
            </b-tr>
            <b-tr>
              <b-th class="text-right">Von</b-th>
              <b-td>{{ form.startTime }}</b-td>
            </b-tr>
            <b-tr>
              <b-th class="text-right">Bis</b-th>
              <b-td>{{ form.endTime }}</b-td>
            </b-tr>
            <b-tr>
              <b-th class="text-right">Flugleiter</b-th>
              <b-td>{{ form.sessionLeader }}</b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>

        <h4>Gast</h4>
        <b-form-group id="guest-name-group" label="Gastname" label-for="guest-input">
          <b-form-input id="guest-input" v-model.trim="$v.form.guestName.$model" :state="validateState('guestName')"></b-form-input>
          <b-form-invalid-feedback>
            Ungültiger Gastname
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group id="guest-info-group" label="Gastinformationen" label-for="guest-textarea">
          <b-form-textarea id="guest-textarea" v-model="form.guestText" rows="3"></b-form-textarea>
        </b-form-group>

        <b-button type="submit" variant="primary" :disabled="submitLoader">
          <b-spinner v-show="submitLoader" small></b-spinner>
          Speichern
        </b-button>
      </b-form>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios'
import { required, helpers } from 'vuelidate/lib/validators'
import { formValidation } from '@/scripts/formValidation'
import { formSession } from '@/scripts/session'

const guestNameRegex = helpers.regex("guestNameRegex", /^([A-Z][a-zöäüß]+)([- ]([A-Z][a-zöäüß]+) )*([a-z]+ )*([A-Z][a-zöäüß]+)([-]([A-Z][a-zöäüß]+))*$/) 

export default {
  name: "EditSession",
  mixins: [formValidation, formSession],
  data() {
    return {
      sessionId: null,
      sessionLoader: false,

      submitState: null,
      submitLoader: false
    }
  },
  validations: {
    form: {
      guestName: {
        required,
        guestNameRegex
      }
    }
  },
  async mounted() {
    this.sessionId = this.$route.query.id
    this.sessionLoader = true

    await axios.get("http://localhost:5000/sessions?id=" + this.sessionId)
      .then(response => {
        this.sessionLoader = false

        var session = response.data['sessions'][0]

        this.form.pilotName = session.pilot_name
        this.form.date = session.date
        this.form.startTime = session.start_time
        this.form.endTime = session.end_time
        this.form.sessionLeader = session.session_leader
        this.form.guestName = session.guest_name
        this.form.guestText = session.guest_info
      })
      .catch(error => {
        this.sessionLoader = false
        this.sessionState = false
        console.error(error);
    });
  },
  methods: {
    onSubmit(event) {
      if (this.validateSubmit(event)) { this.editSession() }
    },

    async editSession() {
      this.submitLoader = true

      const newSession = {
        session_id: this.sessionId,
        guest_name: this.form.guestName,
        guest_info: this.form.guestText
      }

      await axios.put("http://localhost:5000/sessions", newSession)
        .then(() => {
          this.submitLoader = false
          this.submitState = true
          setTimeout(() => {this.$router.go(-1)}, 3000)
        })
        .catch(error => {
          console.log(error)
          this.submitLoader = false
          this.submitState = false
        });
    }
  }
}
</script>

<style>

</style>