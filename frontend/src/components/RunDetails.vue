<template>
  <div class="run-details-overlay" @click.self="$emit('close')">
    <div class="run-details-modal">
      <div class="modal-header">
        <h3>Run Details: {{ runName }}</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else class="modal-content">
        <div class="section">
          <h4>Info</h4>
          <div class="info-grid">
            <div class="info-item">
              <label>Run ID</label>
              <span>{{ run.info.run_id }}</span>
            </div>
            <div class="info-item">
              <label>Status</label>
              <span>{{ run.info.status }}</span>
            </div>
            <div class="info-item">
              <label>Start Time</label>
              <span>{{ formatDate(run.info.start_time) }}</span>
            </div>
          </div>
        </div>

        <div class="section">
          <h4>Params</h4>
          <table class="details-table">
            <thead>
              <tr>
                <th>Key</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="param in run.data.params" :key="param.key">
                <td>{{ param.key }}</td>
                <td>{{ param.value }}</td>
              </tr>
              <tr v-if="!run.data.params?.length">
                <td colspan="2" class="empty">No parameters</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="section">
          <h4>Model Metrics</h4>
          <div class="metrics-list">
            <div v-for="metric in modelMetrics" :key="metric.key" class="metric-item">
              <div class="metric-header" @click="toggleMetricHistory(metric.key)">
                <span class="metric-key">{{ metric.key }}</span>
                <span class="metric-value">{{ metric.value }}</span>
                <span class="expand-icon">{{ expandedMetric === metric.key ? '▼' : '▶' }}</span>
              </div>
              <div v-if="expandedMetric === metric.key" class="metric-history">
                <MetricChart 
                  v-if="metricHistory[metric.key]" 
                  :label="metric.key" 
                  :data="metricHistory[metric.key]" 
                />
                <div v-else class="loading-history">Loading history...</div>
              </div>
            </div>
            <div v-if="!modelMetrics.length" class="empty">No model metrics</div>
          </div>
        </div>

        <div class="section">
          <h4>System Metrics</h4>
          <div class="metrics-list">
            <div v-for="metric in systemMetrics" :key="metric.key" class="metric-item">
              <div class="metric-header" @click="toggleMetricHistory(metric.key)">
                <span class="metric-key">{{ metric.key }}</span>
                <span class="metric-value">{{ metric.value }}</span>
                <span class="expand-icon">{{ expandedMetric === metric.key ? '▼' : '▶' }}</span>
              </div>
              <div v-if="expandedMetric === metric.key" class="metric-history">
                <MetricChart 
                  v-if="metricHistory[metric.key]" 
                  :label="metric.key" 
                  :data="metricHistory[metric.key]" 
                />
                <div v-else class="loading-history">Loading history...</div>
              </div>
            </div>
            <div v-if="!systemMetrics.length" class="empty">No system metrics</div>
          </div>
        </div>

        <div class="section">
          <h4>Artifacts</h4>
          <table class="details-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Path</th>
                <th>Type</th>
                <th>Size</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="artifact in artifacts" :key="artifact.path">
                <td>{{ artifact.path.split('/').pop() }}</td>
                <td>{{ artifact.path }}</td>
                <td>{{ getArtifactType(artifact.path) }}</td>
                <td>{{ artifact.file_size || '-' }}</td>
              </tr>
              <tr v-if="!artifacts.length">
                <td colspan="4" class="empty">No artifacts</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { api } from '../services/api';
import MetricChart from './MetricChart.vue';

const props = defineProps({
  runId: String
});

defineEmits(['close']);

const run = ref(null);
const artifacts = ref([]);
const loading = ref(true);

const runName = computed(() => {
  if (!run.value) return '...';
  return run.value.data.tags?.find(t => t.key === 'mlflow.runName')?.value || run.value.info.run_name || run.value.info.run_id;
});

const modelMetrics = computed(() => {
  if (!run.value?.data?.metrics) return [];
  return run.value.data.metrics.filter(m => !m.key.startsWith('system/'));
});

const systemMetrics = computed(() => {
  if (!run.value?.data?.metrics) return [];
  return run.value.data.metrics.filter(m => m.key.startsWith('system/'));
});

onMounted(async () => {
  try {
    const data = await api.getRun(props.runId);
    run.value = data.run;
    
    const artifactsData = await api.getArtifacts(props.runId);
    artifacts.value = artifactsData.files || [];
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

function formatDate(timestamp) {
  if (!timestamp) return '-';
  return new Date(parseInt(timestamp)).toLocaleString();
}

const expandedMetric = ref(null);
const metricHistory = ref({});

async function toggleMetricHistory(metricKey) {
  if (expandedMetric.value === metricKey) {
    expandedMetric.value = null;
    return;
  }

  expandedMetric.value = metricKey;
  
  if (!metricHistory.value[metricKey]) {
    try {
      const history = await api.getMetricHistory(props.runId, metricKey);
      metricHistory.value[metricKey] = history.metrics;
    } catch (e) {
      console.error('Failed to fetch metric history:', e);
    }
  }
}

function getArtifactType(path) {
  const ext = path.split('.').pop();
  return ext === path ? 'unknown' : ext;
}
</script>

<style scoped>
.run-details-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.run-details-modal {
  background: white;
  width: 800px;
  max-width: 90%;
  height: 80vh;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-content {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.section {
  margin-bottom: 30px;
}

.section h4 {
  margin-bottom: 15px;
  color: var(--primary-color);
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 5px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-size: 0.85rem;
  color: #6c757d;
  margin-bottom: 4px;
}

.info-item span {
  font-weight: 500;
  word-break: break-all;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
}

.details-table th, .details-table td {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.details-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.metrics-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.metric-item {
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f8f9fa;
  cursor: pointer;
  transition: background 0.2s;
}

.metric-header:hover {
  background: #e9ecef;
}

.metric-key {
  font-weight: 600;
  flex: 1;
}

.metric-value {
  font-family: monospace;
  margin-right: 15px;
}

.expand-icon {
  font-size: 0.8rem;
  color: #6c757d;
}

.metric-history {
  padding: 15px;
  background: white;
  border-top: 1px solid #f0f0f0;
}

.loading-history {
  text-align: center;
  color: #6c757d;
  padding: 20px;
}

.empty {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 20px;
}
</style>
