import axios from 'axios'
import { required, helpers } from 'vuelidate/lib/validators'

const surnameRegex = helpers.regex("surnameRegex", /^([a-z]+ )*([A-Z][a-zöäüß]+)([-]([A-Z][a-zöäüß]+))*$/)
const nameRegex = helpers.regex("nameRegex", /^([A-Z][a-zöäüß]+)([- ]([A-Z][a-zöäüß]+))*$/)
const usernameRegex = helpers.regex("usernameRegex", /^[a-z][a-z0-9_-]{2,15}$/)

export const formPilot = {
  data() {
    return {
      form: {
        pilotSurname: null,
        pilotName: null,
        pilotUsername: null,
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
        rfidList: []
      },

      pilot: {
        pilotLoader: false,
        pilotState: null,
      }
    }
  },
  validations: {
    form: {
      pilotSurname: {
        required,
        surnameRegex
      },
      pilotName: {
        required,
        nameRegex
      },
      pilotUsername: {
        required,
        usernameRegex
      },
      rfid: {
        required
      },
      isAdmin: {}
    }
  },
  methods: {
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name];
      return $dirty ? !$error : null;
    },

    validateAll() {
      var states = {}
      console.log(this.form)

      for (const key in this.form) {
        states[key] = this.validateState(key)
      }


      return states
    },

    onSubmit(event) {
      event.preventDefault()
      this.$v.form.$touch()
      if (!this.$v.form.$anyError) {
        this.pilotRequest()
      }
    },

    submitSuccess() {
      this.submit.submitLoader = false
      this.submit.submitState = true

      this.form.pilotSurname = null
      this.form.pilotName = null
      this.form.pilotUsername = null
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
      this.rfidList.rfidListLoader = true

      await axios.get("http://localhost:5000/rfid")
        .then(response => {
          var rfidList = response.data['rfid_list']
          this.rfidList.rfidList = []
          for (var i = 0; i < rfidList.length; i++) {
            this.rfidList.rfidList.push(response.data['rfid_list'][i])
          }
          this.rfidList.rfidListLoader = false
        })
        .catch(error => {
          console.error(error);
          this.rfidList.rfidListLoader = false
          this.rfidList.rfidListState = false
      });
    }
  },
  async mounted() {
    console.log("hey")
    this.getRfidList()

    // unshift
  }
}; 