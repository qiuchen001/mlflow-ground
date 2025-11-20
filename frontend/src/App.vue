<template>
  <div class="app-container">
    <ExperimentList @select="onExperimentSelect" />
    <main class="main-content">
      <RunTable :experimentId="selectedExperimentId" @select-run="onRunSelect" />
    </main>
    <RunDetails v-if="selectedRunId" :runId="selectedRunId" @close="selectedRunId = null" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ExperimentList from './components/ExperimentList.vue';
import RunTable from './components/RunTable.vue';
import RunDetails from './components/RunDetails.vue';

const selectedExperimentId = ref(null);
const selectedRunId = ref(null);

function onExperimentSelect(id) {
  selectedExperimentId.value = id;
  selectedRunId.value = null; // Clear run selection when experiment changes
}

function onRunSelect(id) {
  selectedRunId.value = id;
}
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: var(--bg-color);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
