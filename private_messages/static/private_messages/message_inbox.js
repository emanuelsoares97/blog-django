document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('message-form');
    const container = document.getElementById('messages-container');
    const currentUser = container.dataset.currentUser.toLowerCase();

    let lastTimestamp = null;

    const scrollToBottom = () => {
        container.scrollTop = container.scrollHeight;
    };

    // Inicializa o timestamp com a última msg visível
    const atualizarUltimoTimestamp = () => {
        const lastMsg = container.querySelector('small:last-of-type');
        if (lastMsg) {
            // Para compatibilidade, gravar formato ISO
            lastTimestamp = new Date(lastMsg.getAttribute('data-iso')).toISOString();
        }
    };

    // ⬇️ Função para enviar mensagem
    const enviarMensagem = () => {
        const formData = new FormData(form);
        fetch("", {
            method: "POST",
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(res => res.json())
        .then(data => {
            addMessage(data);
            form.reset();
            scrollToBottom();
            lastTimestamp = data.timestamp; // atualizar último horário
        });
    };

    // ⬇️ Função para adicionar msg no chat
    const addMessage = (data) => {
        const alignClass = (data.sender.toLowerCase() === currentUser) ? "text-end" : "";
        container.innerHTML += `
            <div class="mb-2 ${alignClass}" style="text-align: right;">
                <strong>${data.sender}</strong><br>
                ${data.content.replace(/\n/g, "<br>")}<br>
                <small data-iso="${data.timestamp}">
                    ${new Date(data.timestamp).toLocaleString('pt-PT')}
                </small>
            </div>
        `;
    };


    // Handlers de envio
    form.addEventListener('submit', e => {
        e.preventDefault();
        enviarMensagem();
    });

    form.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            enviarMensagem();
        }
    });

    // Ao abrir a página
    scrollToBottom();
    atualizarUltimoTimestamp();

});
