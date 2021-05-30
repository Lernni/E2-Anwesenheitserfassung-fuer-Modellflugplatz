<template>
  <div class="protocol-overview">
    <h2>Protokolldaten</h2>
    <b-container fluid class="mb-3">
      <b-row align-h="center">
        <b-col lg="6">
          <b-form-group label="Name" label-for="name-filter-input">
            <b-form-input v-model="pilotName" id="name-filter-input" type="search"></b-form-input>
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
                :hide-header="true"
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
                :hide-header="true"
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
          <b-button-group class="float-right">
            <b-button :pressed="filteredSessions" variant="primary" @click="filteredSessions = true; getSessions()">
              <b-icon-filter :flip-v="filteredSessions"></b-icon-filter>
              Filtern
            </b-button>
            <b-button v-if="filteredSessions" variant="danger" v-b-tooltip.hover title="Filter aufheben" @click="filteredSessions = false; getSessions()">
              <b-icon-x scale="1.2"></b-icon-x>
            </b-button>
          </b-button-group>
        </b-col>
      </b-row>
    </b-container>

    <b-overlay :show="sessionLoader" spinner-type="grow">
      <b-table
        striped
        :items="items"
        :fields="fields"
        :current-page="currentPage"
      >
        <template #cell(guest_details)="row">
          <b-button v-if="row.item.guest.name" variant="outline-dark" size="sm" @click="row.toggleDetails">{{row.item.guest.name}}</b-button>
        </template>

        <template #row-details="row">
          <b-card :sub-title="'Gast: ' + row.item.guest.name">
            {{row.item.guest.text}}
          </b-card>
        </template>

        <template #cell(actions)="row">
            <b-button :href="'/session/edit?id=' + row.item.session_id" size="sm" variant="outline-primary" v-b-tooltip.hover title="Bearbeiten">
              <b-icon-pencil-square></b-icon-pencil-square>
            </b-button>
        </template>
      </b-table>
    </b-overlay>

    <b-pagination v-model="currentPage" :total-rows="sessionCount" :per-page="perPage"></b-pagination>

    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>

    <b-container>
      <b-row>
        <b-button variant="primary">Protokolldaten herunterladen</b-button>
      </b-row>
      <b-row class="mt-3">
        <b-button variant="primary" to="session/new">Flugsession nachtragen</b-button>
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
      items: [],
      fields: [
        {key: "session_id", label: "ID"},
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
      filteredSessions: false,
      pilotName: null,

      perPage: 10,
      currentPage: 1,
      sessionCount: 0,

      sessionLoader: false,
      sessionState: null,
    }
  },

  // TODO: Protokolldaten herunterladen
  // GET /sessions?csv
  // Rückgabe: CSV zum Download

  methods: {
    async getSessions() {
      this.sessionLoader = true

      var from = ((this.currentPage - 1) * this.perPage) + 1
      var to = from + this.perPage - 1

      var requestURL = "http://localhost:5000/sessions?from=" + from + "&to=" + to

      if (this.filteredSessions) {
        requestURL += "&start_date=" + new Date(this.startDate).toISOString().split('T')[0] + "&end_date=" + new Date(this.endDate).toISOString().split('T')[0]

        if (this.pilotName != null) {
          requestURL += "&name=" + this.pilotName
        }
      }

      await axios.get(requestURL
      ).then(result => {
        this.items = result.data['sessions']
        this.sessionCount = result.data['session_count']

        this.sessionLoader = false
      }, error => {
        console.error(error);

        this.sessionLoader = false
        this.sessionState = false
      });
    },
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