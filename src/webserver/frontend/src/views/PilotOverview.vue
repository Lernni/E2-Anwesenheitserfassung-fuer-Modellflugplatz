<template>
  <h2>Pilotenübersicht</h2>

  <div class="input-group mb-3">
    <input type="text" class="form-control" placeholder="Pilot">
    <div class="input-group-append">
      <button class="btn btn-primary" type="button">Suche</button>
    </div>
  </div>

  <PilotsTable/>

  <button class="btn btn-primary">Deaktivierte Piloten</button>
</template>

<script>
// @ is an alias to /src
import PilotsTable from '@/components/PilotsTable.vue'

export default {

  name: 'PilotOverview',
  components: {
    PilotsTable
  }
}
</script>
