<template>
  <div class="modify-pilot">
    <Pilot
      header="Pilot bearbeiten"
      submitText="Speichern"
      v-model="$v.form"
      :states="validateAll()"
      :submit="submit"
      :rfidList="rfidList"
      :pilot="pilot"
      @formSubmit="onSubmit"
    >
      <template v-slot:alerts>
        <b-alert variant="success" :show="submit.submitState" dismissible>
          Pilot wurde erfolgreich bearbeitet!<br/><br/>
          Weiterleitung zur Pilotenübersicht...
        </b-alert>

        <b-alert variant="danger" :show="submit.submitState == false" dismissible>
          Pilot konnte nicht bearbeitet werden!<br>
          {{ submit.submitErrorMsg }}
        </b-alert>

        <b-alert variant="danger" :show="pilot.pilotState == false">
          Der angeforderte Pilot konnte nicht geladen werden!
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
// TODO: Überprüfe, ob man einen deaktivierten Piloten bearbeiten kann
import axios from 'axios'
import Pilot from '@/components/Pilot.vue'
import { formPilot } from '@/scripts/pilot'

export default {
  name: "EditPilot",
  mixins: [formPilot],
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

    await axios.get("http://localhost:5000/pilots?id=" + this.pilotId)
      .then(response => {
        this.pilot.pilotLoader = false

        var pilot = response.data['pilots'][0]

        this.form.pilotSurname = pilot.pilot_surname
        this.form.pilotName = pilot.pilot_name
        this.form.pilotUsername = pilot.pilot_username
        this.form.isAdmin = pilot.is_admin

        this.rfidList.rfidList.unshift(pilot.rfid)
        this.form.rfid = pilot.rfid
      })
      .catch(error => {
        this.pilot.pilotLoader = false
        this.pilot.pilotState = false
        console.error(error);
    });
  },

  methods: {
    async pilotRequest() {
      this.submit.submitLoader = true

      const newPilot = {
        pilot_id: this.pilotId,
        pilot_name: this.form.pilotName,
        pilot_surname: this.form.pilotSurname,
        rfid: this.form.rfid,
        pilot_username: this.form.pilotUsername,
        reset_password: this.resetPassword,
        is_admin: this.form.isAdmin,
      }

      await axios.put("http://localhost:5000/pilots", newPilot)
        .then(() => {
          this.submitSuccess()
          this.resetPassword = false
          setTimeout(() => {this.$router.go(-1)}, 3000)
        })
        .catch(error => {this.submitFailure(error)});
    }
  }
}
</script>