<template>
  <div class="add-session">
    <h2>Flugsession nachtragen</h2>

    <b-alert variant="danger" :show="pilotListState == false">
      Keine Verbindung zur Datenbank!
    </b-alert>

    <b-alert variant="danger" :show="submitState == false" dismissable>
      Flugsession konnte nicht nachgetragen werden!
    </b-alert>

    <b-alert variant="success" :show="submitState" dismissable>
      Flugsession wurde erfolgreich nachgetragen!
    </b-alert>

    <b-form @submit="onSubmit" @reset="onReset" :novalidate="true">
      <b-row>
        <b-col cols="8">
          <b-form-group id="pilot-name-group" label="Pilot" label-for="pilot-name-input">
            <b-overlay :show="pilotListLoader" spinner-type="grow" spinner-small>
              <b-form-input id="pilot-name-input" class="mb-3" placeholder="Name" v-model="pilotSearch" type="search" autocomplete="off"></b-form-input>
              <b-form-select v-model.trim="$v.form.pilot.$model" :options="filteredPilotList" :select-size="5" :state="validateState('pilot')"></b-form-select>
              <b-form-invalid-feedback :state="validateState('pilot')">
                Kein Pilot ausgewählt
              </b-form-invalid-feedback>
            </b-overlay>
          </b-form-group>

          <b-row>
            <b-col>
              <b-form-group id="session-start-group" label="Startzeit" label-for="session-start-time-input">
                <b-form-input id="session-start-time-input" v-model.trim="$v.form.startTime.$model" :state="validateState('endTime') && validateState('startTime')" type="time"></b-form-input>
                <b-form-invalid-feedback>
                  Ungültige Zeitangabe
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group id="session-end-group" label="Endzeit" label-for="session-end-time-input">
                <b-form-input id="session-end-time-input" v-model.trim="$v.form.endTime.$model" :state="validateState('endTime') && validateState('startTime')" type="time"></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-form-group id="session-leader-group">
            <b-form-checkbox id="session-leader-checkbox" name="session-leader-checkbox" v-model="form.sessionLeader">Flugleiter</b-form-checkbox>
          </b-form-group>
          <b-form-group id="guest-check-group">
            <b-form-checkbox id="guest-checkbox" name="guest-checkbox" v-model="form.guest">mit Gast</b-form-checkbox>
          </b-form-group>
          <b-container v-show="form.guest">
            <b-form-group id="guest-name-group" label="Gastname" label-for="guest-input">
              <b-form-input id="guest-input" v-model.trim="$v.form.guestName.$model" :state="validateState('guestName')"></b-form-input>
              <b-form-invalid-feedback>
                Ungültiger Gastname
              </b-form-invalid-feedback>
            </b-form-group>
            <b-form-group id="guest-info-group" label="Gastinformationen" label-for="guest-textarea">
              <b-form-textarea id="guest-textarea" v-model="form.guestText" rows="3"></b-form-textarea>
            </b-form-group>
          </b-container>
        </b-col>
        <b-col>
          <b-form-group id="session_date" label="Datum" label-for="sessionDatePicker">
            <b-calendar
              id="sessionDatePicker"
              v-model.trim="$v.form.date.$model"
              locale="de-DE"
              :start-weekday="1"
              labelHelp=""
              labelNoDateSelected="Kein Datum ausgewählt"
              :max="maxDate"
              :class="validateState('date') == false ? 'form_error' : ''"
            >
            </b-calendar>
            <b-form-invalid-feedback :state="validateState('date')">
              Kein Datum ausgewählt
            </b-form-invalid-feedback>
          </b-form-group>
        </b-col>
      </b-row>
      <b-button type="submit" variant="primary" :disabled="submitLoader">
        <b-spinner v-show="submitLoader" small></b-spinner>
        Speichern
      </b-button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'
import { required, helpers } from 'vuelidate/lib/validators'
import { formValidation } from '@/scripts/formValidation'

const guestNameRegex = helpers.regex("guestNameRegex", /^([A-Z][a-zöäüß]+)([- ]([A-Z][a-zöäüß]+) )*([a-z]+ )*([A-Z][a-zöäüß]+)([-]([A-Z][a-zöäüß]+))*$/) 

export default {
  name: "NewSession",
  mixins: [formValidation],
  data() {
    return {
      form: {
        startTime: "",
        endTime: "",
        date: null,
        sessionLeader: false,
        guest: false,
        guestName: null,
        guestText: null,
        pilot: null,
      },

      maxDate: new Date(),

      submitLoader: false,
      submitState: null,
      pilotListLoader: false,
      pilotListState: null,
      pilotSearch: null,
      pilotList: [],
      filteredPilotList: []
    }
  },
  validations() {
    var form = {
      pilot: {required},
      date: {required},
      startTime: {required},
      endTime: {
        required,
        minValue: time => {
          var splitEndTime = time.split(":")
          var splitStartTime = this.form.startTime.split(":")

          return new Date().setHours(splitEndTime[0], splitEndTime[1]) > new Date().setHours(splitStartTime[0], splitStartTime[1])
        }
      },
      guestName: {}
    }

    if (this.form.guest) {
      form.guestName = {
        required,
        guestNameRegex
      }
    }

    return {
      form
    }
  },
  methods: {
    onSubmit(event) {
      if (this.validateSubmit()) {this.postNewSession() }
    },

    async postNewSession() {
      this.submitLoader = true

      var session = {
        pilot_id: this.form.pilot,
        session_date: this.form.date,
        start_time: this.form.startTime,
        end_time: this.form.endTime,
        is_leader: this.form.sessionLeader
      }

      if (this.form.guest) {
        session['guest_name'] = this.form.guestName
        session['guest_info'] = this.form.guestText
      }

      console.log(session)

      await axios.post("http://localhost:5000/sessions", session)
        .then(() => {
          this.submitLoader = false
          this.submitState = true
        })
        .catch(error => {
          console.error(error);
          this.submitLoader = false
          this.submitState = false
      });
    }
  },
  watch: {
    pilotSearch: function() {
      this.filteredPilotList = []

      Object.values(this.pilotList).forEach(pilot => {
        if (pilot.text.includes(this.pilotSearch)) {
          this.filteredPilotList.push(pilot)
        }
      })

    }
  },
  async mounted() {
    this.pilotListLoader = true

    await axios.get("http://localhost:5000/pilot-list")
      .then(response => {
        var pilotList = response.data['pilots'].map((pilot) => ({
          value: pilot.pilot_id,
          text: "[" + pilot.pilot_id + "] " + pilot.pilot_name 
        }))

        this.pilotList = pilotList
        this.filteredPilotList = pilotList
        this.pilotListLoader = false
      })
      .catch(error => {
        console.error(error);
        this.pilotListLoader = false
        this.pilotListState = false
    });
  }
}
</script>

<style scoped>
.form_error {
  border: 1px #dc3545 solid !important;
  border-radius: 5px;
}
</style>