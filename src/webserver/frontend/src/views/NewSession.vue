<template>
    <div class="add-session">
        <h2>Flugsession nachtragen</h2>
        <b-form>
            <b-row>
                <b-col cols="8">
                    <b-form-group id="pilot-name-group" label="Pilot" label-for="pilot-name-select">
                        <b-form-select id="pilot-name-select" v-model="selected" :options="options"></b-form-select>
                    </b-form-group>
                    <b-row>
                        <b-col>
                            <b-form-group id="session-start-group" label="Startzeit" label-for="session-start-picker">
                                <b-form-timepicker id="session-start-picker" placeholder="Start" v-model="value" locale="de"></b-form-timepicker>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group id="session-end-group" label="Endzeit" label-for="session-end-picker">
                                <b-form-timepicker id="session-end-picker" placeholder="Ende" v-model="value" locale="de"></b-form-timepicker>
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-form-group id="session-leader-group">
                        <b-form-checkbox id="session-leader-checkbox" name="session-leader-checkbox" v-model="status">Flugleiter</b-form-checkbox>
                    </b-form-group>
                    <b-form-group id="guest-check-group">
                        <b-form-checkbox id="guest-checkbox" name="guest-checkbox" v-model="guest">mit Gast</b-form-checkbox>
                    </b-form-group>
                    <b-container v-show="guest">
                        <b-form-group id="guest-name-group" label="Gastname" label-for="guest-input">
                            <b-form-input id="guest-input" v-model="text"></b-form-input>
                        </b-form-group>
                        <b-form-group id="guest-info-group" label="Gastinformationen" label-for="guest-textarea">
                            <b-form-textarea id="guest-textarea" v-model="text" rows="3"></b-form-textarea>
                        </b-form-group>
                    </b-container>
                </b-col>
                <b-col>
                    <b-form-group id="session_date" label="Datum" label-for="sessionDatePicker">
                        <b-calendar id="sessionDatePicker" v-model="value" locale="de-DE" :start-weekday="1"></b-calendar>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-button type="submit" variant="primary">Speichern</b-button>
        </b-form>
    </div>
</template>

<script>
// TODO: Pilotenauswahl: Namenssuche und Filter aus Pilotenliste
// TODO: GET Request: /pilot-list
// -> Backend liefert aktive Piloten: {pilot_id, pilot_name}
export default {
    name: "NewSession",
    // TODO: Submit: POST /sessions
    // Rückgabe: Hinzufügen erfolgreich -> Gehe auf die aufrufende Seite zurück
    data() {
        return {
            selected: null,
            options: [
                {value: null, text: "[ID] Pilotenname"},
                {value: 0, text: "[0] Max Mustermann"}
            ],
            guest: false
        }
    }
}
</script>