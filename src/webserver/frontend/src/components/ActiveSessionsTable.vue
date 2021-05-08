<template>
  <div class="active-sessions-table">
    <b-table striped :items="items" :fields="fields"></b-table>
    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ActiveSessions',
  props: {
    msg: String
  },
  data() {
    return {
      items: [
        // test item
        {session_id: 1, pilot_name: "Max Mustermann", start_time: "12.05.2020", session_leader: true}
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
    };
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