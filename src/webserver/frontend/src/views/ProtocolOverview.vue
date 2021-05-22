<template>
  <div class="protocol-overview">
    <h2>Protokolldaten</h2>
    <b-container fluid class="mb-3">
      <b-row align-h="center">
        <b-col lg="6">
          <b-form-group label="Name" label-for="name-filter-input">
            <b-input-group prepend="Suche">
              <b-form-input id="name-filter-input" v-model="pilot_name" type="search"></b-form-input>
            </b-input-group>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row align-h="center">
        <b-col lg="3">
          <b-form-group label="Startdatum" label-for="start-date-filter">
              <b-form-datepicker
                id="start-date-filter"
                placeholder="Datum auswählen"
                v-model="startDate"
                locale="de-DE"
                :start-weekday="1"
                hide-header="true"
                labelHelp=""
                :max="endDate"
              >
              </b-form-datepicker>
          </b-form-group>
        </b-col>
        <b-col lg="3">
          <b-form-group label="Enddatum" label-for="end-date-filter">
              <b-form-datepicker
                id="end-date-filter"
                placeholder="Datum auswählen"
                v-model="endDate"
                locale="de-DE"
                :start-weekday="1"
                hide-header="true"
                labelHelp=""
                :min="startDate"
                :max="maxDate"
              >
              </b-form-datepicker>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row align-h="center">
        <b-col lg="6">
          <b-button variant="primary" @click="getSessions()" class="float-right">Suchen</b-button>
        </b-col>
      </b-row>
    </b-container>

    <b-table
      striped
      :items="items"
      :fields="fields"
      :total-rows="items.length"
      :per-page="perPage"
      :current-page="currentPage"
    >
      <template #cell(guest_details)="row">
        <b-button v-if="row.item.guest_name" variant="outline-dark" size="sm" @click="row.toggleDetails">{{row.item.guest_name}}</b-button>
      </template>

      <template #row-details="row">
        <b-card :sub-title="'Gast: ' + row.item.guest_name">
          {{row.item.guest_text}}
        </b-card>
      </template>

      <template #cell(actions)="row">
          <b-button :href="'/session/modify?id=' + row.item.session_id" size="sm" variant="outline-primary" v-b-tooltip.hover title="Bearbeiten">
            <b-icon-pencil-square></b-icon-pencil-square>
          </b-button>
      </template>
    </b-table>

    <b-pagination v-model="currentPage" :total-rows="items.length" :per-page="perPage"></b-pagination>

    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>

    <b-container>
      <b-row>
        <b-button variant="primary">Protokolldaten herunterladen</b-button>
      </b-row>
      <b-row class="mt-3">
        <b-button variant="primary" to="add-session">Flugsession nachtragen</b-button>
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
        {
          key: "date",
          label: "Datum",
          formatter: (value) => {
            return new Date(value).toLocaleDateString()
          }
        },
        {key: "start_time", label: "Beginn"},
        {key: "end_time", label: "Ende"},
        {
          key: "session_leader",
          label: "Flugleiter",
          formatter: (value) => {
            return value ? "F" : ""
          }
        },
        {key: "guest_details", label: "Gast"},
        {key: "actions", label: ""}
      ],

      startDate: new Date(),
      endDate: new Date(),
      maxDate: new Date(),

      perPage: 10,
      currentPage: 0,
    }
  },

  // TODO: Protokolldaten herunterladen
  // GET /sessions?csv
  // Rückgabe: CSV zum Download

  methods: {
    async getSessions() {
      var from = this.currentPage * this.perPage
      var to = from + this.perPage - 1

      await axios.get(
        "http://localhost:5000/sessions?name=" + this.pilot_name + "&start_date=" + this.startDate + "&end_date=" + this.endDate + "&from=" + from + "&to=" + to
      ).then(result => {
        this.items = result.data['sessions'];
      }, error => {
        console.error(error);
      });
    }
  },
  watch: {
    currentPage: function() {
      this.getSessions()
    }
  },
  async mounted() {
    this.getSessions()
  }
}
</script>