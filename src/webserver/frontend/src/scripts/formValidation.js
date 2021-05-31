export const formValidation = {
  methods: {
    validateState(name) {
      const { $dirty, $error } = this.$v.form[name];
      return $dirty ? !$error : null;
    },

    validateSubmit(event) {
      event.preventDefault()
      this.$v.form.$touch()
      return !this.$v.form.$anyError
    },

    onReset(event) {
      event.preventDefault()
    },
  }
}