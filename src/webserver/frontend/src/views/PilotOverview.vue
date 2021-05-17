<template>
  <div class="pilot-overview">
    <h2>Pilotenübersicht</h2>

    <b-input-group class="mb-3">
      <b-form-input placeholder="Pilot"></b-form-input>
      <b-input-group-append>
        <b-button variant="primary">Suchen</b-button>
      </b-input-group-append>
    </b-input-group>

    <b-table striped :items="items" :fields="fields" :filter="filter" :filter-included-fields="filterOn">
      <template #cell(actions)="row">
        <b-button v-if="!row.item.active" size="sm" variant="outline-success" v-b-tooltip.hover title="Reaktivieren">
          <b-icon-plus-circle-fill></b-icon-plus-circle-fill>
        </b-button>
        <b-button-group v-else size="sm">
          <b-button variant="outline-primary" :href="'/pilot/modify?id=' + row.item.pilot_id" v-b-tooltip.hover title="Bearbeiten">
            <b-icon-pencil-square></b-icon-pencil-square>
          </b-button>
          <b-button variant="outline-danger" v-on:click="delete_pilot(row.item.pilot_id)" v-b-tooltip.hover title="Deaktivieren">
            <b-icon-dash-circle-fill></b-icon-dash-circle-fill>
          </b-button>
        </b-button-group>
      </template>
    </b-table>
    <b-button variant="primary" v-on:click="toggle_active_pilots()">{{ toggle_active_pilots_button }}</b-button>
  </div>
</template>

<script>
import axios from 'axios'
import { BIconPencilSquare, BIconDashCircleFill, BIconPlusCircleFill } from 'bootstrap-vue'

export default {
  name: 'PilotOverview',
  components: {
    BIconPencilSquare,
    BIconDashCircleFill,
    BIconPlusCircleFill
  },
  data() {
    return {
      items: [
        // test item
        // TODO: rfid format prüfen
        // TODO: filter event -> asynchrones GET Request
        { pilot_id: 1, pilot_name: "Testpilot", entry_date: "2021-03-21", rfid: 123, active: true},
        { pilot_id: 2, pilot_name: "Deaktivierter Testpilot", entry_date: "21.03.2008", rfid: 125, active: false}
      ],
      fields: [
        {key: "pilot_name", label: "Name"},
        {key: "entry_date", label: "Eintrittsdatum"},
        {key: "rfid", label: "RFID"},
        {key: "actions", label: ""}
      ],
      filter: "true",
      filterOn: ["active"],
      toggle_active_pilots_button: "Deaktivierte Piloten"
    };
  },
  methods: {
    delete_pilot: function(pilot_id) {
      alert("Soll " + this.items.find(x => x.pilot_id === pilot_id).pilot_name + " wirklich deaktiviert werden? Die Zuordnung zum RFID-Ausweis wird entfernt.")
      // TODO: PUT /pilots?id=2?active=false
      // Rückgabe: Änderung erfolgreich -> Seite neu laden
    },
    // TODO: Methode: reaktivieren eines Piloten
    // TODO: PUT /pilots?id=2?active=true
    // Rückgabe: Änderung erfolgreich -> Seite neu laden
    toggle_active_pilots: function() {
      // TODO: toggle GET Request ?active=false
      if (this.filter == "true") {
        this.filter = "false"
        this.toggle_active_pilots_button = "Aktive Piloten"
      } else {
        this.filter = "true"
        this.toggle_active_pilots_button = "Deaktivierte Piloten"
      }
    }
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/pilots?active=true"}).then(result => {
      this.items = result.data['pilots'];
    }, error => {
      console.error(error);
    });
  }
}
</script>
