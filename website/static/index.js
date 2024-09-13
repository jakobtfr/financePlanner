function deleteIncome(incomeId) {
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
            .then((_res) => {
                    window.location.href = "/"
                    console.log('Income deleted successfully');
                }
            )
            .catch(error => console.error('Error:', error));
    }
}

function deleteExpense(expenseId) {
    if (confirm("Are you sure you want to delete this expense entry?")) {
        fetch('/delete-expense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({expenseId: expenseId})
        })
            .then(response => response.json())
            .then((_res) => {
                    window.location.href = "/"
                    console.log('Expense deleted successfully');
                }
            )
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


function generateSankey() {
    fetch('/generate-sankey', {
        method: 'GET'

    }).then((_res) => {
        window.location.href = "/"
    });
}

function delete_account() {
    if (confirm("Are you sure you want to delete this account? This cannot be undone.")) {
        fetch('/delete_account', {
            method: 'DELETE'
        }).then((_res) => {
            window.location.href = "/login"
        });
    }
}

window.setTimeout(function () {
    $(".alert").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}, 4000);

function setContribution(value) {
    document.getElementById("contribution").value = value;
}

