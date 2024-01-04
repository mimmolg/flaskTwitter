
    // Aggiungi un listener per gestire il clic sul pulsante "mi piace"
    document.addEventListener('DOMContentLoaded', function () {
        var likeButtons = document.querySelectorAll('.like-button');

        likeButtons.forEach(function (button) {
            button.addEventListener('click', function () {
                // Inverti la classe 'active' per cambiare il colore del cuore
                button.classList.toggle('active');
            });
        });
    });
