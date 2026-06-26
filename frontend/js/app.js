const API_URL = 'http://localhost:8000';

class App {
    constructor() {
        this.token = localStorage.getItem('token') || null;
        this.user = JSON.parse(localStorage.getItem('user')) || null;
        
        document.addEventListener('DOMContentLoaded', () => {
            this.updateNav();
            setTimeout(() => {
                if (window.lucide) {
                    lucide.createIcons();
                }
            }, 0);
        });
    }

    updateNav() {
        const authSection = document.getElementById('nav-auth-section');
        if (!authSection) return;

        if (this.token) {
            authSection.innerHTML = `
                <a href="dashboard.html" class="btn-outline">
                    <i data-lucide="user"></i> Profil
                </a>
                <button class="btn-primary" onclick="app.logout()">Chiqish</button>
            `;
        } else {
            authSection.innerHTML = `
                <a href="login.html" class="btn-outline">Kirish</a>
                <a href="register.html" class="btn-primary">Ro'yxatdan o'tish</a>
            `;
        }
        if (window.lucide) {
            lucide.createIcons();
        }
    }

    showToast(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? 'check-circle' : 'alert-circle';
        toast.innerHTML = `<i data-lucide="${icon}"></i> <span>${message}</span>`;
        
        container.appendChild(toast);
        if (window.lucide) lucide.createIcons();
        
        setTimeout(() => {
            toast.style.animation = 'fadeIn 0.3s ease reverse forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    async apiCall(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...(this.token && { 'Authorization': `Bearer ${this.token}` }),
            ...options.headers
        };

        try {
            const response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });
            const data = await response.json().catch(() => ({}));
            
            if (!response.ok) {
                throw new Error(data.detail || data.message || 'Xatolik yuz berdi');
            }
            return data;
        } catch (error) {
            this.showToast(error.message, 'error');
            throw error;
        }
    }

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        this.updateNav();
        window.location.href = 'index.html';
    }
}

const app = new App();
