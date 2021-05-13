<template>
  <div class="admin-panel">
    <h2>Aktive Flugsessions</h2>
    <SessionsTable/>
    <hr>
    <h2>Admin-Bereich</h2>
    <AdminPanel/>
  </div>
</template>

<script>
import axios from 'axios'
import SessionsTable from '@/components/SessionsTable.vue'
import AdminPanel from '@/components/AdminPanel.vue'

export default {
  name: 'Home',
  components: {
    SessionsTable,
    AdminPanel
  },
  data() {
    return {
      sessions: [
        // test object
        {session_id: 1, pilot_name: "Maria Mustermann", start_time: "12.05.2020", session_leader: true}
      ]
    }
  },
  provide() {
    // TODO: Test reactivity to dynamic changes
    return {
      items: this.sessions
    }
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/sessions?running=true"}).then(result => {
      this.sessions = result.data['sessions'];
    }, error => {
      console.error(error);
    });
  }
}
</script>
