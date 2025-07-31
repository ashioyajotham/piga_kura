// Admin Ballots Management JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Status toggle functionality
    document.querySelectorAll('.status-toggle').forEach(badge => {
        badge.addEventListener('click', function() {
            const ballotId = this.dataset.ballotId;
            const isActive = this.dataset.active === 'true';
            toggleBallotStatus(ballotId, !isActive);
        });
    });

    // Form submissions
    document.getElementById('createBallotForm').addEventListener('submit', handleCreateBallot);
    document.getElementById('editBallotForm').addEventListener('submit', handleEditBallot);
});

// View ballot details
function viewBallot(ballotId) {
    fetch(`/admin/api/ballots/${ballotId}`)
        .then(response => response.json())
        .then(ballot => {
            const content = `
                <div class="ballot-preview">
                    <h3>${ballot.title}</h3>
                    <p class="text-muted">${ballot.description || 'No description'}</p>
                    <div class="row">
                        <div class="col-md-6">
                            <strong>Type:</strong> ${ballot.ballot_type}<br>
                            <strong>Start:</strong> ${new Date(ballot.start_date).toLocaleString()}<br>
                            <strong>End:</strong> ${new Date(ballot.end_date).toLocaleString()}<br>
                        </div>
                        <div class="col-md-6">
                            <strong>Status:</strong> ${ballot.is_active ? 'Active' : 'Inactive'}<br>
                            <strong>Candidates:</strong> ${ballot.candidates?.length || 0}<br>
                            <strong>Total Votes:</strong> ${ballot.vote_count || 0}<br>
                        </div>
                    </div>
                </div>
            `;
            
            // Create and show modal
            const modal = new bootstrap.Modal(document.createElement('div'));
            // Implementation depends on your modal structure
            alert('Ballot Preview:\n' + ballot.title + '\n' + ballot.description);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading ballot details');
        });
}

// Edit ballot
function editBallot(ballotId) {
    fetch(`/admin/api/ballots/${ballotId}`)
        .then(response => response.json())
        .then(ballot => {
            document.getElementById('editBallotId').value = ballot.id;
            document.getElementById('editBallotTitle').value = ballot.title;
            document.getElementById('editBallotType').value = ballot.ballot_type;
            document.getElementById('editBallotDescription').value = ballot.description || '';
            document.getElementById('editBallotStartDate').value = formatDateForInput(ballot.start_date);
            document.getElementById('editBallotEndDate').value = formatDateForInput(ballot.end_date);
            document.getElementById('editBallotIsActive').checked = ballot.is_active;
            
            new bootstrap.Modal(document.getElementById('editBallotModal')).show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading ballot data');
        });
}

// Handle create ballot form submission
function handleCreateBallot(e) {
    e.preventDefault();
    
    const data = {
        title: document.getElementById('createBallotTitle').value,
        description: document.getElementById('createBallotDescription').value,
        ballot_type: document.getElementById('createBallotType').value,
        start_date: document.getElementById('createBallotStartDate').value,
        end_date: document.getElementById('createBallotEndDate').value,
        min_voters: parseInt(document.getElementById('createBallotMinVoters').value) || 0,
        max_voters: parseInt(document.getElementById('createBallotMaxVoters').value) || null,
        requires_verification: document.getElementById('createBallotRequiresVerification').checked,
        is_active: document.getElementById('createBallotIsActive').checked
    };

    fetch('/admin/api/ballots', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success || result.id) {
            bootstrap.Modal.getInstance(document.getElementById('createBallotModal')).hide();
            location.reload(); // Refresh to show new ballot
        } else {
            alert(result.error || 'Error creating ballot');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating ballot');
    });
}

