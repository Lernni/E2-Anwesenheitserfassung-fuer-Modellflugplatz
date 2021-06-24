/*
  *** auth.js ***
  - Mixin für Formvalidierung durch Vuelidate
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
*/

// siehe https://vuelidate.js.org/#getting-started

export const formValidation = {
  methods: {
    // Für das ausgweählte Formular-Objekt (z.B. Nutzername, Vorname, Passwort, ...) wird geprüft,
    // ob die gewünschten Anforderungen an die Eingabe erfüllt sind
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name];
      return $dirty ? !$error : null;
    },

    // Wird ausgeführt, um ein Formular abzuschicken
    // Sind die alle gewünschten Anforderungen an das Formular erfüllt, dann abschicken
    validateSubmit(event) {
      event.preventDefault()
      // Entscheide die Korrektheit der Eingabe für alle "unberührten" Felder
      this.$v.form.$touch()
      return !this.$v.form.$anyError
    },

    onReset(event) {
      event.preventDefault()
    },
  }
}