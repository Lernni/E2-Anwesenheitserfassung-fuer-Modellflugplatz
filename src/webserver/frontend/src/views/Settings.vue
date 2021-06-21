<template>
  <div class="settings">

    <b-modal id="pilot-checkout-modal" title="Uhrzeit der täglichen Pilotenabmeldung">
      <b-form-group id="pilot-checkout-group" label="Uhrzeit auswählen" label-for="pilot-checkout-time-input">
        <b-form-input id="pilot-checkout-time-input" v-model="settings.checkout_time" type="time"></b-form-input>
      </b-form-group>

      <template #modal-footer>
        <b-button variant="secondary" @click="$bvModal.hide('pilot-checkout-modal')">Abbrechen</b-button>
        <b-button :disabled="submitLoader" variant="primary" @click="submitSetttings('pilot-checkout-modal')">
          <b-spinner v-show="submitLoader" small></b-spinner>
          Speichern
        </b-button>
      </template>
    </b-modal>

    <b-modal id="rfid-tag-modal" size="lg" title="RFID-Tags verwalten">
      <b-container fluid>
        <b-form>
          <b-row class="justify-content-center">
            <b-col>
              <b-alert variant="success" :show="addRfidState">
                RFID-Tag wurde erfolgreich hinzugefügt
              </b-alert>
              <b-alert variant="danger" :show="addRfidState == false">
                RFID-Tag konnte nicht hinzugefügt werden!
              </b-alert>
              <b-form @submit="onSubmitRfidTag" :novalidate="true">
                <b-form-group id="rfid-input-group" label="RFID-Tag hinzufügen" label-for="rfid-input">
                  <b-input-group id="rfid-input" prepend="0x">
                    <b-form-input v-model.trim="$v.form.rfidTag.$model" :state="validateState('rfidTag')"></b-form-input>
                    <b-input-group-append>
                      <b-button variant="success" type="submit" :disabled="addRfidLoader">
                        <b-spinner v-show="addRfidLoader" small></b-spinner>
                        <b-icon-plus v-show="!addRfidLoader" scale="1.5"></b-icon-plus>
                        Hinzufügen
                      </b-button>
                    </b-input-group-append>
                  </b-input-group>
                  <b-form-invalid-feedback :state="validateState('rfidTag')">
                    Ungültiger RFID-Tag! RFID-Tag muss hexadezimal angegeben werden!
                  </b-form-invalid-feedback>
                </b-form-group>
              </b-form>
            </b-col>
          </b-row>
          <b-row class="justify-content-center">
            <b-col cols="12" md="6">
              <b-form-group id="free-rfid-group" label="Frei" label-for="free-rfid-table">
                <b-overlay :show="freeRfidLoader" spinner-type="grow">
                  <b-table sticky-header :items="freeRfidList" :fields="freeRfidFields" head-variant="light">
                    <template #cell()="row">
                      {{ row.item }}
                    </template>
                  </b-table>
                </b-overlay>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group id="used-rfid-group" label="Vergeben" label-for="used-rfid-table">
                <b-overlay :show="usedRfidLoader" spinner-type="grow">
                  <b-table sticky-header :items="usedRfidList" :fields="usedRfidFields" head-variant="light"></b-table>
                </b-overlay>
              </b-form-group>
            </b-col>
          </b-row>
        </b-form>
      </b-container>

      <template #modal-footer>
        <b-button variant="primary" @click="$bvModal.hide('rfid-tag-modal')">
          OK
        </b-button>
      </template>
    </b-modal>

    <b-modal id="terminal-config-modal" size="lg" title="Tasten- & Bedienkonfiguration">
      <b-container>
        <b-row cols="3" class="align-items-center" v-for="config in settings.terminal_config" :key="config.name">
          <b-col cols="12" lg="2" class="pl-0">
            {{ config.name }}:
          </b-col>
          <b-col class="d-flex align-items-center py-2 px-0" cols="12" md="6" lg="5">
            <b-input-group append="Sek" class="mr-3">
              <b-form-input v-model="config.duration" min="0" type="number"></b-form-input>
            </b-input-group>
            <b-form-checkbox v-model="config.button" class="mr-3">
              Taster
            </b-form-checkbox>
          </b-col>
          <b-col class="d-flex align-items-center py-2 px-0" cols="12" md="6" lg="5">
            <b-input-group append="LED" class="mr-3">
              <b-form-input v-model="config.color" type="color"></b-form-input>
            </b-input-group>
            <b-form-checkbox v-model="config.blinking">
              Blinken
            </b-form-checkbox>
          </b-col>
        </b-row>
      </b-container>

      <template #modal-footer>
        <b-button variant="secondary" @click="$bvModal.hide('terminal-config-modal')">Abbrechen</b-button>
        <b-button :disabled="submitLoader" variant="primary" @click="submitSetttings('terminal-config-modal')">
          <b-spinner v-show="submitLoader" small></b-spinner>
          Speichern
        </b-button>
      </template>
    </b-modal>

    <b-modal id="tolerance-time-modal" title="Toleranzzeit bei An- & Abmeldung">
      <b-form-group id="tolerance-time-group" label="Toleranzzeit auswählen" label-for="tolerance-time-input">
        <b-input-group append="Min">
          <b-form-input min="0" id="tolerance-time-input" v-model="settings.tolerance" type="number"></b-form-input>
        </b-input-group>
      </b-form-group>

      <template #modal-footer>
        <b-button variant="secondary" @click="$bvModal.hide('tolerance-time-modal')">Abbrechen</b-button>
        <b-button :disabled="submitLoader" variant="primary" @click="submitSetttings('tolerance-time-modal')">
          <b-spinner v-show="submitLoader" small></b-spinner>
          Speichern
        </b-button>
      </template>
    </b-modal>

    <h2>Einstellungen</h2>

    <b-alert variant="success" :show="submitState">
      Einstellungen erfolgreich gespeichert
    </b-alert>
    <b-alert variant="danger" :show="submitState == false">
      Einstellungen konnten nicht gespeichert werden!
    </b-alert>

    <b-overlay :show="submitLoader" spinner-type="grow">
      <b-container fluid="md">
        <b-row class="justify-content-center">
          <b-col lg="8">
            <br>
            <h4>Allgemeine Einstellungen</h4>
            <b-row cols="2" class="align-items-center">
              <b-col cols="10" md="8" class="py-2">
                Uhrzeit der täglichen Pilotenabmeldung
              </b-col>
              <b-col cols="2" md="4" class="py-2 text-center">
                <b-button variant="primary" v-b-modal.pilot-checkout-modal>
                  <b-icon-pencil-square></b-icon-pencil-square>
                  <span class="ml-1 d-none d-md-inline">Bearbeiten</span>
                </b-button>
              </b-col>
              <b-col cols="10" md="8" class="py-2">
                RFID-Kennungen verwalten
              </b-col>
              <b-col cols="2" md="4" class="py-2 text-center">
                <b-button variant="primary" v-b-modal.rfid-tag-modal>
                  <b-icon-pencil-square></b-icon-pencil-square>
                  <span class="ml-1 d-none d-md-inline">Bearbeiten</span>
                </b-button>
              </b-col>
            </b-row>
            <br>
            <h4>Terminal</h4>
            <b-row cols="2" class="align-items-center">
              <b-col cols="10" md="8" class="py-2">
                Tasten- & Bedienkonfiguration
              </b-col>
              <b-col cols="2" md="4" class="py-2 text-center">
                <b-button variant="primary" v-b-modal.terminal-config-modal>
                  <b-icon-pencil-square></b-icon-pencil-square>
                  <span class="ml-1 d-none d-md-inline">Bearbeiten</span>
                </b-button>
              </b-col>
              <b-col cols="10" md="8" class="py-2">
                Toleranzzeit bei An- & Abmeldung
              </b-col>
              <b-col cols="2" md="4" class="py-2 text-center">
                <b-button variant="primary" v-b-modal.tolerance-time-modal>
                  <b-icon-pencil-square></b-icon-pencil-square>
                  <span class="ml-1 d-none d-md-inline">Bearbeiten</span>
                </b-button>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-container>
    </b-overlay>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import { formValidation } from '@/scripts/formValidation'

