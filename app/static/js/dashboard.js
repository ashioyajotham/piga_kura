class DashboardManager {
    constructor() {
        this.updateInterval = null;
        this.initializeEventListeners();
        this.startPolling();
    }

    initializeEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            this.updateVoteCount();
            const ballotControls = document.querySelectorAll('.ballot-control');
            ballotControls.forEach(control => {
                control.addEventListener('click', this.handleBallotControl.bind(this));
            });
        });
    }

    async updateVoteCount() {
        try {
            const response = await fetch('/api/votes/count');
            const data = await response.json();
            this.updateDashboardUI(data);
        } catch (error) {
            console.error('Error updating vote count:', error);
        }
    }

    updateDashboardUI(data) {
        const votesContainer = document.getElementById('votes-container');
        if (votesContainer && data.votes) {
            // Update UI with vote data
            Object.entries(data.votes).forEach(([candidateId, count]) => {
                const element = document.getElementById(`vote-count-${candidateId}`);
                if (element) element.textContent = count;
            });
        }
    }

    startPolling() {
        this.updateInterval = setInterval(() => this.updateVoteCount(), 5000);
    }

    async handleBallotControl(event) {
        const action = event.target.dataset.action;
        const ballotId = event.target.dataset.ballotId;
        
        try {
            const response = await fetch(`/api/ballot/${ballotId}/${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                this.updateVoteCount();
            }
        } catch (error) {
            console.error('Error controlling ballot:', error);
        }
    }
}

// Initialize dashboard
const dashboard = new DashboardManager();
