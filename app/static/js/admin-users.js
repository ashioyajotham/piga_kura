// Admin Users Management JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Status toggle functionality
    document.querySelectorAll('.status-toggle').forEach(badge => {
        badge.addEventListener('click', function() {
            const userId = this.dataset.userId;
            const isVerified = this.dataset.verified === 'true';
            toggleUserVerification(userId, !isVerified);
        });
    });

    // Form submissions
    document.getElementById('editUserForm').addEventListener('submit', handleEditUser);
    document.getElementById('createUserForm').addEventListener('submit', handleCreateUser);
});

// View user details
function viewUser(userId) {
    fetch(`/admin/api/users/${userId}`)
        .then(response => response.json())
        .then(user => {
            const content = `
                <div class="row">
                    <div class="col-md-6">
                        <strong>ID:</strong> ${user.id}<br>
                        <strong>Email:</strong> ${user.email}<br>
                        <strong>Voter ID:</strong> ${user.voter_id}<br>
                        <strong>Role:</strong> ${getUserRole(user)}<br>
                    </div>
                    <div class="col-md-6">
                        <strong>Status:</strong> ${user.is_verified ? 'Verified' : 'Pending'}<br>
                        <strong>Registered:</strong> ${new Date(user.created_at).toLocaleString()}<br>
                        <strong>Last Login:</strong> ${user.last_login || 'Never'}<br>
                    </div>
                </div>
                <hr>
                <div class="mt-3">
                    <h6>Voting History</h6>
                    <p class="text-muted">Total votes cast: ${user.vote_count || 0}</p>
                </div>
            `;
            document.getElementById('userDetailsContent').innerHTML = content;
            new bootstrap.Modal(document.getElementById('userDetailsModal')).show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading user details');
        });
}

// Edit user
function editUser(userId) {
    fetch(`/admin/api/users/${userId}`)
        .then(response => response.json())
        .then(user => {
            document.getElementById('editUserId').value = user.id;
            document.getElementById('editUserEmail').value = user.email;
            document.getElementById('editUserVoterId').value = user.voter_id;
            document.getElementById('editUserRole').value = getUserRoleValue(user);
            document.getElementById('editUserVerified').checked = user.is_verified;
            
            new bootstrap.Modal(document.getElementById('editUserModal')).show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading user data');
        });
}

// Handle edit user form submission
function handleEditUser(e) {
    e.preventDefault();
    
    const userId = document.getElementById('editUserId').value;
    const data = {
        voter_id: document.getElementById('editUserVoterId').value,
        role: document.getElementById('editUserRole').value,
        is_verified: document.getElementById('editUserVerified').checked
    };

    fetch(`/admin/api/users/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('editUserModal')).hide();
            location.reload(); // Refresh to show changes
        } else {
            alert(result.error || 'Error updating user');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating user');
    });
}

// Handle create user form submission
function handleCreateUser(e) {
    e.preventDefault();
    
    const data = {
        email: document.getElementById('createUserEmail').value,
        voter_id: document.getElementById('createUserVoterId').value,
        password: document.getElementById('createUserPassword').value,
        role: document.getElementById('createUserRole').value,
        is_verified: document.getElementById('createUserVerified').checked
    };

    fetch('/admin/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('createUserModal')).hide();
            location.reload(); // Refresh to show new user
        } else {
            alert(result.error || 'Error creating user');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating user');
    });
}

// Delete user
function deleteUser(userId, userEmail) {
    if (confirm(`Are you sure you want to delete user "${userEmail}"? This action cannot be undone.`)) {
        fetch(`/admin/api/users/${userId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                document.getElementById(`user-row-${userId}`).remove();
                alert('User deleted successfully');
            } else {
                alert(result.error || 'Error deleting user');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting user');
        });
    }
}

// Approve official
function approveOfficial(userId) {
    if (confirm('Approve this official account?')) {
        fetch(`/admin/api/users/${userId}/approve`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                location.reload(); // Refresh to show changes
            } else {
                alert(result.error || 'Error approving official');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error approving official');
        });
    }
}

// Toggle user verification
function toggleUserVerification(userId, verified) {
    fetch(`/admin/api/users/${userId}/verify`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ verified: verified })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            location.reload(); // Refresh to show changes
        } else {
            alert(result.error || 'Error updating verification status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating verification status');
    });
}

// Helper functions
function getUserRole(user) {
    if (user.is_admin) return 'Admin';
    if (user.is_official) return 'Official';
    return 'Voter';
}

function getUserRoleValue(user) {
    if (user.is_admin) return 'admin';
    if (user.is_official) return 'official';
    return 'voter';
}