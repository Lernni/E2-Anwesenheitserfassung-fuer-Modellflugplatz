<template>
  <b-table striped :items="items" :fields="fields">
    <template #cell(actions)="row">
        <b-button-group size="sm">
          <b-button variant="outline-primary" :href="'/edit-pilot?id=' + row.item.pilot_id">edit</b-button>
          <b-button variant="outline-danger" v-on:click="delete_pilot(row.item.pilot_id)">deactivate</b-button>
        </b-button-group>
    </template>
  </b-table>
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
      items: [
        // test item
        { pilot_id: 1, pilot_name: "Testpilot", entry_date: "21.03.2021", rfid: 123}
      ],
      fields: [
        {key: "pilot_name", label: "Name"},
        {key: "entry_date", label: "Eintrittsdatum"},
        {key: "rfid", label: "RFID"},
        {key: "actions", label: ""}
      ]
    };
  },
  methods: {
    delete_pilot: function(pilot_id) {
      alert("Soll " + this.items.find(x => x.pilot_id === pilot_id).pilot_name + " wirklich deaktiviert werden? Die Zuordnung zum RFID-Ausweis wird entfernt.")
      // POST pilot deactivate
    }
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/pilots"}).then(result => {
      this.items = result.data['pilots'];
    }, error => {
      console.error(error);
    });
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
/*.pilot-options .unicon svg {
  fill: currentColor;
}*/
</style>
