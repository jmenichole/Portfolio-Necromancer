// Portfolio Necromancer Dashboard JavaScript

// API Base URL - change this if running on different host/port
const API_BASE_URL = window.location.origin;

// State
let projectCount = 0;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeProjectManagement();
    initializeFormHandlers();
    
    // Add initial project
    addProject();
});

// Tab Management
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.getAttribute('data-tab');
            
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            button.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });
}

// Project Management
function initializeProjectManagement() {
    const addProjectBtn = document.getElementById('add-project-btn');
    addProjectBtn.addEventListener('click', addProject);
}

function addProject() {
    projectCount++;
    
    const template = document.getElementById('project-template');
    const clone = template.content.cloneNode(true);
    
    // Set project number
    clone.querySelector('.project-number').textContent = projectCount;
    
    // Add remove handler
    const removeBtn = clone.querySelector('.remove-project-btn');
    removeBtn.addEventListener('click', function() {
        this.closest('.project-card').remove();
    });
    
    document.getElementById('projects-container').appendChild(clone);
}

// Form Handlers
function initializeFormHandlers() {
    // Manual generation
    document.getElementById('generate-btn').addEventListener('click', generatePortfolio);
    
    // Auto generation
    document.getElementById('auto-generate-btn').addEventListener('click', autoGeneratePortfolio);
    
    // Error close
    document.getElementById('error-close-btn').addEventListener('click', hideError);
}

async function generatePortfolio() {
    try {
        // Validate and collect form data
        const ownerName = document.getElementById('owner-name').value.trim();
        const ownerEmail = document.getElementById('owner-email').value.trim();
        
        if (!ownerName || !ownerEmail) {
            showError('Please fill in required fields (Name and Email)');
            return;
        }
        
        const ownerTitle = document.getElementById('owner-title').value.trim() || 'Developer';
        const ownerBio = document.getElementById('owner-bio').value.trim() || '';
        const theme = document.getElementById('theme').value;
        const colorScheme = document.getElementById('color-scheme').value;
        
        // Collect projects
        const projects = [];
        const projectCards = document.querySelectorAll('.project-card');
        
        if (projectCards.length === 0) {
            showError('Please add at least one project');
            return;
        }
        
        projectCards.forEach(card => {
            const title = card.querySelector('.project-title').value.trim();
            const category = card.querySelector('.project-category').value;
            const description = card.querySelector('.project-description').value.trim();
            const url = card.querySelector('.project-url').value.trim();
            const tagsStr = card.querySelector('.project-tags').value.trim();
            
            if (title) {
                const tags = tagsStr ? tagsStr.split(',').map(t => t.trim()) : [];
                
                projects.push({
                    title,
                    category,
                    description,
                    url: url || null,
                    tags
                });
            }
        });
        
        if (projects.length === 0) {
            showError('Please add at least one project with a title');
            return;
        }
        
        // Prepare request data
        const data = {
            owner: {
                name: ownerName,
                email: ownerEmail,
                title: ownerTitle,
                bio: ownerBio
            },
            projects,
            theme,
            color_scheme: colorScheme,
            show_watermark: true
        };
        
        // Show loading
        showLoading();
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (!response.ok) {
            throw new Error(result.error || 'Failed to generate portfolio');
        }
        
        // Show success
        showResult(result);
        
    } catch (error) {
        hideLoading();
        showError(error.message);
        console.error('Error:', error);
    }
}

async function autoGeneratePortfolio() {
    try {
        const configText = document.getElementById('config-json').value.trim();
        
        if (!configText) {
            showError('Please provide configuration');
            return;
        }
        
        // Try to parse as JSON or YAML
        let config;
        try {
            config = JSON.parse(configText);
        } catch (e) {
            // If not JSON, try to parse as YAML (simple approach)
            showError('Please provide valid JSON configuration. YAML parsing requires server-side conversion.');
            return;
        }
        
        const data = { config };
        
        // Show loading
        showLoading();
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/api/generate/auto`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        hideLoading();
        
        if (!response.ok) {
            throw new Error(result.error || 'Failed to auto-generate portfolio');
        }
        
        // Show success
        showResult(result);
        
    } catch (error) {
        hideLoading();
        showError(error.message);
        console.error('Error:', error);
    }
}

// UI Helper Functions
function showLoading() {
    hideResult();
    hideError();
    document.getElementById('loading-section').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading-section').style.display = 'none';
}

function showResult(result) {
    hideLoading();
    hideError();
    
    const section = document.getElementById('result-section');
    const message = document.getElementById('result-message');
    const previewLink = document.getElementById('preview-link');
    const downloadLink = document.getElementById('download-link');
    
    message.textContent = result.message || 'Your portfolio has been generated successfully!';
    
    if (result.project_count) {
        message.textContent += ` (${result.project_count} projects)`;
    }
    
    previewLink.href = `${API_BASE_URL}${result.preview_url}`;
    downloadLink.href = `${API_BASE_URL}${result.download_url}`;
    
    section.style.display = 'block';
    
    // Scroll to result
    section.scrollIntoView({ behavior: 'smooth' });
}

function hideResult() {
    document.getElementById('result-section').style.display = 'none';
}

function showError(message) {
    hideLoading();
    hideResult();
    
    const section = document.getElementById('error-section');
    const messageEl = document.getElementById('error-message');
    
    messageEl.textContent = message;
    section.style.display = 'block';
    
    // Scroll to error
    section.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    document.getElementById('error-section').style.display = 'none';
}

// API Health Check on Load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.error('API is not available:', error);
    }
}

// Check API health on load
checkAPIHealth();
