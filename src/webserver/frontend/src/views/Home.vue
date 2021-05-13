<template>
  <div class="admin-panel">
    <h2>Aktive Flugsessions</h2>
    <b-table striped :items="items" :fields="fields"></b-table>
    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>
    <hr>
    <h2>Admin-Bereich</h2>
    <b-container>
      <b-row cols="2" class="text-center">
        <b-col class="py-3">Protokoll ansehen</b-col>
        <b-col>
          <b-button variant="primary">Zum Protokoll</b-button>
        </b-col>
        <b-col class="py-3">Flüge nachtragen</b-col>
        <b-col>
          <b-button variant="primary">Formular</b-button>
        </b-col>
        <b-col class="py-3">Mitgliederverwaltung</b-col>
        <b-col>
          <b-button variant="primary">Zur Übersicht</b-button>
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
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      items: [
        // test object
        {session_id: 1, pilot_name: "Maria Mustermann", start_time: "12:07", session_leader: true}
      ],
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
      ]
    }
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/sessions?running=true"}).then(result => {
      this.items = result.data['sessions'];
    }, error => {
      console.error(error);
    });
  }
}
</script>
