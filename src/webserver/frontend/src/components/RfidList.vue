<template>
  <b-form-group label="RFID-Kennung" label-for="rfid-select">
    <b-overlay :show="rfidListLoader" spinner-type="grow" spinner-small>
      <b-form-select required id="rfid-select" v-model="rfid" :state="rfidListState" :options="rfidList"></b-form-select>
      <b-form-invalid-feedback id="input-live-feedback">
        Keine Verbindung zur Datenbank
      </b-form-invalid-feedback>
    </b-overlay>
  </b-form-group>
</template>

<script>
import axios from 'axios'

export default {
  name: "RfidList",
  data() {
    return {
      rfidListLoader: false,
      rfidListState: null,
      rfid: null,
      rfidList: [
        // test objects
        {value: 7, text: "0x65A7F"},
        {value: 12, text: "0xAA340"},
        {value: 8, text: "0xDCA11"},
      ]
    }
  },
  watch: {
    rfid: function() {
      this.$emit('selectedRfid', this.rfid)
    }
  },
  async mounted() {
    this.rfidListLoader = true

    await axios.get("http://localhost:5000/rfid")
      .then(response => {
        this.rfidList = response.data['rfid_list']
        this.rfidListLoader = false
      })
      .catch(error => {
        console.error(error);
        this.rfidListLoader = false
        this.rfidListState = false
    });
  }
}
</script>

<style>

</style>