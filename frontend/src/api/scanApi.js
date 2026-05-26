import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const scanApi = {
  getHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  runScan: async (repoUrl, userId = null, useAiExplanation = true) => {
    const response = await apiClient.post('/scan', {
      repo_url: repoUrl,
      user_id: userId,
      use_ai_explanation: useAiExplanation,
    });
    return response.data;
  },

  getScanHistory: async (userId) => {
    const response = await apiClient.get(`/scans/${userId}`);
    return response.data;
  },

  getScanDetails: async (scanId) => {
    const response = await apiClient.get(`/scan/${scanId}`);
    return response.data;
  },

  deleteScan: async (scanId) => {
    const response = await apiClient.delete(`/scan/${scanId}`);
    return response.data;
  },

  explainIssue: async (issueId, userId = null) => {
    const response = await apiClient.post('/explain', {
      issue_id: issueId,
      user_id: userId,
    });
    return response.data;
  },
};

export default apiClient;
const API_URL = API_BASE_URL;
export { API_URL };
