// Archivo de interactividad para el portal web institucional
document.addEventListener("DOMContentLoaded", function() {
    console.log("Portal Educativo - Jardín Escuela e Instituto Jesús Nazareno cargado correctamente.");

    // Opcional: Resaltar la sección actual en la navegación o agregar efectos dinámicos
    const links = document.querySelectorAll(".nav-menu a");
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.style.fontWeight = "bold";
            link.style.textDecoration = "underline";
        }
    });
});
function ampliarImagen(imagenSrc, titulo) {
    // Función base para gestionar la vista previa o modal de las imágenes institucionales
    console.log("Abriendo imagen: " + titulo + " -> Ruta: " + imagenSrc);
}