export default {
  name: "Settings",
  mixins: [formValidation],
  data() {
    return {
      form: {
        rfidTag: null
      },

      // rfid tags
      addRfidLoader: false,
      freeRfidLoader: false,
      usedRfidLoader: false,
      addRfidState: null,

      freeRfidList: [],
      freeRfidFields: ["RFID-Tags"],

      usedRfidList: [],
      usedRfidFields: [
        {key: "pilot_id", label: "ID"},
        {key: "pilot_name", label: "Pilot"},
        {key: "rfid", label: "RFID-Tag"}
      ],

      // settings
      settingsLoader: false,
      settingsState: null,
      settings: {},

      submitState: null,
      submitLoader: false,
    }
  },
  validations: {
    form: {
      rfidTag: {
        required,
        isHex(value) {
          if (value == null) return false
          var checkNumber = parseInt(value, 16);
          return (checkNumber.toString(16) === value.toLowerCase())
        }
      }
    }
  },
  mounted() {
    var showRfid = this.$route.query.rfid_tags
    if (showRfid !== undefined) this.$bvModal.show('rfid-tag-modal')

    this.getFreeRfidList()
    this.getUsedRfidList()
    this.getSettings()
  },
  methods: {
    async submitSetttings(modal) {
      await this.postSettings()
      this.$bvModal.hide(modal)
    },

    onSubmitRfidTag(event) {
      if (this.validateSubmit(event)) { this.addRfidTag() }
    },

    async addRfidTag() {
      this.addRfidLoader = true

      const payload = {
        rfid: this.form.rfidTag
      }

      this.$axios.post("/rfid", payload)
      .then(() => {
        this.addRfidLoader = false
        this.addRfidState = true
        this.form.rfidTag = null
        this.$v.$reset()

        this.getFreeRfidList()
      }).catch(() => {
        this.addRfidLoader = false
        this.addRfidState = false
      })
    },  

    async getSettings() {
      this.settingsLoader = true

      this.$axios.get("/settings")
      .then(response => {
        this.settings = response.data['settings']
        this.settingsState = true
        this.settingsLoader = false
      })
      .catch(error => {
        console.error(error);
        this.settingsState = false
        this.settingsLoader = false
      })
    },

    async postSettings() {
      this.submitLoader = true

      this.$axios.post("/settings", this.settings)
      .then(() => {
        this.submitState = true
        this.submitLoader = false
      })
      .catch(error => {
        console.error(error);
        this.submitState = false
        this.submitLoader = false
      })
    },

    async getFreeRfidList() {
      this.freeRfidLoader = true

      this.$axios.get("/rfid_available")
      .then(response => {
        this.freeRfidList = response.data['rfid_list']
        this.freeRfidLoader = false
      }).catch(error => {
        console.error(error);
        this.freeRfidLoader = false
      });
    },

    async getUsedRfidList() {
      this.usedRfidLoader = true

      this.$axios.get("/rfid_assigned")
      .then(response => {
        this.usedRfidList = response.data['rfid_list']
        this.usedRfidLoader = false
      }).catch(error => {
        console.error(error);
        this.usedRfidLoader = false
      });
    },
  }
}
</script>

<style>

</style>