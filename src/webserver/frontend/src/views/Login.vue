<template>
  <div class="login-box card">
    <div class="card-body">
      <h5 class="card-title">Login</h5>
      <form action="">
        <div class="form-group">
          <label for="userInput">Benutzername</label>
          <input type="text" class="form-control" id="userInput">
        </div>
        <div class="form-group">
          <label for="passwordInput">Passwort</label>
          <input type="password" class="form-control" id="passwordInput">
        </div>
        <button type="submit" class="btn btn-primary">Anmelden</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login'
}
</script>

<style>

</style>