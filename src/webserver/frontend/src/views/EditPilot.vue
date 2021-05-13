<template>
  <div class="edit-pilot">
    <h2>Pilot erstellen</h2>
    <b-form>
      <b-container>
        <b-row cols="2">
          <b-col>
            <b-form-group label="Nachname" label-for="pilot-surname-input">
              <b-form-input id="pilot-surname-input" v-model="surname"></b-form-input>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Vorname" label-for="pilot-name-input">
              <b-form-input id="pilot-name-input" v-model="name"></b-form-input>
            </b-form-group>
          </b-col>
          <b-col></b-col>
        </b-row>
      </b-container>
    </b-form>
  </div>
</template>

<script>
// Pilot erstellen
// GET /rfid

// POST /pilots


// Pilot modifizieren
// GET /pilots?id=2
// GET /rfid
// -> Vorauswahl für den eigenen Ausweis

// PUT /pilots


// Pilot reaktivieren
// GET /pilots?id=2
// GET /rfid

// PUT /pilots JSON: {active=true}
export default {

}
</script>

<style>

</style>