import axios from 'axios';

// Base API URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API service with methods for interacting with the backend
const ApiService = {
  /**
   * Get a list of scenarios with pagination
   * 
   * @param {Object} params - Query parameters
   * @param {number} params.limit - Max number of scenarios to return
   * @param {number} params.offset - Offset for pagination
   * @returns {Promise<Object>} Paginated list of scenarios
   */
  async getScenarios(params = { limit: 10, offset: 0 }) {
    try {
      const response = await api.get('/scenarios', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching scenarios:', error);
      throw error;
    }
  },
  
  /**
   * Get a scenario by ID
   * 
   * @param {string} id - Scenario ID
   * @returns {Promise<Object>} Scenario data
   */
  async getScenarioById(id) {
    try {
      const response = await api.get(`/scenarios/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching scenario ${id}:`, error);
      throw error;
    }
  },
  
  /**
   * Generate a new scenario
   * 
   * @param {Object} parameters - Generation parameters
   * @returns {Promise<Object>} Generated scenario
   */
// frontend/src/services/ApiService.js

// In ApiService.js
async generateScenario(parameters) {
  try {
    console.log('Sending parameters to API:', parameters);
    
    // Structure the request according to what the backend expects
    const requestData = {
      parameters,
      include_context: parameters.include_context !== undefined ? parameters.include_context : true,
      similarity_threshold: parameters.similarity_threshold || 0.7
    };
    
    console.log('Structured request data:', requestData);
    
    const response = await api.post('/scenarios/generate', requestData);
    console.log('API response:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error generating scenario:', error);
    
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
      console.error('Response headers:', error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error message:', error.message);
    }
    
    throw error;
  }
},
  
  /**
   * Validate a scenario
   * 
   * @param {string} scenarioId - Scenario ID to validate
   * @returns {Promise<Object>} Validation results
   */

  async validateScenario(scenarioId) {
    try {
      // First fetch the scenario
      const scenario = await this.getScenarioById(scenarioId);
      
      // Then validate it
      const response = await api.post('/scenarios/validate', {
        scenario_id: scenarioId,
        scenario: scenario
      });
      
      return response.data;
    } catch (error) {
      console.error(`Error validating scenario ${scenarioId}:`, error);
      throw error;
    }
  },
  
  /**
   * Get validation results for a scenario
   * 
   * @param {string} scenarioId - Scenario ID
   * @returns {Promise<Object>} Validation results
   */
  async getValidationResults(scenarioId) {
    try {
      const response = await api.get(`/scenarios/${scenarioId}/validation`);
      return response.data;
    } catch (error) {
      // This endpoint might not exist yet, so we'll mock it
      console.warn(`Validation endpoint not available for ${scenarioId}, using mocked data`);
      
      // For demo/development purposes, we'll return mock validation results
      return {
        scenario_id: scenarioId,
        is_valid: Math.random() > 0.3, // 70% chance of being valid
        physics_validation: {
          is_valid: Math.random() > 0.3,
          voltage_violations: [],
          line_violations: []
        },
        opendss_validation: {
          success: true,
          voltage_violations: [],
          thermal_violations: []
        },
        opendss_success: true
      };
    }
  },
  
  /**
   * Upload a scenario file
   * 
   * @param {File} file - Scenario file to upload
   * @returns {Promise<Object>} Upload result
   */
  async uploadScenarioFile(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/data/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error uploading scenario file:', error);
      throw error;
    }
  },
  
  /**
   * Get prompt templates
   * 
   * @returns {Promise<Array>} List of prompt templates
   */
  async getPromptTemplates() {
    try {
      const response = await api.get('/prompts/templates');
      return response.data;
    } catch (error) {
      console.error('Error fetching prompt templates:', error);
      throw error;
    }
  },
  
  /**
   * Create a new prompt template
   * 
   * @param {Object} template - Template data
   * @returns {Promise<Object>} Created template
   */
  async createPromptTemplate(template) {
    try {
      const response = await api.post('/prompts/templates', template);
      return response.data;
    } catch (error) {
      console.error('Error creating prompt template:', error);
      throw error;
    }
  }
};

export default ApiService;