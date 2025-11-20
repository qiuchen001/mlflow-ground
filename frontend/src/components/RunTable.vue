<template>
  <div class="run-table-container">
    <div v-if="!experimentId" class="empty-state">
      Select an experiment to view runs.
    </div>
    <div v-else-if="loading" class="loading">
      Loading runs...
    </div>
    <div v-else>
      <div class="table-header">
        <h3>Runs for Experiment {{ experimentId }}</h3>
        <span class="count">{{ runs.length }} runs found</span>
      </div>
      
      <div class="table-wrapper">
        <table class="run-table">
          <thead>
            <tr>
              <th>Run Name</th>
              <th>Date</th>
              <th>User</th>
              <th>Status</th>
              <!-- Dynamic headers for metrics/params could go here, keeping it simple for now -->
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="run in runs" :key="run.info.run_id" @click="viewRun(run)">
              <td class="name-cell">{{ run.data.tags?.find(t => t.key === 'mlflow.runName')?.value || run.info.run_name || run.info.run_id }}</td>
              <td>{{ formatDate(run.info.start_time) }}</td>
              <td>{{ run.data.tags?.find(t => t.key === 'mlflow.user')?.value || 'Unknown' }}</td>
              <td>
                <span :class="['status-badge', run.info.status.toLowerCase()]">{{ run.info.status }}</span>
              </td>
              <td>{{ run.data.tags?.find(t => t.key === 'mlflow.source.name')?.value || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { api } from '../services/api';

const props = defineProps({
  experimentId: String
});

const emit = defineEmits(['select-run']);

const runs = ref([]);
const loading = ref(false);

watch(() => props.experimentId, async (newId) => {
  if (!newId) return;
  loading.value = true;
  try {
    const data = await api.getRuns(newId);
    runs.value = data.runs || [];
  } catch (e) {
    console.error(e);
    runs.value = [];
  } finally {
    loading.value = false;
  }
});

function formatDate(timestamp) {
  if (!timestamp) return '-';
  return new Date(parseInt(timestamp)).toLocaleString();
}

function viewRun(run) {
  emit('select-run', run.info.run_id);
}
</script>

<style scoped>
.run-table-container {
  flex: 1;
  padding: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.empty-state, .loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #6c757d;
  font-size: 1.1rem;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h3 {
  margin: 0;
}

.count {
  color: #6c757d;
}

.table-wrapper {
  flex: 1;
  overflow: auto;
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.run-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.run-table th, .run-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.run-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
  position: sticky;
  top: 0;
}

.run-table tr:hover {
  background-color: var(--hover-bg);
  cursor: pointer;
}

.name-cell {
  font-weight: 500;
  color: var(--primary-color);
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.finished {
  background-color: #d1e7dd;
  color: #0f5132;
}

.status-badge.failed {
  background-color: #f8d7da;
  color: #842029;
}

.status-badge.running {
  background-color: #fff3cd;
  color: #664d03;
}
</style>
