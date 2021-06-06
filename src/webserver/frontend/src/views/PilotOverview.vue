<template>
  <div class="pilots">
    <h2>Pilotenübersicht</h2>

    <b-alert variant="success" :show="deactivateState" dismissible>
      Pilot wurde erfolgreich deaktiviert!
    </b-alert>

    <b-alert variant="danger" :show="deactivateState == false" dismissible>
      {{ deactivateMsg }}
    </b-alert>

    <b-alert variant="danger" :show="pilotsState == false">
      Piloten konnten nicht geladen werden!
    </b-alert>

    <b-row class="text-center no-gutters mb-2">
      <b-col class="mb-2 mb-md-0">
        <b-input-group prepend="Suche">
          <b-form-input type="search" v-model="pilotName" placeholder="Name"></b-form-input>
        </b-input-group>
      </b-col>
      <b-col cols="12" md="auto">
        <b-button variant="primary" class="ml-md-2" @click="toggleActivePilots()">{{ toggleActivePilotsButton }}</b-button>
        <b-button variant="success" class="ml-2" to="pilots/new">
          <b-icon icon="plus" scale="1.5"></b-icon>
          Pilot erstellen
        </b-button>
      </b-col>
    </b-row>

    <b-modal disabled v-model="showModal" title="Pilot deaktivieren" header-bg-variant="danger" header-text-variant="light">
      Soll {{ toDeactivatePilot.pilot_name }} {{ toDeactivatePilot.pilot_surname }} wirklich deaktiviert werden?<br/><br/>
      Die Zuweisung des RFID-Ausweises zum Piloten wird aufgehoben und der Ausweis wird als frei markiert.

      <template #modal-footer>
        <b-button variant="secondary" @click="showModal = false">Abbrechen</b-button>
        <b-button :disabled="deactivateLoader" variant="danger" @click="deactivatePilot()">
          <b-spinner v-show="deactivateLoader" small></b-spinner>
          Deaktivieren
        </b-button>
      </template>
    </b-modal>

    <b-overlay :show="pilotsLoader" spinner-type="grow">
      <b-table stacked="sm" striped :items="items" :fields="fields" :filter="pilotName">
        <template #cell(pilot_name)="row">
          {{ row.item.pilot_name }} {{ row.item.pilot_surname }}
        </template>

        <template #cell(actions)="row">
          <b-button v-if="!isActive" :href="'/pilots/reactivate?id=' + row.item.pilot_id" size="sm" variant="outline-success" v-b-tooltip.hover title="Reaktivieren">
            <b-icon-plus-circle-fill></b-icon-plus-circle-fill>
            <span class="d-block d-sm-none">Reaktivieren</span>
          </b-button>
          <b-button-group v-else size="sm">
            <b-button variant="outline-primary" :href="'/pilots/edit?id=' + row.item.pilot_id" v-b-tooltip.hover title="Bearbeiten">
              <b-icon-pencil-square></b-icon-pencil-square>
              <span class="d-block d-sm-none">Bearbeiten</span>
            </b-button>
            <b-button variant="outline-danger" @click="showDeactivateModal(row.item)" v-b-tooltip.hover title="Deaktivieren">
              <b-icon-dash-circle-fill></b-icon-dash-circle-fill>
              <span class="d-block d-sm-none">Deaktivieren</span>
            </b-button>
          </b-button-group>
        </template>
      </b-table>
    </b-overlay>
  </div>
</template>

<script>
export default {
  name: 'Pilots',
  data() {
    return {
      items: [],
      fields: [
        {key: "pilot_id", label: "ID"},
        {key: "pilot_name", label: "Name"},
        {
          key: "entry_date",
          label: "Eintrittsdatum",
          formatter: (value) => {
            return new Date(value).toLocaleDateString()
          }
        },
        {
          key: "rfid",
          label: "RFID",
          formatter: (value) => {
            return (value == "null") ? "nicht vergeben" : value
          }
        },
        {key: "actions", label: "", class: "text-center"}
      ],
      toggleActivePilotsButton: "Zeige inaktive Piloten",

      pilotName: null,
      isActive: true,
      searchInput: null,

      toDeactivatePilot: [],
      showModal: false,

      pilotsLoader: false,
      pilotsState: null,

      deactivateLoader: false,
      deactivateState: null,
      deactivateMsg: null,
    };
  },
  methods: {
    showDeactivateModal(pilot) {
      this.toDeactivatePilot = pilot
      this.showModal = true
    },

    async deactivatePilot() {
      this.deactivateLoader = true

      // check if pilot has a running session
      new Promise((resolve, reject) => {
        this.$axios.get("http://localhost:5000/sessions/running").then(result => {
          var sessions = result.data["sessions"]

          for (var i = 0; i < sessions.length; i++) {
            if (sessions[i].pilot_id == this.toDeactivatePilot.pilot_id) {
              console.log(sessions[i])
              // pilot has active session
              this.deactivateMsg = "Pilot konnte nicht deaktiviert werden, da er zurzeit eine Flugsession hat!"
              reject()
            }
          }
          
          resolve()
        }, error => {
          console.error(error)
          this.deactivateMsg = "Pilot konnte nicht deaktiviert werden!"
          reject()
        });
      }).then(() => {
        // pilot has no running session and can be deactivated
        this.toDeactivatePilot.rfid = null

        this.$axios.put("http://localhost:5000/pilots?id=" + this.toDeactivatePilot.pilot_id, this.toDeactivatePilot).then(result => {
          this.items = result.data["pilots"]
          this.deactivateState = true
          this.getPilots()
        }, error => {
          console.error(error)
          this.deactivateMsg = "Pilot konnte nicht deaktiviert werden!"
          this.deactivateState = false
        });
      }, error => {
        // pilot has active session, or get request failed
        console.error(error)
        this.deactivateState = false
      });

      this.deactivateLoader = false
      this.showModal = false
    },

    toggleActivePilots() {
      if (this.isActive) {
        this.isActive = false
        this.toggleActivePilotsButton = "Zeige aktive Piloten"
      } else {
        this.isActive = true
        this.toggleActivePilotsButton = "Zeige inaktive Piloten"
      }

      this.getPilots()
    },

    async getPilots() {
      this.pilotsLoader = true

      await this.$axios.get("http://localhost:5000/pilots?is_active=" + this.isActive).then(result => {
        this.items = result.data["pilots"]
        console.log(this.items)
        this.pilotsLoader = false
      }, error => {
        console.error(error)
        this.pilotsLoader = false
        this.pilotsState = false
      });
    }
  },
  async mounted() {
    this.getPilots()
  }
}
</script>