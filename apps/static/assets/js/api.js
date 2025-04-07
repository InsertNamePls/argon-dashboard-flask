// apps/static/assets/js/api.js

// Base API fetcher function with error handling
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'same-origin', // Send cookies for authentication
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `API error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Error calling ${endpoint}:`, error);
        throw error;
    }
}

// API functions for each category
const datasetsAPI = {
    async getAll() {
        return fetchAPI('/dashboard/api/datasets');
    },
    
    async getById(id) {
        return fetchAPI(`/dashboard/api/datasets/${id}`);
    },
    
    async create(data) {
        return fetchAPI('/dashboard/api/datasets', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

const modelsAPI = {
    async getAll() {
        return fetchAPI('/dashboard/api/models');
    },
    
    async getById(id) {
        return fetchAPI(`/dashboard/api/models/${id}`);
    },
    
    async train(data) {
        return fetchAPI('/dashboard/api/models/train', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

const endpointsAPI = {
    async getAll() {
        return fetchAPI('/dashboard/api/endpoints');
    },
    
    async getById(id) {
        return fetchAPI(`/dashboard/api/endpoints/${id}`);
    },
    
    async deploy(data) {
        return fetchAPI('/dashboard/api/endpoints/deploy', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async invoke(id, data) {
        return fetchAPI(`/dashboard/api/endpoints/${id}/invoke`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};