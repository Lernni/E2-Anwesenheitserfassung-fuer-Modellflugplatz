<template>
  <div class="sessions">
    <h2>Protokolldaten</h2>

    <b-alert variant="danger" :show="sessionState == false">
      Protokolldaten konnten nicht geladen werden
    </b-alert>

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

    <b-pagination class="d-md-none" v-model="currentPage" :total-rows="sessionCount" :per-page="perPage"></b-pagination>

    <b-overlay :show="sessionLoader" spinner-type="grow">
      <b-table
        class="d-none d-md-table"
        stacked="sm"
        striped
        :items="items"
        :fields="fieldsDesktop"
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
          <b-button v-if="canEdit(row.item.pilot_id)" :href="'/sessions/edit?id=' + row.item.session_id" size="sm" variant="outline-primary" v-b-tooltip.hover title="Bearbeiten">
            <b-icon-pencil-square></b-icon-pencil-square>
          </b-button>
        </template>
      </b-table>

      <b-table stacked class="d-md-none" striped :items="items" :fields="fieldsMobile">
        <template #cell(session_time)="row">
          {{ row.item.start_time }} - {{ row.item.end_time == null ? "offen" : row.item.end_time }}
        </template>

        <template #cell(guest)="row">
          {{ row.item.guest.name != null ? row.item.guest.name : "Kein Gast"}}<br/>
          {{ row.item.guest.name != null ? row.item.guest.text : ""}}
        </template>

        <template #cell(actions)="row">
          <b-button v-if="canEdit(row.item.pilot_id)" :href="'/sessions/edit?id=' + row.item.session_id" size="sm" variant="outline-primary" v-b-tooltip.hover title="Bearbeiten">
            <b-icon-pencil-square></b-icon-pencil-square>
            <span class="d-block d-sm-none">Bearbeiten</span>
          </b-button>
        </template>
      </b-table>
    </b-overlay>

    <b-pagination v-model="currentPage" :total-rows="sessionCount" :per-page="perPage"></b-pagination>

    <p class="font-italic last-ping-info">Letzte Aktualisierung: --:--</p>

    <b-container>
        <b-row class="footer-buttons">
          <b-button variant="primary">Protokolldaten herunterladen</b-button>
        </b-row>
        <b-row class="mt-3 footer-buttons">
          <b-button variant="primary" to="sessions/new">Flugsession nachtragen</b-button>
        </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "Sessions",
  data() {
    return {
      items: [],
      fieldsDesktop: [
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
      fieldsMobile: [
        {key: "pilot_name", label: "Pilot"},
        {
          key: "date",
          label: "Datum",
          formatter: (value) => {
            return new Date(value).toLocaleDateString()
          }
        },
        {key: "session_time", label: "Zeitraum"},
        {
          key: "session_leader",
          label: "Flugleiter",
          formatter: (value) => {
            return value ? "Ja" : "Nein"
          }
        },
        {key: "guest", label: "Gast"},
        {key: "actions", label: "", class: "text-center"}
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

      userInfo: null
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

      await this.$axios.get(requestURL)
      .then(result => {
        this.items = result.data['sessions']
        this.sessionCount = result.data['session_count']

        this.sessionLoader = false
      }, error => {
        console.error(error);

        this.sessionLoader = false
        this.sessionState = false
      });
    },
    canEdit(pilotId) {
      if (this.userInfo.is_admin) return true
      return (this.userInfo.id == pilotId)
    }
  },
  watch: {
    currentPage: function() {
      this.getSessions()
    }
  },
  async mounted() {
    this.userInfo = JSON.parse(this.$store.getters.userInfo)
    this.getSessions()
  }
}
</script>