window.addEventListener('load', function() {
    const messages = document.querySelector('.messages');
    messages.scrollTop = messages.scrollHeight - messages.clientHeight;
});