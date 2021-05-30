<template>
  <div class="pilot-overview">
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
      <b-col>
        <b-input-group prepend="Suche">
          <b-form-input type="search" v-model="filterCriteria.pilot_name" placeholder="Name"></b-form-input>
        </b-input-group>
      </b-col>
      <b-col cols="12" md="auto">
        <b-button variant="primary" class="ml-2" @click="toggleActivePilots()">{{ toggleActivePilotsButton }}</b-button>
        <b-button variant="success" class="ml-2" to="pilot/new">
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
      <b-table striped :items="items" :fields="fields" :filter="filterCriteria" :filter-function="filterTable">
        <template #cell(pilot_name)="row">
          {{ row.item.pilot_name }} {{ row.item.pilot_surname }}
        </template>

        <template #cell(actions)="row">
          <b-button v-if="!row.item.is_active" :href="'/pilot/reactivate?id=' + row.item.pilot_id" size="sm" variant="outline-success" v-b-tooltip.hover title="Reaktivieren">
            <b-icon-plus-circle-fill></b-icon-plus-circle-fill>
          </b-button>
          <b-button-group v-else size="sm">
            <b-button variant="outline-primary" :href="'/pilot/edit?id=' + row.item.pilot_id" v-b-tooltip.hover title="Bearbeiten">
              <b-icon-pencil-square></b-icon-pencil-square>
            </b-button>
            <b-button variant="outline-danger" @click="showDeactivateModal(row.item)" v-b-tooltip.hover title="Deaktivieren">
              <b-icon-dash-circle-fill></b-icon-dash-circle-fill>
            </b-button>
          </b-button-group>
        </template>
      </b-table>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PilotOverview',
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
        {key: "actions", label: ""}
      ],
      toggleActivePilotsButton: "Zeige deaktive Piloten",

      filterCriteria: {
        pilot_name: null,
        is_active: true
      },
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
      filterTable(row, filter) {
        if (filter.pilot_name != null) {
          if (!row.pilot_name.includes(filter.pilot_name)) return false
        }

        return (row.is_active == filter.is_active)
    },

    showDeactivateModal(pilot) {
      this.toDeactivatePilot = pilot
      this.showModal = true
    },

    async deactivatePilot() {
      this.deactivateLoader = true

      // check if pilot has a running session
      new Promise((resolve, reject) => {
        axios.get("http://localhost:5000/sessions/running").then(result => {
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
        this.toDeactivatePilot.is_active = false
        this.toDeactivatePilot.rfid = null

        axios.put("http://localhost:5000/pilots?id=" + this.toDeactivatePilot.pilot_id, this.toDeactivatePilot).then(result => {
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
      if (this.filterCriteria.is_active) {
        this.filterCriteria.is_active = false
        this.toggleActivePilotsButton = "Zeige aktive Piloten"
      } else {
        this.filterCriteria.is_active = true
        this.toggleActivePilotsButton = "Zeige deaktive Piloten"
      }

      this.getPilots()
    },

    async getPilots() {
      this.pilotsLoader = true

      await axios.get("http://localhost:5000/pilots?is_active=" + this.filterCriteria.is_active).then(result => {
        this.items = result.data["pilots"]
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
