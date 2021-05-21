<template>
  <div class="admin-panel">
    <h2>Aktive Flugsessions</h2>
    <b-table striped :items="items" :fields="fields"></b-table>

    <b-alert :show="noSessions" variant="info">
      Zurzeit keine Piloten auf dem Flugplatz
    </b-alert>

    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>
    <hr>
    <h2>Admin-Bereich</h2>
    <b-container>
      <b-row cols="2" class="text-center">
        <b-col class="py-3">Protokoll ansehen</b-col>
        <b-col>
          <b-button variant="primary" to="protocol-overview">Zum Protokoll</b-button>
        </b-col>
        <b-col class="py-3">Flüge nachtragen</b-col>
        <b-col>
          <b-button variant="primary" to="add-session">Formular</b-button>
        </b-col>
        <b-col class="py-3">Mitgliederverwaltung</b-col>
        <b-col>
          <b-button variant="primary" to="pilot-overview">Zur Übersicht</b-button>
        </b-col>
        <b-col class="py-3">Alle Piloten abmelden</b-col>
        <b-col>
          <b-button variant="primary">Piloten abmelden</b-button>
        </b-col>
        <b-col class="py-3">Systemeinstellungen</b-col>
        <b-col>
          <b-button variant="primary">Einstellungen</b-button>
        </b-col>
      </b-row>
    </b-container>
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
      fields: [
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

      noSessions: true
    }
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/sessions?running"}).then(result => {
      this.items = result.data['sessions'];
      this.noSessions = (this.items.length == 0)

    }, error => {
      console.error(error);
    });
  }
}
</script>