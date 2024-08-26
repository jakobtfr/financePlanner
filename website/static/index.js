function deleteIncome(incomeId) {
    // Show confirmation dialog
    if (confirm("Are you sure you want to delete this income entry?")) {
        // If the user confirms, make the delete request
        fetch('/delete-income', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({incomeId: incomeId})
        })
            .then(response => response.json())
            .then(data => {
                fetch('/delete-income', {
                    method: 'POST',
                    body: JSON.stringify({incomeId: incomeId})
                }).then((_res) => {
                    window.location.href = "/"
                });
                // Handle the response
                console.log('Income deleted successfully');
                // Optionally, refresh the page or update the UI
                // location.reload(); // Uncomment this to refresh the page
            })
            .catch(error => console.error('Error:', error));
    }
}