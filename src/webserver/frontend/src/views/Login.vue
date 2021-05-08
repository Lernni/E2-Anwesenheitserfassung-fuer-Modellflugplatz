<template>
  <b-card class="login-box" title="Login">
    <b-form>
      <b-form-group label="Benutzername" label-for="userInput">
        <b-form-input type="text" id="userInput"></b-form-input>
      </b-form-group>
      <b-form-group label="Passwort" label-for="passwordInput">
        <b-form-input type="password" id="passwordInput"></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Anmelden</b-button>
    </b-form>
  </b-card>
</template>

<script>
export default {
  name: 'Login'
}
</script>

<style>

</style>