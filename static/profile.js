
    document.addEventListener('DOMContentLoaded', function () {
        // Imposta un timeout per nascondere l'elemento dopo un certo periodo
        setTimeout(function () {
            var notifyElement = document.querySelector('.notify');
            if (notifyElement) {
                notifyElement.style.display = 'none';
            }
        }, 1000); // Imposta il tempo in millisecondi (5 secondi nel caso di questo esempio)
    });
