<template>
  <div class="reactivate-pilot">
    <Pilot
      header="Pilot reaktivieren"
      submitText="Reaktivieren"
      v-model="$v.form"
      :states="validateAll()"
      :submit="submit"
      :rfidList="rfidList"
      :pilot="pilot"
      :username="username"
      @formSubmit="onSubmit"
      @setUsername="setUsername"
    >
      <template v-slot:alerts>
        <b-alert variant="success" :show="submit.submitState">
          Pilot wurde erfolgreich reaktiviert!<br><br>
          Weiterleitung zur Pilotenübersicht...
        </b-alert>

        <b-alert variant="danger" :show="submit.submitState == false" dismissible>
          Pilot konnte nicht reaktiviert werden!<br>
          {{ submit.submitErrorMsg }}
        </b-alert>

        <b-alert variant="danger" :show="pilot.pilotState == false">
          Der angeforderte Pilot existiert nicht oder ist bereits aktiviert!
        </b-alert>
      </template>

      <template v-slot:login-form>
        <b-form-checkbox class="mt-2" id="reset-pwd-checkbox" v-model="resetPassword" name="reset-pwd-checkbox">
          Passwort zurücksetzen
        </b-form-checkbox>
      </template>
    </Pilot>
  </div>
</template>

<script>
import axios from 'axios'
import Pilot from '@/components/Pilot.vue'
import { formPilot } from '@/scripts/pilot'
import { formValidation } from '@/scripts/formValidation'

export default {
  name: "ReactivatePilot",
  mixins: [formPilot, formValidation],
  components: {
    Pilot
  },
  data() {
    return {
      pilotId: null,
      resetPassword: false
    }
  },
  async mounted() {
    this.pilotId = this.$route.query.id
    this.pilot.pilotLoader = true 

    await this.getRfidList()
    await this.getPilotUsernames()

    await axios.get("http://localhost:5000/pilots?id=" + this.pilotId + "&is_active=false")
      .then(response => {
        this.pilot.pilotLoader = false

        var pilot = response.data['pilots'][0]

        this.form.pilotSurname = pilot.pilot_surname
        this.form.pilotName = pilot.pilot_name
        this.form.pilotUsername = pilot.pilot_username
        this.form.isAdmin = pilot.is_admin
      })
      .catch(error => {
        this.pilot.pilotLoader = false
        this.pilot.pilotState = false
        console.error(error);
    });
  },
  methods: {
    onSubmit(event) {
      if (this.validateSubmit(event)) this.reactivatePilot()
    },

    async reactivatePilot() {
      this.submit.submitLoader = true

      const newPilot = {
        pilot_id: this.pilotId,
        pilot_name: this.form.pilotName,
        pilot_surname: this.form.pilotSurname,
        rfid: this.form.rfid,
        pilot_username: this.form.pilotUsername,
        reset_password: this.resetPassword,
        is_admin: this.form.isAdmin,
        is_active: true
      }

      await axios.put("http://localhost:5000/pilots", newPilot)
        .then(() => {
          this.submitSuccess()
          this.resetPassword = false
          setTimeout(() => {this.$router.push("/pilots")}, 3000)
        })
        .catch(error => {this.submitFailure(error)});
    }
  }
}
</script>