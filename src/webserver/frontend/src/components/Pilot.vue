<template>
  <div class="pilot">
    <h2>{{ header }}</h2>
    <b-container class="w-75">
      <b-alert variant="danger" :show="rfidList.rfidListState == false" dismissible>
        RFID-Kennungen konnten nicht geladen werden!
      </b-alert>
      <slot name="alerts"></slot>
      <b-overlay :show="pilot.pilotLoader">
        <b-form v-show="(pilot.pilotState != false) ? !submit.submitState : submit.submitState" @submit="onSubmit" :novalidate="true">
          <h4>Pilotendaten</h4>
          <b-row cols="2">
            <b-col>
              <b-form-group label="Vorname" label-for="pilot-name-input">
                <b-form-input id="pilot-name-input" v-model.trim="value.pilotName.$model" :state="states.pilotName"></b-form-input>
                <b-form-invalid-feedback>
                  Ungültiger Vorname
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="Nachname" label-for="pilot-surname-input">
                <b-form-input id="pilot-surname-input" v-model.trim="value.pilotSurname.$model" :state="states.pilotSurname"></b-form-input>
                <b-form-invalid-feedback>
                  Ungültiger Nachname
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col> 
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
          <b-row cols="2">
            <b-col>
              <b-form-group label="Nutzername" label-for="pilot-username-input" description="Der Pilot vergibt das Passwort beim ersten Anmeldeversuch selbst.">
                <b-form-input id="pilot-username-input" v-model.trim="value.pilotUsername.$model" :state="states.pilotUsername"></b-form-input>
                <b-form-invalid-feedback>
                  Ungültiger Nutzername
                </b-form-invalid-feedback>
              </b-form-group>
              <b-form-checkbox id="admin-checkbox" v-model="value.isAdmin.$model" name="admin-checkbox">
                Pilot hat Adminrechte
              </b-form-checkbox>
              <slot name="login-form"></slot>
            </b-col>
          </b-row>

          <b-button class="mt-3" type="submit" variant="primary" :disabled="submit.submitLoader">
            <b-spinner v-show="submit.submitLoader" small></b-spinner>
            {{ submitText }}
          </b-button>
        </b-form>
      </b-overlay>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "Pilot",
  props: ["header", "submitText", "value", "states", "submit", "rfidList", "pilot"],
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.$emit("formSubmit", event)
    }
  }
}
</script>