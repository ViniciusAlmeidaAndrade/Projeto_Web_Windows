function animarElemento(elemento) {
    elemento.classList.add('animar');
    setTimeout(() => {
        elemento.classList.remove('animar');
    }, 1000); // Duração da animação
}
////////////////////////////