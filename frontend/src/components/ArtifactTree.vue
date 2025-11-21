<template>
  <div class="artifact-tree">
    <div v-if="loading" class="loading-tree">Loading...</div>
    <div v-else>
      <div v-for="file in files" :key="file.path" class="tree-item">
        <div 
          class="tree-item-header" 
          :style="{ paddingLeft: depth * 20 + 'px' }"
          @click="handleItemClick(file)"
        >
          <span class="icon">{{ file.is_dir ? (expanded[file.path] ? '📂' : '📁') : '📄' }}</span>
          <span class="name">{{ file.path.split('/').pop() }}</span>
        </div>
        
        <div v-if="file.is_dir && expanded[file.path]" class="tree-children">
          <ArtifactTree 
            :run-id="runId" 
            :path="file.path" 
            :depth="depth + 1"
            @file-selected="$emit('file-selected', $event)"
          />
        </div>
      </div>
      <div v-if="!files.length" class="empty-tree" :style="{ paddingLeft: depth * 20 + 'px' }">
        (empty)
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { api } from '../services/api';

const props = defineProps({
  runId: {
    type: String,
    required: true
  },
  path: {
    type: String,
    default: ''
  },
  depth: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['file-selected']);

const files = ref([]);
const loading = ref(true);
const expanded = ref({});

onMounted(async () => {
  try {
    const data = await api.getArtifacts(props.runId, props.path);
    files.value = data.files || [];
    // Sort: directories first, then files
    files.value.sort((a, b) => {
      if (a.is_dir === b.is_dir) {
        return a.path.localeCompare(b.path);
      }
      return a.is_dir ? -1 : 1;
    });
  } catch (e) {
    console.error('Failed to fetch artifacts:', e);
  } finally {
    loading.value = false;
  }
});

function handleItemClick(file) {
  if (file.is_dir) {
    expanded.value[file.path] = !expanded.value[file.path];
  } else {
    emit('file-selected', file);
  }
}
</script>

<style scoped>
.tree-item-header {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  cursor: pointer;
  user-select: none;
}

.tree-item-header:hover {
  background-color: #f0f0f0;
}

.icon {
  margin-right: 6px;
  font-size: 1.1em;
}

.name {
  font-size: 0.9em;
}

.loading-tree, .empty-tree {
  padding: 4px 8px;
  color: #888;
  font-style: italic;
  font-size: 0.9em;
}
</style>
