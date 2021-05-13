<template>
  <div class="admin-panel">
    <h2>Aktive Flugsessions</h2>
    <b-table striped :items="items" :fields="fields"></b-table>
    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>
    <hr>
    <h2>Admin-Bereich</h2>
    <AdminPanel/>
  </div>
</template>

<script>
import axios from 'axios'
import AdminPanel from '@/components/AdminPanel.vue'

export default {
  name: 'Home',
  components: {
    AdminPanel
  },
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
