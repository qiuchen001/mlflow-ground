<template>
  <div class="experiment-list">
    <div class="header">
      <h2>Experiments</h2>
    </div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="list">
      <div
        v-for="exp in experiments"
        :key="exp.experiment_id"
        class="experiment-item"
        :class="{ active: selectedId === exp.experiment_id }"
        @click="selectExperiment(exp.experiment_id)"
      >
        <span class="name">{{ exp.name }}</span>
        <span class="id">#{{ exp.experiment_id }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from '../services/api';

const emit = defineEmits(['select']);
const experiments = ref([]);
const loading = ref(true);
const selectedId = ref(null);

onMounted(async () => {
  try {
    const data = await api.getExperiments();
    // MLflow search experiments returns { experiments: [...] }
    experiments.value = data.experiments || [];
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

function selectExperiment(id) {
  selectedId.value = id;
  emit('select', id);
}
</script>

<style scoped>
.experiment-list {
  width: 250px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
}

.header h2 {
  font-size: 1.2rem;
  margin: 0;
  color: var(--primary-color);
}

.list {
  flex: 1;
  overflow-y: auto;
}

.experiment-item {
  padding: 15px 20px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--hover-bg);
  transition: background-color 0.2s;
}

.experiment-item:hover {
  background-color: var(--hover-bg);
}

.experiment-item.active {
  background-color: #e7f1ff; /* Light blue */
  border-left: 4px solid var(--primary-color);
}

.name {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.id {
  font-size: 0.8rem;
  color: #6c757d;
}

.loading {
  padding: 20px;
  color: #6c757d;
  text-align: center;
}
</style>
