<template>
  <h2>Aktive Flugsessions</h2>
  <ActiveSessionsTable/>
  <hr>
  <h2>Admin-Bereich</h2>
  <AdminPanel/>
</template>

<script>
// @ is an alias to /src
import ActiveSessionsTable from '@/components/ActiveSessionsTable.vue'
import AdminPanel from '@/components/AdminPanel.vue'

export default {
  name: 'Home',
  components: {
    ActiveSessionsTable,
    AdminPanel
  }
}
</script>
