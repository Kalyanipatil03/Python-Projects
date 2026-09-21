// static/js/main.js
async function toggleWatchlist(movieId, buttonElement) {
    try {
        const response = await fetch(`/toggle-watchlist/${movieId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        const data = await response.json();
        if (data.success) {
            const icon = buttonElement.querySelector('i');
            if (data.added) {
                buttonElement.classList.add('bg-red-600');
                icon.className = 'fa-solid fa-check';
            } else {
                buttonElement.classList.remove('bg-red-600');
                icon.className = 'fa-solid fa-plus';
            }
        }
    } catch (error) {
        console.error('Error toggling watchlist:', error);
    }
}