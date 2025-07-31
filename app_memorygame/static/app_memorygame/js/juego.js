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
            window.location.href = '/menu';
        });
    }

    function mostrarModalVictoria() {
        const modal = new bootstrap.Modal(document.getElementById('modalVictoria'));
        modal.show();

        document.getElementById('btnVolverMenuVictoria').addEventListener('click', () => {
            window.location.href = '/menu';
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
                setTimeout(() => mostrarModalVictoria(), 500);
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

    // Mostrar todas las cartas volteadas durante 5 segundos antes de empezar
    cards.forEach(card => {
        card.classList.add('is-flipped');
    });

    // Desactivar clics hasta que pasen los 5 segundos
    lockBoard = true;

    setTimeout(() => {
        // Voltear todas las cartas de nuevo
        cards.forEach(card => {
            card.classList.remove('is-flipped');
        });

        // Activar clics
        lockBoard = false;

        // Empezar el temporizador
        startTimer();
    }, 5000);

    // Mostrar todas las cartas volteadas al inicio durante 5 segundos
    document.addEventListener('DOMContentLoaded', () => {
        const todasLasCartas = document.querySelectorAll('.memory-card');

        // Voltea todas temporalmente
        todasLasCartas.forEach(card => card.classList.add('volteada'));

        // A los 5 segundos, las desvoltea
        setTimeout(() => {
            todasLasCartas.forEach(card => card.classList.remove('volteada'));
            // Aquí ya empieza el juego
        }, 5000);
    });


    // Añadir event listeners
    cards.forEach(card => card.addEventListener('click', flipCard));
});