document.addEventListener("DOMContentLoaded", function() {

    const weeksInput = document.getElementById('weeksInput');
    const totalPriceSpan = document.getElementById('totalPrice');

    if (weeksInput && totalPriceSpan) {
        const weeklyPrice = parseFloat(weeksInput.dataset.weeklyPrice);
        weeksInput.addEventListener('input', function() {
            const weeks = parseInt(this.value) || 0;
            totalPriceSpan.innerText = (weeks * weeklyPrice).toFixed(2);
        });
    }

    const favoriteForm = document.getElementById('favoriteForm');

    if (favoriteForm) {
        favoriteForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const url = this.action;
            const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
            const btn = document.getElementById('favoriteBtn');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    if (data.is_favorited) {
                        btn.innerHTML = 'Remove from Favorites ♥';
                    } else {
                        btn.innerHTML = 'Save to Favorites ♡';
                    }
                }
            })
            .catch(error => console.error('Error in AJAX request:', error));
        });
    }

});