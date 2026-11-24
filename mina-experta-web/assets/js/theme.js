(() => {
  const clave = 'mina-experta-tema';
  const raiz = document.documentElement;
  let preferencia;
  try {
    preferencia = localStorage.getItem(clave);
  } catch {
    // Algunos navegadores restringen el almacenamiento al abrir un archivo local.
  }
  const temaInicial = preferencia === 'oscuro' || preferencia === 'claro'
    ? preferencia
    : (matchMedia('(prefers-color-scheme: dark)').matches ? 'oscuro' : 'claro');
  raiz.dataset.tema = temaInicial;

  document.addEventListener('DOMContentLoaded', () => {
    const boton = document.getElementById('btnTheme');

    function mostrarTema(tema) {
      raiz.dataset.tema = tema;
      boton.setAttribute('aria-pressed', String(tema === 'oscuro'));
    }

    mostrarTema(temaInicial);
    boton.addEventListener('click', () => {
      const tema = raiz.dataset.tema === 'oscuro' ? 'claro' : 'oscuro';
      mostrarTema(tema);
      try {
        localStorage.setItem(clave, tema);
      } catch {
        // El selector sigue funcionando durante la sesión.
      }
    });
  });
})();