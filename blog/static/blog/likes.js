document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id');
            const url = `/post/${postId}/toggle-like-ajax/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // função para pegar cookie CSRF
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.innerHTML = `❤️ (<span class="likes-count">${data.total_likes}</span>)`;
                    this.setAttribute('aria-pressed', 'true');
                    this.classList.remove('btn-outline-primary');
                    this.classList.add('btn-primary');
                } else {
                    this.innerHTML = `🤍 (<span class="likes-count">${data.total_likes}</span>)`;
                    this.setAttribute('aria-pressed', 'false');
                    this.classList.remove('btn-primary');
                    this.classList.add('btn-outline-primary');
                }
            })
            .catch(error => {
                console.error('Error ao tentar dar like:', error);
            });
        });
    });

    // Função para pegar cookie CSRF (requerida para POST)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Verifica se cookie começa com o nome
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
