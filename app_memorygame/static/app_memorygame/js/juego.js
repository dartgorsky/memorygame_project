document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.memory-card');
    const puntosSpan = document.getElementById('puntos');
    const vidasSpan = document.getElementById('vidas');
    const intentosSpan = document.getElementById('intentos');
    const timerSpan = document.getElementById('timer');

    const resultadoForm = document.getElementById('resultado-form');
    const inputStatus = document.getElementById('input-status');
    const inputAttempts = document.getElementById('input-attempts');
    const inputScore = document.getElementById('input-score');

    let hasFlippedCard = false;
    let lockBoard = false; // Inicia desbloqueado, sin preview
    let firstCard = null;
    let secondCard = null;

    let puntos = 0;
    let intentos = 0;
    let vidas = parseInt(vidasSpan.textContent);
    const totalPairs = cards.length / 2;

    let pairsFound = 0;

    let tiempoRestante = parseInt(timerSpan.textContent);
    let timerInterval;

    let juegoTerminado = false;

    function enviarResultado(status) {
        if (juegoTerminado) return;
        juegoTerminado = true;

        inputStatus.value = status;
        inputAttempts.value = intentos;
        inputScore.value = puntos;

        resultadoForm.submit();
    }

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
                enviarResultado('L');
            }
        }, 1000);
    }

    function flipCard() {
        if (lockBoard) return;
        if (this === firstCard) return;

        this.classList.add('is-flipped');

        if (!hasFlippedCard) {
            hasFlippedCard = true;
            firstCard = this;
            return;
        }

        secondCard = this;
        lockBoard = true;

        checkForMatch();
    }

    function checkForMatch() {
        intentos++;
        intentosSpan.textContent = intentos;

        const isMatch = firstCard.dataset.id === secondCard.dataset.id;

        if (isMatch) {
            puntos++;
            puntosSpan.textContent = puntos;
            pairsFound++;

            disableCards();

            resetBoard();

            if (pairsFound === totalPairs) {
                clearInterval(timerInterval);
                setTimeout(() => enviarResultado('W'), 500);
            } else {
                lockBoard = false;
            }
        } else {
            vidas--;
            vidasSpan.textContent = vidas;

            setTimeout(() => {
                firstCard.classList.remove('is-flipped');
                secondCard.classList.remove('is-flipped');

                resetBoard();

                if (vidas <= 0) {
                    clearInterval(timerInterval);
                    enviarResultado('L');
                } else {
                    lockBoard = false;
                }
            }, 1200);
        }
    }

    function disableCards() {
        firstCard.removeEventListener('click', flipCard);
        secondCard.removeEventListener('click', flipCard);
    }

    function resetBoard() {
        [hasFlippedCard, lockBoard] = [false, false];
        [firstCard, secondCard] = [null, null];
    }

    const resultadoServidor = document.body.dataset.resultado;
    if (resultadoServidor === 'W') {
        mostrarModalVictoria();
    } else if (resultadoServidor === 'L') {
        mostrarModalPerdiste();
    } else {
        // Vista previa de 5 segundos antes de que empiece la partida
        function showPreview() {
            lockBoard = true; // bloquea interacciones durante preview
            // Muestra todas las cartas
            cards.forEach(card => card.classList.add('is-flipped'));

            setTimeout(() => {
                // Oculta todas las cartas
                cards.forEach(card => card.classList.remove('is-flipped'));

                // Permite interacciones y arranca el juego
                lockBoard = false;
                cards.forEach(card => card.addEventListener('click', flipCard));

                // Asegurarse de no tener otro intervalo activo
                if (timerInterval) clearInterval(timerInterval);
                startTimer();
            }, 5000);
        }

        showPreview();
    }

});
