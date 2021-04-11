<template>
  <div class="home">
    <ActivePilots/>
  </div>
</template>

<script>
// @ is an alias to /src
import ActivePilots from '@/components/ActivePilots.vue'

export default {
  name: 'Home',
  components: {
    ActivePilots
  }
}
</script>
