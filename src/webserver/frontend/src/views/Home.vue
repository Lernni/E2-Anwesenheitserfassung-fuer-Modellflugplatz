<template>
  <div class="admin-panel">
    <h2>Aktive Flugsessions</h2>
    <b-table class="d-none d-sm-table" striped :items="items" :fields="fieldsDesktop"></b-table>
    <b-table class="d-sm-none" striped :items="items" :fields="fieldsMobile">
      <template #cell(session_leader)="row">
        <b>{{ row.item.session_leader ? "F" : "" }}</b>
      </template>
    </b-table>

    <b-alert :show="noSessions" variant="info">
      Zurzeit keine Piloten auf dem Flugplatz
    </b-alert>

    <p class="font-italic last-ping-info">Letzte Aktualisierung: --:--</p>
    <hr>
    <h2>Quicklinks</h2>
    <div class="d-none d-sm-block">
      <b-row cols="2" class="align-items-center text-center">
        <b-col class="py-2">
          <b-button variant="primary" to="pilots/new">Pilot erstellen</b-button>
        </b-col>
        <b-col class="py-2">
          <b-button variant="primary" to="protocol">Protokoll ansehen</b-button>
        </b-col>
        <b-col class="py-2">
          <b-button variant="primary" to="rfid">RFID-Tag hinzufügen</b-button>          
        </b-col>
        <b-col class="py-2">
          <b-button variant="primary" to="session/new">Flüge nachtragen</b-button>
        </b-col>
        <b-col class="py-2">
          <b-button variant="primary" to="pilots">Pilotenübersicht</b-button>
        </b-col>
        <b-col class="py-2">
          <b-button variant="primary">Alle Piloten abmelden</b-button>
        </b-col>
        <b-col class="py-2">
          <b-button variant="primary">Einstellungen</b-button>
        </b-col>
      </b-row>
    </div>
    <b-list-group class="text-center d-sm-none">
      <b-list-group-item to="protocol">Protokoll ansehen</b-list-group-item>
      <b-list-group-item to="session/new">Flüge nachtragen</b-list-group-item>
      <b-list-group-item to="pilots">Pilotenübersicht</b-list-group-item>
      <b-list-group-item to="pilots/new">Pilot erstellen</b-list-group-item>
      <b-list-group-item to="rfid">RFID-Tag hinzufügen</b-list-group-item>
      <b-list-group-item to="settings">Einstellungen</b-list-group-item>
      <b-list-group-item variant="danger">Alle Piloten abmelden</b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
// TODO: letzte Aktualisierung bekommen -> Einstellungen?
// TODO: conditional rendering des Admin-Panels
// TODO: POST /sessions?checkout-all
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      items: [],
      fieldsDesktop: [
        {key: "pilot_id", label: "ID"},
        {key: "pilot_name", label: "Pilot"},
        {key: "start_time", label: "Beginn"},
        {
          key: "session_leader",
          label: "Flugleiter",
          formatter: (value) => {
            return value ? "F" : ""
          }
        }
      ],
      fieldsMobile: [
        {key: "pilot_name", label: "Pilot"},
        {
          key: "start_time",
          label: "Beginn",
          formatter: (value) => {
            var time = value.split(":")
            return time[0] + ":" + time[1]
          }
        },
        {
          key: "session_leader",
          label: "",
          formatter: (value) => {
            return value ? "F" : ""
          }
        }
      ],

      noSessions: true
    }
  },
  async mounted() {
    await axios.get("http://localhost:5000/sessions/running").then(result => {
      this.items = result.data['sessions'];
      this.noSessions = (this.items.length == 0)

    }, error => {
      console.error(error);
    });
  }
}
</script>