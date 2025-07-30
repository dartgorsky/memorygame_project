document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.memory-card');
    const puntosSpan = document.getElementById('puntos');
    const vidasSpan = document.getElementById('vidas');
    const intentosSpan = document.getElementById('intentos');
    const timerSpan = document.getElementById('timer');

    let hasFlippedCard = false;
    let lockBoard = false;
    let firstCard, secondCard;

    let puntos = 0;
    let intentos = 0;
    let vidas = parseInt(vidasSpan.textContent);
    const totalPairs = cards.length / 2;

    let pairsFound = 0;

    // Temporizador
    let tiempoRestante = parseInt(timerSpan.textContent);
    let timerInterval;

    function mostrarModalPerdiste() {
        const modal = new bootstrap.Modal(document.getElementById('modalPerdiste'));
        modal.show();

        document.getElementById('btnVolverMenu').addEventListener('click', () => {
            window.location.href = '/menu';  // Cambia si tu URL es diferente
        });
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            tiempoRestante--;
            timerSpan.textContent = tiempoRestante;

            if (tiempoRestante <= 0) {
                clearInterval(timerInterval);
                mostrarModalPerdiste();
            }
        }, 1000);
    }

    function flipCard() {
        if (lockBoard) return;
        if (this === firstCard) return;

        this.classList.add('is-flipped');

        if (!hasFlippedCard) {
            // Primer click
            hasFlippedCard = true;
            firstCard = this;
            return;
        }

        // Segundo click
        secondCard = this;
        lockBoard = true;

        checkForMatch();
    }

    function checkForMatch() {
        intentos++;
        intentosSpan.textContent = intentos;

        const isMatch = firstCard.dataset.id === secondCard.dataset.id;

        if (isMatch) {
            // Coinciden
            puntos++;
            puntosSpan.textContent = puntos;

            pairsFound++;

            disableCards();

            if (pairsFound === totalPairs) {
                clearInterval(timerInterval);
                setTimeout(() => alert('¡Felicidades! Has ganado el juego.'), 500);
            }

            resetBoard();
        } else {
            // No coinciden
            vidas--;
            vidasSpan.textContent = vidas;

            setTimeout(() => {
                unflipCards();

                if (vidas <= 0) {
                    clearInterval(timerInterval);
                    mostrarModalPerdiste();
                }
            }, 1000);
        }
    }

    function disableCards() {
        firstCard.removeEventListener('click', flipCard);
        secondCard.removeEventListener('click', flipCard);
    }

    function unflipCards() {
        firstCard.classList.remove('is-flipped');
        secondCard.classList.remove('is-flipped');
        resetBoard();
    }

    function resetBoard() {
        [hasFlippedCard, lockBoard] = [false, false];
        [firstCard, secondCard] = [null, null];
    }

    function resetGame() {
        location.reload();
    }

    // Empezar el temporizador
    startTimer();

    // Añadir event listeners
    cards.forEach(card => card.addEventListener('click', flipCard));
});
