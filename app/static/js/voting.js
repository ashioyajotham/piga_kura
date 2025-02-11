document.addEventListener('DOMContentLoaded', function() {
    const votingForm = document.getElementById('voting-form');
    
    votingForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const selectedCandidate = document.querySelector('input[name="candidate"]:checked');
        if (!selectedCandidate) {
            alert('Please select a candidate');
            return;
        }
        
        try {
            const response = await fetch('/api/vote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    candidate_id: selectedCandidate.value,
                    ballot_id: window.ballotId
                })
            });
            
            if (response.ok) {
                window.location.href = '/vote/success';
            } else {
                const data = await response.json();
                alert(data.error || 'Error casting vote');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error submitting vote');
        }
    });
});
