<template>
  <div class="pilot-overview">
    <h2>Pilotenübersicht</h2>

    <b-input-group class="mb-3">
      <b-form-input placeholder="Pilot"></b-form-input>
      <b-input-group-append>
        <b-button variant="primary">Suchen</b-button>
      </b-input-group-append>
    </b-input-group>

    <PilotsTable/>
  </div>
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
