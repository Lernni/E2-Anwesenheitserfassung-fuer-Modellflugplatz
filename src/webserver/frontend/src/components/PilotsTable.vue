<template>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Name</th>
        <th>Aktiv</th>
        <th>RFID</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="pilot in pilots" :key="pilot.pilot_id">
        <td>{{pilot.pilot_name}}</td>
        <td>{{pilot.entry_date}}</td>
        <td>{{pilot.rfid}}</td>
        <td>
          <div class="btn-group pilot-options" role="group">
            <a type="button" :href="'/edit-pilot?id=' + pilot.pilot_id" class="btn btn-outline-primary">
              <unicon name="edit-alt"></unicon>
            </a>
            <a type="button" v-on:click="delete_pilot(pilot)" class="btn btn-outline-danger">
              <unicon name="minus-circle"></unicon>
            </a>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PilotsTable',
  props: {
    msg: String
  },
  data() {
    return {
      pilots: [
        { pilot_id: 1, pilot_name: "Testpilot", entry_date: "21.03.2021", rfid: 123}
      ]
    };
  },
  methods: {
    delete_pilot: function(pilot) {
      alert("Soll " + pilot.pilot_name + " wirklich deaktiviert werden? Die Zuordnung zum RFID-Ausweis wird entfernt.")
      // POST pilot deactivate
    }
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
<style>
.pilot-options .unicon svg {
  fill: currentColor;
}
</style>
