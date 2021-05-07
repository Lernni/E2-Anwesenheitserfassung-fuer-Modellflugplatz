<template>
  <table class="table table-striped">
    <thead>
      <tr>
        <th scope="col">Pilot</th>
        <th scope="col">Beginn</th>
        <th scope="col">Flugleiter</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="session in sessions" :key="session.session_id">
        <td>{{session.pilot_name}}</td>
        <td>{{session.start_time}}</td>
        <td v-if="session.leader == 'True'">F</td>
      </tr>
    </tbody>
  </table>
  <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>
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
      sessions: []
    };
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
