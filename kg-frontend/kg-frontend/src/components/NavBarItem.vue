<template>
  <div @click="itemClick" :class="{ active: isActive }">
    <div><slot name="nav"></slot></div>
  </div>
</template>
<script>
export default {
  name: "NavBarItem",
  components: {},
  props: {
    path: String,
  },
  data() {
    return {};
  },
  computed: {
    isActive() {
      return this.$route.path.indexOf(this.path) !== -1;
    },
  },
  methods: {
    itemClick() {
      this.$router.replace(this.path);
    },
  },
};
</script>
<style scoped>
.active {
  background-color: #e0e7ff;
  color: #4338ca;
}
</style>
