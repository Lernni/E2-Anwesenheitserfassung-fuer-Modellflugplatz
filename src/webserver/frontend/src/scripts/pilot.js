/*
  *** pilot.js ***
  - Mixin für Verwaltung der gemeinsam genutzten Funktionen der Piloten-Formulare
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
*/

import { required, helpers, maxLength } from 'vuelidate/lib/validators'

const surnameRegex = helpers.regex("surnameRegex", /^([a-z]+ )*([A-Z][a-záàéèöäüß]+)([-]([A-Z][a-záàéèöäüß]+))*$/)
const nameRegex = helpers.regex("nameRegex", /^([A-Z][a-záàéèöäüß]+)([- ]([A-Z][a-záàéèöäüß]+))*$/)

export const formPilot = {
  data() {
    return {
      form: {
        pilotSurname: null,
        pilotName: null,
        pilotUsername: null,
        eID: null,
        rfid: null,
        isAdmin: false,
      },
      
      submit: {
        submitLoader: false,
        submitState: null,
        submitErrorMsg: null,
      },
      
      rfidList: {
        rfidListLoader: false,
        rfidListState: null,
        rfidList: [],
        noRfid: false,
      },

      pilot: {
        pilotLoader: false,
        pilotState: null,
      },

      username: {
        pilotUsernames: [],
        pilotUsernameLoader: false,
        pilotUsernameState: null,
      }
    }
  },
  validations: {
    form: {
      pilotSurname: {
        required,
        surnameRegex,
        maxLength: maxLength(50),
      },
      pilotName: {
        required,
        nameRegex,
        maxLength: maxLength(50)
      },
      // TODO: required setzen, wenn eID implementiert wurde
      eID: {
        // required
      },
      rfid: {
        required
      },
      // keine Anforderung an isAdmin, pilotUsername
      // muss aber trotzdem aufgeführt werden, da es in form enthalten ist und form an Pilot.vue weitergegeben wird
      isAdmin: {},
      pilotUsername: {},
    }
  },
  watch: {
    "rfidList.rfidList": function() {
      this.rfidList.noRfid = (this.rfidList.rfidList.length == 0)
    },
    "form.pilotName": function() {
      this.setUsername()
    },
    "form.pilotSurname": function() {
      this.setUsername()
    }
  },
  methods: {
    validateAll() {
      var states = {}

      for (const key in this.form) {
        states[key] = this.validateState(key)
      }

      return states
    },

    // Bestimmung des Nutzernamen anhand des Vor- und Nachnamen
    // Bsp: Max Muster -> max_muster
    setUsername() {
      var name = this.form.pilotName
      var surname = this.form.pilotSurname
      var username = ""

      if (name != null && surname != null) {
        name = name.toLowerCase().replace(" ", "_")
        surname = surname.toLowerCase().replace(" ", "_")
        
        username = name + "_" + surname
        if (this.username.pilotUsernames.includes(username)) {
          var index = 1
          do { index++ } while (this.username.pilotUsernames.includes(username + index));

          username += index
        }

        this.form.pilotUsername = username
      }
    },

    submitSuccess() {
      this.submit.submitLoader = false
      this.submit.submitState = true

      this.form.pilotSurname = null
      this.form.pilotName = null
      this.form.pilotUsername = null
      this.form.eID = null
      this.form.rfid = null
      this.form.isAdmin = false
    },

    submitFailure(error) {
      console.error(error);
      this.submit.submitLoader = false
      this.submit.submitState = false
      this.submit.submitErrorMsg = error
    },

    async getRfidList() {
      return new Promise((resolve, reject) => {
        this.rfidList.rfidListLoader = true

        this.$axios.get("/rfid_available")
          .then(response => {
            var rfidList = response.data['rfid_list']
            this.rfidList.rfidList = []
            for (var i = 0; i < rfidList.length; i++) {
              this.rfidList.rfidList.push(response.data['rfid_list'][i])
            }
  
            this.rfidList.rfidListLoader = false

            resolve()
          })
          .catch(error => {
            console.error(error);
            this.rfidList.rfidListLoader = false
            this.rfidList.rfidListState = false

            reject()
        });
      })
    },

    // Laden aller Nutzernamen zum Überprüfen auf Namensgleichheit
    async getPilotUsernames() {
      return new Promise((resolve, reject) => {
        this.username.pilotUsernameLoader = true
  
        this.$axios.get("/pilot-list")
          .then(response => {
            this.username.pilotUsernames = response.data['pilots'].map(
              (pilot) => (pilot.pilot_id == this.pilotId) ? null : pilot.pilot_username
            )
            this.username.pilotUsernameLoader = false

            resolve()
          })
          .catch(error => {
            console.error(error);
            this.username.pilotUsernameLoader = false
            this.username.pilotUsernameState = false

            reject()
        });
      })
    }
  }
}; 