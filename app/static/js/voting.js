document.addEventListener('DOMContentLoaded', function() {
    const votingForm = document.getElementById('voting-form');
    
    votingForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const selectedCandidate = document.querySelector('input[name="candidate"]:checked');
        if (!selectedCandidate) {
            alert('Please select a candidate');
            return;
        }
        
        // Show voting in progress
        const submitButton = document.querySelector('.vote-button');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = 'Submitting vote...';
        submitButton.disabled = true;
        
        try {
            console.log('Submitting vote for candidate:', selectedCandidate.value);
            console.log('Ballot ID:', window.ballotId);
            
            const response = await fetch('/api/voter/vote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content
                },
                body: JSON.stringify({
                    candidate_id: parseInt(selectedCandidate.value),
                    ballot_id: parseInt(window.ballotId)
                })
            });
            
            const data = await response.json();
            console.log('Server response:', data);
            
            if (response.ok) {
                window.location.href = '/voter/vote/success?vote_id=' + data.vote_id;
            } else {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
                alert(data.error || 'Error casting vote');
            }
        } catch (error) {
            console.error('Error:', error);
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            alert('Error submitting vote: ' + error.message);
        }
    });
});
