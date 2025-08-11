document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('message-form');
    const container = document.getElementById('messages-container');

    // Função para manter o scroll no final
    const scrollToBottom = () => {
        container.scrollTop = container.scrollHeight;
    };

    // Scroll inicial ao carregar a página
    scrollToBottom();

    // Intercepta o submit
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch("", {
            method: "POST",
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            // Adiciona a nova mensagem ao container
            container.innerHTML += `
                <div class="mb-2 text-end">
                    <strong>${data.sender}</strong><br>
                    ${data.content.replace(/\n/g, "<br>")}<br>
                    <small>${data.timestamp}</small>
                </div>
            `;
            form.reset(); // limpa o campo
            scrollToBottom(); // mantém no fim
        });
    });
});

