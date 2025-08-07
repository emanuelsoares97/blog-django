document.addEventListener('DOMContentLoaded', function() {
  const replyLinks = document.querySelectorAll('.reply-link');

  replyLinks.forEach(function(link) {
    link.addEventListener('click', function(event) {
      event.preventDefault();
      const commentId = this.getAttribute('data-comment-id');

      // Esconde todos os formulários abertos
      document.querySelectorAll('form.reply-form').forEach(form => form.classList.add('d-none'));

      // Mostra só o formulário referente a este comentário
      const form = document.querySelector(`form.reply-form[data-parent-id="${commentId}"]`);
      if (form) {
        form.classList.remove('d-none');
        form.querySelector('textarea').focus();
        // Opcional: scrolla para o formulário
        form.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });
});