<template>
  <div class="protocol-overview">
    <h2>Protokolldaten</h2>
    <b-container fluid class="mb-3">
      <b-row align-h="center">
        <b-col lg="6">
          <b-form-group label="Name" label-for="name-filter-input">
            <b-form-input id="name-filter-input" v-model="filterCriteria.pilot_name" type="search"></b-form-input>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row align-h="center">
        <b-col lg="3">
          <b-form-group label="Startdatum" label-for="start-date-filter">
              <b-form-datepicker id="start-date-filter" v-model="filterCriteria.start_date" locale="de-DE" :start-weekday="1"></b-form-datepicker>
          </b-form-group>
        </b-col>
        <b-col lg="3">
          <b-form-group label="Enddatum" label-for="end-date-filter">
              <b-form-datepicker id="end-date-filter" v-model="filterCriteria.end_date" locale="de-DE" :start-weekday="1"></b-form-datepicker>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>

    <b-table striped :items="items" :fields="fields" :filter="filterCriteria" :filter-function="filterTable">
      <template #cell(guest_details)="row">
        <b-button v-if="row.item.guest_name" variant="outline-dark" size="sm" @click="row.toggleDetails">{{row.item.guest_name}}</b-button>
      </template>

      <template #row-details="row">
        <b-card :sub-title="'Gast: ' + row.item.guest_name">
          {{row.item.guest_text}}
        </b-card>
      </template>
    </b-table>
    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>
    <b-container>
      <b-row>
        <b-button variant="primary">Protokolldaten herunterladen</b-button>
      </b-row>
      <b-row class="mt-3">
        <b-button variant="primary">Flugzeiten nachtragen</b-button>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "ProtocolOverview",
  data() {
    return {
      items: [
        // test object
        {
          session_id: 1,
          pilot_name: "Maria Mustermann",
          date: "2021-05-31",
          start_time: "14:23",
          end_time: "15:33",
          session_leader: true,
          guest_name: "Max Mustermann",
          guest_text: "Versicherungsnummer: 48572493793284"
        },
        {
          session_id: 2,
          pilot_name: "Mario Müller",
          date: "2021-05-12",
          start_time: "12:07",
          end_time: "14:54",
          session_leader: false
        },
      ],
      fields: [
        {key: "pilot_name", label: "Pilot"},
        {key: "date", label: "Datum"},
        {key: "start_time", label: "Beginn"},
        {key: "end_time", label: "Ende"},
        {
          key: "session_leader",
          label: "Flugleiter",
          formatter: (value) => {
            return value ? "F" : ""
          }
        },
        {key: "guest_details", label: "Gast"}
      ],
      filterCriteria: {
        pilot_name: null,
        start_date: null,
        end_date: null
      }
    }
  },
  methods: {
    filterTable(row, filter) {
      if (filter.pilot_name != null) {
        if (!row.pilot_name.includes(filter.pilot_name)) return false
      }

      if (filter.start_date != null && filter.end_date != null) {
        var start_date = new Date(filter.start_date)
        var end_date = new Date(filter.end_date)
        var row_date = new Date(row.date)

        if (!(row_date >= start_date && row_date <= end_date)) return false
      }
      
      return true
    }
  },
  async mounted() {
    await axios({method: "GET", "url": "http://localhost:5000/sessions?all"}).then(result => {
      this.items = result.data['sessions'];
    }, error => {
      console.error(error);
    });
  }
}
</script>

<style>

</style>