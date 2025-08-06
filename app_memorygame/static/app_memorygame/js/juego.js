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
    const resultadoServidor = document.body.dataset.resultado;

    const btnVolverMenu = document.querySelector('a.btn.btn-outline-secondary');
    const modalConfirmarSalida = new bootstrap.Modal(document.getElementById('modalConfirmarSalida'));
    const btnConfirmarSalida = document.getElementById('btnConfirmarSalida');
    const btnCancelarSalida = document.getElementById('btnCancelarSalida');

    const audioWin = new Audio('/static/app_memorygame/sonidos/win.mp3');
    const audioLose = new Audio('/static/app_memorygame/sonidos/lose.mp3');
    const bgMusic = document.getElementById('bg-music');


    let hasFlippedCard = false;
    let lockBoard = false;
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

    if (bgMusic) {
        bgMusic.volume = 0.3;  // volumen entre 0.0 y 1.0, 0.3 es bajo
    }

    [audioWin, audioLose].forEach(a => {
        a.preload = 'auto';
        a.volume = 0.6;
        a.load();
    });

    // Función para enviar resultado
    function enviarResultado(status) {
        if (juegoTerminado) return;
        juegoTerminado = true;

        inputStatus.value = status;
        inputAttempts.value = intentos;
        inputScore.value = puntos;

        resultadoForm.submit();
    }

    // Si se hace clic en "Volver al Menú" y no ha terminado, marcar derrota
    if (btnVolverMenu) {
        btnVolverMenu.addEventListener('click', (e) => {
            e.preventDefault();
            if (!juegoTerminado) {
                modalConfirmarSalida.show();
            } else {
                window.location.href = btnVolverMenu.href;
            }
        });
    }

    btnConfirmarSalida.addEventListener('click', () => {
        modalConfirmarSalida.hide();
        enviarResultado('L');
    });

    btnCancelarSalida.addEventListener('click', () => {
        modalConfirmarSalida.hide();
    });

    function mostrarModalPerdiste() {
        if (bgMusic) {
            bgMusic.pause();
            bgMusic.currentTime = 0;
        }

        const modal = new bootstrap.Modal(document.getElementById('modalPerdiste'));
        modal.show();
        audioLose.currentTime = 0;
        audioLose.play().catch(() => { });
        document.getElementById('btnVolverMenu').addEventListener('click', () => {
            window.location.href = '/menu';
        });
    }

    function mostrarModalVictoria() {
        if (bgMusic) {
            bgMusic.pause();
            bgMusic.currentTime = 0;
        }

        const modal = new bootstrap.Modal(document.getElementById('modalVictoria'));
        modal.show();
        audioWin.currentTime = 0;
        audioWin.play().catch(() => { });
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
        if (lockBoard || this === firstCard) return;

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

    if (resultadoServidor === 'W') {
        mostrarModalVictoria();
    } else if (resultadoServidor === 'L') {
        mostrarModalPerdiste();
    } else {
        // Vista previa de 5 segundos antes de que empiece la partida
        function showPreview() {
            lockBoard = true;
            cards.forEach(card => card.classList.add('is-flipped'));
            setTimeout(() => {
                cards.forEach(card => card.classList.remove('is-flipped'));
                lockBoard = false;
                cards.forEach(card => card.addEventListener('click', flipCard));
                if (timerInterval) clearInterval(timerInterval);
                startTimer();
            }, 5000);
        }
        showPreview();
    }
});
