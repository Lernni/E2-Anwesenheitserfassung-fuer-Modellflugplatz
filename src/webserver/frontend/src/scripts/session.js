/*
  *** session.js ***
  - Mixin für Verwaltung der Session-Daten
  - Genutzt von: NewSession.vue, EditSession.vue
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
*/

export const formSession = {
  data() {
    return {
      form: {
        startTime: "",
        endTime: "",
        date: null,
        sessionLeader: false,
        guestName: null,
        guestText: null,
      }
    }
  }
}