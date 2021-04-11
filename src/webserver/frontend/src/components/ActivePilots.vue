<template>
  <h1>Aktive Piloten</h1>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Beginn der Flugsession</th>
        <th>Flugleiter</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="pilot in pilots" :key="pilot.id">
        <td>{{pilot.name}}</td>
        <td>{{pilot.start_time}}</td>
        <td v-if="pilot.leader == 'True'">F</td>
      </tr>
    </tbody>
  </table>
  
</template>

<script>
import axios from 'axios'

export default {
  name: 'ActivePilots',
  props: {
    msg: String
  },
  data() {
    return {
      pilots: []
    };
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/active_pilots"}).then(result => {
      this.pilots = result.data['active_pilots'];
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
