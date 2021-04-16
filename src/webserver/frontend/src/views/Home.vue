<template>
  <div class="home">
    <AllPilots/>
  </div>
</template>

<script>
// @ is an alias to /src
import AllPilots from '@/components/AllPilots.vue'

export default {
  name: 'Home',
  components: {
    AllPilots
  }
}
</script>
