<template>
  <div class="settings">

    <b-modal id="pilot-checkout-modal" title="Uhrzeit der täglichen Pilotenabmeldung">
      <b-form-group id="pilot-checkout-group" label="Uhrzeit auswählen" label-for="pilot-checkout-time-input">
        <b-form-input id="pilot-checkout-time-input" v-model="pilotCheckoutTime" type="time"></b-form-input>
      </b-form-group>

      <template #modal-footer>
        <b-button variant="secondary" @click="showPilotCheckoutModal = false">Abbrechen</b-button>
        <b-button :disabled="submitLoader" variant="primary" @click="setPilotCheckoutTime()">
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
              <b-form-group id="rfid-input-group" label="RFID-Tag hinzufügen" label-for="rfid-input">
                <b-input-group id="rfid-input" prepend="0x">
                  <b-form-input></b-form-input>
                  <b-input-group-append>
                    <b-button variant="success">
                      <b-icon-plus scale="1.5"></b-icon-plus>
                      Hinzufügen
                    </b-button>
                  </b-input-group-append>
                </b-input-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row class="justify-content-center">
            <b-col cols="12" md="6">
              <b-form-group id="free-rfid-group" label="Frei" label-for="free-rfid-table">
                <b-table sticky-header :items="freeRfidList" :fields="freeRfidFields" head-variant="light"></b-table>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group id="used-rfid-group" label="Vergeben" label-for="used-rfid-table">
                <b-table sticky-header :items="usedRfidList" :fields="usedRfidFields" head-variant="light"></b-table>
              </b-form-group>
            </b-col>
          </b-row>
        </b-form>
      </b-container>

      <template #modal-footer>
        <b-button :disabled="submitLoader" variant="primary" @click="setRFIDList()">
          <b-spinner v-show="submitLoader" small></b-spinner>
          OK
        </b-button>
      </template>
    </b-modal>

    <b-modal id="terminal-config-modal" size="lg" title="Tasten- & Bedienkonfiguration">
      <b-container>
        <b-row cols="3" class="align-items-center" v-for="config in terminalConfig" :key="config.id">
          <b-col cols="12" lg="2" class="pl-0">
            {{ config.name }}:
          </b-col>
          <b-col class="d-flex align-items-center py-2 px-0" cols="12" md="6" lg="5">
            <b-input-group append="Sek" class="mr-3">
              <b-form-input v-model="config.time" min="0" type="number"></b-form-input>
            </b-input-group>
            <b-form-checkbox v-model="config.leaderButton" id="leader-button-checkbox" name="leader-button-checkbox" class="mr-3">
              Taster
            </b-form-checkbox>
          </b-col>
          <b-col class="d-flex align-items-center py-2 px-0" cols="12" md="6" lg="5">
            <b-input-group append="LED" class="mr-3">
              <b-form-input v-model="config.color" type="color"></b-form-input>
            </b-input-group>
            <b-form-checkbox  v-model="config.ledBlinkButton" id="led-blink-checkbox" name="led-blink-checkbox">
              Blinken
            </b-form-checkbox>
          </b-col>
        </b-row>
      </b-container>

      <template #modal-footer>
        <b-button variant="secondary" @click="showPilotCheckoutModal = false">Abbrechen</b-button>
        <b-button :disabled="submitLoader" variant="primary" @click="setTerminalSettings()">
          <b-spinner v-show="submitLoader" small></b-spinner>
          Speichern
        </b-button>
      </template>
    </b-modal>

    <b-modal id="tolerance-time-modal" title="Toleranzzeit bei An- & Abmeldung">
      <b-form-group id="tolerance-time-group" label="Toleranzzeit auswählen" label-for="tolerance-time-input">
        <b-input-group append="Min">
          <b-form-input min="0" id="tolerance-time-input" v-model="toleranceTime" type="number"></b-form-input>
        </b-input-group>
      </b-form-group>

      <template #modal-footer>
        <b-button variant="secondary" @click="showToleranceTimeModal = false">Abbrechen</b-button>
        <b-button :disabled="submitLoader" variant="primary" @click="setToleranceTime()">
          <b-spinner v-show="submitLoader" small></b-spinner>
          Speichern
        </b-button>
      </template>
    </b-modal>

    <h2>Einstellungen</h2>
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
  </div>
</template>

<script>
export default {
  name: "Settings",
  data() {
    return {
      // pilot checkout
      pilotCheckoutTime: 0,

      // rfid tags
      freeRfidList: [],
      freeRfidFields: [
        {key: "rfid", label: "RFID-Tag"},
        {key: "actions", label: ""}
      ],
      usedRfidList: [],
      usedRfidFields: [
        {key: "pilot_id", label: ""},
        {key: "pilot_name", label: "Pilot"},
        {key: "rfid", label: "RFID-Tag"}
      ],

      // terminal config
      // test objects
      terminalConfig: [
        {
          id: 0,
          name: "Anmeldung",
          time: 3,
          leaderButton: true,
          color: "#aaabbb",
          ledBlinkButton: true
        },
        {
          id: 1,
          name: "Abmeldung",
          time: 3,
          leaderButton: true,
          color: "#aaa333",
          ledBlinkButton: true
        },
        {
          id: 2,
          name: "Flugleiter",
          time: 3,
          leaderButton: true,
          color: "#33fa3b",
          ledBlinkButton: false
        },
        {
          id: 3,
          name: "Alle Piloten abmelden",
          time: 10,
          leaderButton: true,
          color: "#4455aa",
          ledBlinkButton: true
        },
      ],

      // tolerance time
      toleranceTime: 0,

      submitLoader: false,
    }
  },
  mounted() {
    this.getRfidList()
  },
  methods: {
    async getRfidList() {

      this.$axios.get("http://localhost:5000/rfid")
      .then(response => {
        this.freeRfidList = response.data['rfid_list']
        console.log(this.freeRfidList)
      }).catch(error => {
        console.error(error);
      });
    },
  }
}
</script>

<style>

</style>