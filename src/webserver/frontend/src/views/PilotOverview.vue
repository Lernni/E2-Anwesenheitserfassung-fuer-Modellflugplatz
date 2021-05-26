<template>
  <div class="pilot-overview">
    <h2>Pilotenübersicht</h2>

    <b-alert variant="success" :show="deactivateState" dismissible>
      Pilot wurde erfolgreich deaktiviert!
    </b-alert>

    <b-alert variant="danger" :show="deactivateState == false" dismissible>
      Pilot konnte nicht deaktiviert werden!
    </b-alert>

    <b-alert variant="danger" :show="pilotsState == false">
      Piloten konnten nicht geladen werden!
    </b-alert>

    <b-input-group prepend="Suche" class="mb-3">
      <b-form-input type="search" v-model="filterCriteria.pilot_name" placeholder="Name"></b-form-input>
    </b-input-group>

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
    <b-button variant="primary" @click="toggleActivePilots()">{{ toggleActivePilotsButton }}</b-button>
    <b-button variant="primary" class="ml-2" to="pilot/new">Pilot erstellen</b-button>
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
        {key: "pilot_name", label: "Name"},
        {
          key: "entry_date",
          label: "Eintrittsdatum",
          formatter: (value) => {
            return new Date(value).toLocaleDateString()
          }
        },
        {key: "rfid", label: "RFID"},
        {key: "actions", label: ""}
      ],
      toggleActivePilotsButton: "Deaktivierte Piloten",

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

      this.toDeactivatePilot.is_active = false
      this.toDeactivatePilot.rfid = null

      await axios.put("http://localhost:5000/pilots?id=" + this.toDeactivatePilot.pilot_id, this.toDeactivatePilot).then(result => {
        this.items = result.data["pilots"]
        this.deactivateLoader = false
        this.showModal = false
        this.deactivateState = true
        this.getPilots()
      }, error => {
        console.error(error)
        this.deactivateLoader = false
        this.showModal = false
        this.deactivateState = false
      });
    },
    toggleActivePilots() {
      if (this.filterCriteria.is_active) {
        this.filterCriteria.is_active = false
        this.toggle_active_pilots_button = "Aktive Piloten"
      } else {
        this.filterCriteria.is_active = true
        this.toggle_active_pilots_button = "Deaktivierte Piloten"
      }

      this.getPilots()
    },
    async getPilots() {
      this.pilotsLoader = true

      await axios.get("http://localhost:5000/pilots?is_active=" + this.filterCriteria.is_active).then(result => {
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
