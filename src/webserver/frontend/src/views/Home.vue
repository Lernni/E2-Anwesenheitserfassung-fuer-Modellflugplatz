<template>
  <div class="container">
    <h2>Aktive Flugsessions</h2>
    <ActiveSessions/>
    <hr>
    <h2>Admin-Bereich</h2>
    <AdminPanel/>
  </div>
</template>

<script>
// @ is an alias to /src
import ActiveSessions from '@/components/ActiveSessions.vue'
import AdminPanel from '@/components/AdminPanel.vue'

export default {
  name: 'Home',
  components: {
    ActiveSessions,
    AdminPanel
  }
}
</script>
