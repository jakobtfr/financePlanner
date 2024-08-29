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

function deleteExpense(expenseId) {
    // Show confirmation dialog
    if (confirm("Are you sure you want to delete this expense entry?")) {
        // If the user confirms, make the delete request
        fetch('/delete-expense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({expenseId: expenseId})
        })
            .then(response => response.json())
            .then(data => {
                fetch('/delete-expense', {
                    method: 'POST',
                    body: JSON.stringify({expenseId: expenseId})
                }).then((_res) => {
                    window.location.href = "/"
                });
                // Handle the response
                console.log('Expense deleted successfully');
                // Optionally, refresh the page or update the UI
                // location.reload(); // Uncomment this to refresh the page
            })
            .catch(error => console.error('Error:', error));
    }
}

function updateDisplay() {
    var showCents = document.getElementById('toggleCents').checked;
    var elements = document.querySelectorAll('.money-display');

    elements.forEach(function (element) {
        var value = parseFloat(element.getAttribute('data-money'));
        element.textContent = showCents ? (Math.floor(value * 100) / 100).toFixed(2) : Math.floor(value);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    updateDisplay();  // Update display on page load
});

document.addEventListener('DOMContentLoaded', function () {
    // Select all alerts
    const alerts = document.querySelectorAll('.alert');

    // Iterate over each alert
    alerts.forEach(function (alert) {
        // Set a timeout to hide the alert after 5 seconds (5000 milliseconds)
        setTimeout(function () {
            // Use Bootstrap's 'fade' class to hide the alert
            alert.classList.remove('show');
            alert.classList.add('fade');
        }, 5000);
    });
});

function generateSankey() {
    fetch('/generate-sankey', {
        method: 'GET'

    }).then((_res) => {
    window.location.href = "/"
});
}