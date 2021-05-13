<template>
  <div class="active-sessions-table">
    <b-table striped :items="items" :fields="fields"></b-table>
    <p class="font-italic text-right">Letzte Aktualisierung: --:--</p>
  </div>
</template>

<script>
export default {
  name: 'ActiveSessions',
  props: {
    msg: String
  },
  inject: ['items'],
  data() {
    return {
      fields: [
        {key: "pilot_name", label: "Pilot"},
        {key: "start_time", label: "Beginn"},
        {
          key: "session_leader",
          label: "Flugleiter",
          formatter: (value) => {
            return value ? "F" : ""
          }
        }
      ]
    };
  },
  
}
</script>