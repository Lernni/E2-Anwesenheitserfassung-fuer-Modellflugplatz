<!--
  *** Pilot.vue ***
  - Vue Komponente zum Erstellen der Piloten-Formulare
  - Genutzt von: NewPilot.vue, EditPilot.vue, ReactivatePilot.vue
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
-->

<template>
  <div class="pilot">
    <h2>{{ header }}</h2>

    <b-alert variant="danger" :show="rfidList.rfidListState == false" dismissible>
      RFID-Kennungen konnten nicht geladen werden!
    </b-alert>

    <!-- Formularspezifische Meldungen -->
    <slot name="alerts"></slot>

    <b-container fluid="md">
      <b-row class="justify-content-center">
        <b-col lg="10">
          <b-overlay :show="pilot.pilotLoader">
            <b-form v-show="formShow()" @submit="onSubmit" :novalidate="true">
              <h4>Pilotendaten</h4>
              <b-row cols="2">
                <b-col cols="12" md="6">
                  <b-form-group label="Vorname" label-for="pilot-name-input">
                    <b-form-input
                      id="pilot-name-input"
                      v-model.trim="value.pilotName.$model"
                      :state="states.pilotName"
                      @change="onChange()"
                      autocomplete="off"
                    >
                    </b-form-input>
                    <b-form-invalid-feedback v-if="!value.pilotName.maxLength">
                      Vorname zu lang!
                    </b-form-invalid-feedback>
                    <b-form-invalid-feedback>
                      Ungültiger Vorname!
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
                <b-col cols="12" md="6">
                  <b-form-group label="Nachname" label-for="pilot-surname-input">
                    <b-form-input
                      id="pilot-surname-input"
                      v-model.trim="value.pilotSurname.$model"
                      :state="states.pilotSurname"
                      @change="onChange()"
                      autocomplete="off"
                    >
                    </b-form-input>
                    <b-form-invalid-feedback v-if="!value.pilotSurname.maxLength">
                      Nachname zu lang!
                    </b-form-invalid-feedback>
                    <b-form-invalid-feedback>
                      Ungültiger Nachname!
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
                <b-col cols="12" md="6"> 
                  <b-form-group label="e-ID" label-for="e-id-input">
                    <b-form-input
                      id="e-id-input"
                      v-model.trim="value.eID.$model"
                      :state="states.eID"
                      autocomplete="off"
                    >
                    </b-form-input>
                  </b-form-group>
                </b-col>
                <b-col cols="12" md="6"> 
                  <b-form-group label="RFID-Kennung" label-for="rfid-select">
                    <b-overlay :show="rfidList.rfidListLoader" spinner-type="grow" spinner-small>
                      <b-form-select required id="rfid-select" v-model.trim="value.rfid.$model" :state="states.rfid" :options="rfidList.rfidList"></b-form-select>
                      <b-form-invalid-feedback id="input-live-feedback" :state="states.rfid">
                        Ungültige RFID-Kennung
                      </b-form-invalid-feedback>
                    </b-overlay>
                  </b-form-group>
                </b-col>
              </b-row>

              <h4>Login-Informationen</h4>
              <b-row>
                <b-col cols="12">
                  <b-form-group label-for="pilot-username-input" description="Der Pilot vergibt das Passwort beim ersten Anmeldeversuch selbst.">
                      <div class="mt-2 mb-2">
                        Nutzername: 
                        <b-spinner small type="grow" label="Small Spinner" v-show="username.pilotUsernameLoader"></b-spinner>
                        <span class="font-weight-bold"> {{ value.pilotUsername.$model }} </span>
                      </div>
                      <b-form-invalid-feedback :state="username.pilotUsernameState != false">
                        Nutzernamen konnten nicht geladen werden!
                      </b-form-invalid-feedback>
                  </b-form-group>
                  <b-form-checkbox id="admin-checkbox" v-model="value.isAdmin.$model" name="admin-checkbox">
                    Pilot hat Adminrechte
                  </b-form-checkbox>
                  <slot name="login-form"></slot>
                </b-col>
              </b-row>

              <div class="footer-buttons">
                <b-button class="mt-3" type="submit" variant="primary" :disabled="submit.submitLoader">
                  <b-spinner v-show="submit.submitLoader" small></b-spinner>
                  {{ submitText }}
                </b-button>
              </div>
            </b-form>
          </b-overlay>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "Pilot",
  // props werden von den jeweiligen Views geliefert
  props: ["header", "submitText", "value", "states", "submit", "rfidList", "pilot", "username"],
  methods: {
    // events werden von den jeweiligen Views ausgewertet
    onSubmit(event) {
      event.preventDefault()
      this.$emit("formSubmit", event)
    },

    onChange() {
      this.$emit("setUsername")
    },
    
    formShow() {
      if (this.pilot.pilotState == false) return false
      if (this.submit.submitState == true) return false
      if (this.rfidList.noRfid == true) return false
      return true
    }
  }
}
</script>