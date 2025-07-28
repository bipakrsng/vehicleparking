<template>
  <nav-bar/>
  <Hero/>
  <Feature />
  <how-it-works/>
  <Contact/>
</template>
<script>
import Hero from './Hero.vue'
import Feature from './Feature.vue'
import HowItWorks from './HowItWorks.vue';
import Contact from './Contact.vue';
export default{
  components:{
    Hero,
    Feature,
    HowItWorks,Contact
  }
}
</script>