// Handle edit ballot form submission
function handleEditBallot(e) {
    e.preventDefault();
    
    const ballotId = document.getElementById('editBallotId').value;
    const data = {
        title: document.getElementById('editBallotTitle').value,
        description: document.getElementById('editBallotDescription').value,
        ballot_type: document.getElementById('editBallotType').value,
        start_date: document.getElementById('editBallotStartDate').value,
        end_date: document.getElementById('editBallotEndDate').value,
        is_active: document.getElementById('editBallotIsActive').checked
    };

    fetch(`/admin/api/ballots/${ballotId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('editBallotModal')).hide();
            location.reload(); // Refresh to show changes
        } else {
            alert(result.error || 'Error updating ballot');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating ballot');
    });
}

// View results
function viewResults(ballotId) {
    fetch(`/admin/api/ballots/${ballotId}/results`)
        .then(response => response.json())
        .then(results => {
            const content = `
                <div class="results-container">
                    <h4>Election Results</h4>
                    <p><strong>Total Votes:</strong> ${results.total_votes}</p>
                    <div class="result-chart">
                        ${results.candidates.map(candidate => `
                            <div class="candidate-result mb-3">
                                <div class="d-flex justify-content-between">
                                    <span><strong>${candidate.name}</strong></span>
                                    <span>${candidate.votes} votes (${candidate.percentage}%)</span>
                                </div>
                                <div class="progress">
                                    <div class="progress-bar" style="width: ${candidate.percentage}%"></div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            document.getElementById('resultsContent').innerHTML = content;
            new bootstrap.Modal(document.getElementById('resultsModal')).show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading results');
        });
}

// Manage candidates
function manageCandidates(ballotId) {
    fetch(`/admin/api/ballots/${ballotId}/candidates`)
        .then(response => response.json())
        .then(candidates => {
            const content = `
                <div class="candidates-management">
                    <div class="d-flex justify-content-between mb-3">
                        <h5>Candidates</h5>
                        <button class="btn btn-success btn-sm" onclick="addCandidate(${ballotId})">
                            <i class="bi bi-plus"></i> Add Candidate
                        </button>
                    </div>
                    <div class="candidates-list">
                        ${candidates.map(candidate => `
                            <div class="candidate-item d-flex justify-content-between align-items-center p-3 border rounded mb-2">
                                <div>
                                    <strong>${candidate.name}</strong><br>
                                    <small class="text-muted">${candidate.position}</small>
                                </div>
                                <div class="btn-group btn-group-sm">
                                    <button class="btn btn-outline-primary" onclick="editCandidate(${candidate.id})">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                    <button class="btn btn-outline-danger" onclick="deleteCandidate(${candidate.id})">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            document.getElementById('candidatesContent').innerHTML = content;
            new bootstrap.Modal(document.getElementById('candidatesModal')).show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading candidates');
        });
}

// Delete ballot
function deleteBallot(ballotId, ballotTitle) {
    if (confirm(`Are you sure you want to delete the ballot "${ballotTitle}"? This action cannot be undone and will delete all associated votes.`)) {
        fetch(`/admin/api/ballots/${ballotId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                document.getElementById(`ballot-row-${ballotId}`).remove();
                alert('Ballot deleted successfully');
            } else {
                alert(result.error || 'Error deleting ballot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting ballot');
        });
    }
}

// Toggle ballot status
function toggleBallotStatus(ballotId, active) {
    fetch(`/admin/api/ballots/${ballotId}/toggle`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_active: active })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            location.reload(); // Refresh to show changes
        } else {
            alert(result.error || 'Error updating ballot status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating ballot status');
    });
}

// Duplicate ballot
function duplicateBallot(ballotId) {
    if (confirm('Create a copy of this ballot?')) {
        fetch(`/admin/api/ballots/${ballotId}/duplicate`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                location.reload(); // Refresh to show new ballot
            } else {
                alert(result.error || 'Error duplicating ballot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error duplicating ballot');
        });
    }
}

// Export results
function exportResults(ballotId) {
    window.open(`/admin/api/ballots/${ballotId}/export`, '_blank');
}

// Helper functions
function formatDateForInput(dateString) {
    const date = new Date(dateString);
    return date.toISOString().slice(0, 16);
}

// Cleanup modal backdrops
function cleanupModalBackdrops() {
    // Remove any stray modal backdrops
    const backdrops = document.querySelectorAll('.modal-backdrop');
    backdrops.forEach(backdrop => {
        if (backdrop.parentNode) {
            backdrop.parentNode.removeChild(backdrop);
        }
    });
    
    // Reset body classes
    document.body.classList.remove('modal-open');
    document.body.style.paddingRight = '';
    document.body.style.overflow = '';
}

// Candidate management functions
function addCandidate(ballotId) {
    // Clean up any existing modal issues first
    cleanupModalBackdrops();
    
    const modalHtml = `
        <div class="modal fade" id="addCandidateModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Add New Candidate</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <form id="addCandidateForm">
                        <div class="modal-body">
                            <div class="mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" class="form-control" id="candidateName" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Position</label>
                                <input type="text" class="form-control" id="candidatePosition" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Manifesto</label>
                                <textarea class="form-control" id="candidateManifesto" rows="3"></textarea>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-success">Add Candidate</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page and show it
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('addCandidateModal'));
    modal.show();
    
    // Handle form submission
    document.getElementById('addCandidateForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const data = {
            name: document.getElementById('candidateName').value,
            position: document.getElementById('candidatePosition').value,
            manifesto: document.getElementById('candidateManifesto').value
        };
        
        fetch(`/admin/api/ballots/${ballotId}/candidates`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                modal.hide();
                
                // Clean up and refresh without reopening modal
                setTimeout(() => {
                    cleanupModalBackdrops();
                    refreshCandidatesList(ballotId);
                }, 300); // Wait for modal animation
                
                alert('Candidate added successfully!');
            } else {
                alert(result.error || 'Error adding candidate');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding candidate');
        });
    });
    
    // Enhanced cleanup when modal is hidden
    document.getElementById('addCandidateModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
        cleanupModalBackdrops(); // Extra cleanup
    });
}

function editCandidate(candidateId) {
    // Implementation for editing candidates
    alert('Edit candidate functionality - to be implemented');
}

function deleteCandidate(candidateId) {
    if (confirm('Delete this candidate?')) {
        fetch(`/admin/api/candidates/${candidateId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                location.reload();
            } else {
                alert(result.error || 'Error deleting candidate');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting candidate');
        });
    }
}