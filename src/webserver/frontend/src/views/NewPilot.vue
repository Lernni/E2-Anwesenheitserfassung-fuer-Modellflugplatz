<template>
  <div class="new-pilot">
    <Pilot
      header="Pilot erstellen"
      submitText="Speichern"
      v-model="$v.form"
      :states="validateAll()"
      :submit="submit"
      :rfidList="rfidList"
      :pilot="pilot"
      @formSubmit="onSubmit"
    >
      <template v-slot:alerts>
        <b-alert variant="success" :show="submit.submitState">
          Pilot wurde erfolgreich angelegt!<br/><br/>
          <b-button variant="success" @click="newPilot()">Weiteren Piloten erstellen</b-button>
        </b-alert>

        <b-alert variant="danger" :show="submit.submitState == false" dismissible>
          Pilot konnte nicht angelegt werden!<br>
          {{ submit.submitErrorMsg }}
        </b-alert>
      </template>
    </Pilot>
  </div>
</template>

<script>
import axios from 'axios'
import Pilot from '@/components/Pilot.vue'
import { formPilot } from '@/scripts/pilot'

export default {
  name: "NewPilot",
  mixins: [formPilot],
  components: {
    Pilot
  },

  methods: {
    newPilot() {
      this.submit.submitState = null
      this.$v.$reset()
    },

    async pilotRequest() {
      this.submit.submitLoader = true

      const newPilot = {
        pilot_name: this.form.pilotName,
        pilot_surname: this.form.pilotSurname,
        rfid_code: this.form.rfid,
        pilot_username: this.form.pilotUsername,
        is_admin: this.form.isAdmin
      }

      await axios.post("http://localhost:5000/pilots", newPilot)
        .then(() => {
          this.submitSuccess()
          this.getRfidList()
        })
        .catch(error => {this.submitFailure(error)});
    }
  }
}
</script>