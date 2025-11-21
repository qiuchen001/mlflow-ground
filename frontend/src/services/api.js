const API_BASE_URL = 'http://127.0.0.1:8001';

export const api = {
    async getExperiments() {
        const response = await fetch(`${API_BASE_URL}/experiments`);
        if (!response.ok) {
            throw new Error('Failed to fetch experiments');
        }
        return response.json();
    },

    async getRuns(experimentId) {
        const response = await fetch(`${API_BASE_URL}/experiments/${experimentId}/runs`);
        if (!response.ok) {
            throw new Error('Failed to fetch runs');
        }
        return response.json();
    },

    async getRun(runId) {
        const response = await fetch(`${API_BASE_URL}/runs/${runId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch run details');
        }
        return response.json();
    },

    async getMetricHistory(runId, metricKey) {
        const response = await fetch(`${API_BASE_URL}/runs/${runId}/metrics/history?metric_key=${metricKey}`);
        if (!response.ok) {
            throw new Error('Failed to fetch metric history');
        }
        return response.json();
    },

    async getArtifacts(runId, path = null) {
        let url = `${API_BASE_URL}/runs/${runId}/artifacts`;
        if (path) {
            url += `?path=${path}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Failed to fetch artifacts');
        }
        return response.json();
    }
};
