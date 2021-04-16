<template>
  <h1>Alle Piloten</h1>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>RFID-Code</th>
        <th>Name</th>
        <th>Einstrittsdatum</th>
        <th>Aktiv</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="pilot in pilots" :key="pilot.pilot_id">
        <td>{{pilot.pilot_id}}</td>
        <td>{{pilot.rfid_code}}</td>
        <td>{{pilot.name}}</td>
        <td>{{pilot.eintrittsdatum}}</td>
        <td>{{pilot.aktiv}}</td>
      </tr>
    </tbody>
  </table>
  
</template>

<script>
import axios from 'axios'

export default {
  name: 'AllPilots',
  props: {
    msg: String
  },
  data() {
    return {
      pilots: []
    };
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/pilots"}).then(result => {
      this.pilots = result.data['pilots'];
    }, error => {
      console.error(error);
    });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
table {
  margin: auto;
}
th, td {
  padding: 5px;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
