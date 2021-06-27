<!--
  *** NewPilot.vue ***
  - implementiert Pilot.vue zum Erstellen eines Piloten
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
-->

<template>
  <div class="new-pilot">
    <!-- Weiterleitung von Events in Pilot an eigene Methoden: @formSubmit = "onSubmit" -->
    <Pilot
      header="Pilot erstellen"
      submitText="Speichern"
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
          Pilot wurde erfolgreich angelegt!<br><br>
          <b-button variant="success" @click="resetPilot()">Weiteren Piloten erstellen</b-button>
        </b-alert>

        <b-alert variant="info" :show="rfidList.noRfid">
          Kein freier RFID-Tag verfügbar! Fügen Sie dem System einen neuen RFID-Tag hinzu, bevor Sie einen Piloten erstellen.<br/><br/>
          <b-button variant="info" to="/settings?rfid_tags">RFID-Tag hinzufügen</b-button>
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
import Pilot from '@/components/Pilot.vue'
import { formPilot } from '@/scripts/pilot'
import { formValidation } from '@/scripts/formValidation'

export default {
  name: "NewPilot",
  mixins: [formPilot, formValidation],
  components: {
    Pilot
  },

  methods: {
    resetPilot() {
      this.submit.submitState = null
      // Zurücksetzen der State-Markierungen im Formular
      // siehe https://stackoverflow.com/questions/64512752/vuelidate-set-dirty-false-for-all-properties-when-form-is-submitted
      this.$v.$reset()
    },

    onSubmit(event) {
      if (this.validateSubmit(event)) this.newPilot()
    },

    async newPilot() {
      this.submit.submitLoader = true

      const newPilot = {
        pilot_name: this.form.pilotName,
        pilot_surname: this.form.pilotSurname,
        // TODO: Auskommentieren, wenn e-ID implementiert wurde
        // e_id: this.form.eID,
        rfid: this.form.rfid,
        pilot_username: this.form.pilotUsername,
        is_admin: this.form.isAdmin
      }

      await this.$axios.post("/pilots", newPilot)
        .then(() => {
          this.submitSuccess()
          // Vorbereitung für die Erstellung weiterer Piloten
          this.getRfidList()
          this.getPilotUsernames()
        })
        .catch(error => {this.submitFailure(error)});
    }
  },
  mounted() {
    this.getRfidList()
    this.getPilotUsernames()
  }
}
</script>