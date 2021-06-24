/*
  *** auth.js ***
  - Mixin für Passwortverschlüsselung und Eingabedaten im Login und Signup
  - Genutzt von: Login.vue, Signup.vue
  - Autor: Lenny Reitz
  - Mail: lenny.reitz@htw-dresden.de
*/

// siehe https://zetcode.com/python/bcrypt/
// siehe https://www.codespot.org/hashing-passwords-in-nodejs/

import bcrypt from 'bcryptjs'

export const authService = {
  data() {
    return {
      form: {
        username: null,
        password: null
      }
    }
  },
  methods: {
    encryptPassword(password) {
      const salt = bcrypt.genSaltSync(10)
      return bcrypt.hashSync(password, salt)
    }
  }
}