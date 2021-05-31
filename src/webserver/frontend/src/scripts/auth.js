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