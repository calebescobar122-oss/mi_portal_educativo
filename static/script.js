// Archivo de interactividad para el portal web institucional
document.addEventListener("DOMContentLoaded", function() {
    console.log("Portal Educativo - Jardín Escuela e Instituto Jesús Nazareno cargado correctamente.");

    // ==========================================================
    // 1. RESALTAR EL ENLACE DE NAVEGACIÓN ACTIVO
    // ==========================================================
    const links = document.querySelectorAll(".nav-menu a");
    const currentUrl = window.location.pathname;

    links.forEach(link => {
        // Compara la ruta de la página actual con el enlace del menú
        if (link.getAttribute("href") && currentUrl.includes(link.getAttribute("href"))) {
            link.style.color = "var(--accent-gold)";
            link.style.borderBottom = "2px solid var(--accent-gold)";
            link.style.paddingBottom = "4px";
        }
    });

    // ==========================================================
    // 2. ANIMACIÓN DE APARICIÓN AL HACER SCROLL (FADE-IN)
    // ==========================================================
    const observerOptions = {
        root: null,
        rootMargin: "0px",
        threshold: 0.15 // Se activa cuando el 15% del elemento ingresa a la pantalla
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target); // Se ejecuta una sola vez por elemento
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll(".fade-in");
    animatedElements.forEach(el => observer.observe(el));

    // ==========================================================
    // 3. ACORDEÓN DESPLEGABLE PARA PREGUNTAS FRECUENTES (FAQ)
    // ==========================================================
    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(question => {
        question.addEventListener("click", function() {
            const faqItem = this.parentElement;
            
            // Cierra los demás acordeones abiertos (Opcional, para mantenerlo limpio)
            document.querySelectorAll(".faq-item").forEach(item => {
                if (item !== faqItem) {
                    item.classList.remove("active");
                }
            });

            // Alterna el estado del seleccionado
            faqItem.classList.toggle("active");
        });
    });

    // ==========================================================
    // 4. BOTÓN FLOTANTE DE WHATSAPP DINÁMICO
    // ==========================================================
    if (!document.querySelector(".whatsapp-float")) {
        const waButton = document.createElement("a");
        waButton.href = "https://wa.me/50431913765";
        waButton.target = "_blank";
        waButton.className = "whatsapp-float";
        waButton.title = "Escríbenos por WhatsApp";
        waButton.innerHTML = "💬";
        document.body.appendChild(waButton);
    }

    // ==========================================================
    // 5. RESPUESTA AL ENVIAR EL FORMULARIO DE CONTACTO
    // ==========================================================
    const contactForm = document.querySelector(".contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Evita el recargado inmediato de la página
            
            // Simulación de envío exitoso
            alert("¡Gracias por comunicarte con el Instituto Jesús Nazareno! Nos pondremos en contacto contigo a la brevedad.");
            contactForm.reset();
        });
    }
});

// ==========================================================
// 6. MODAL / LIGHTBOX PARA AMPLIAR IMÁGENES DE GALERÍA
// ==========================================================
function ampliarImagen(imagenSrc, titulo) {
    console.log("Abriendo imagen: " + titulo + " -> Ruta: " + imagenSrc);

    // Revisa si ya existe un modal activo para no duplicar
    let modal = document.getElementById("imageModal");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "imageModal";
        modal.style.position = "fixed";
        modal.style.top = "0";
        modal.style.left = "0";
        modal.style.width = "100%";
        modal.style.height = "100%";
        modal.style.backgroundColor = "rgba(0,0,0,0.85)";
        modal.style.zIndex = "2000";
        modal.style.display = "flex";
        modal.style.flexDirection = "column";
        modal.style.alignItems = "center";
        modal.style.justifyContent = "center";
        modal.style.cursor = "pointer";

        modal.innerHTML = `
            <div style="position: relative; max-width: 85%; max-height: 85%; text-align: center;">
                <img id="modalImg" src="" alt="" style="max-width: 100%; max-height: 75vh; border-radius: 8px; border: 3px solid var(--accent-gold); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <p id="modalCaption" style="color: #fff; font-size: 1.1rem; margin-top: 1rem; font-weight: 600;"></p>
                <span style="position: absolute; top: -30px; right: -10px; color: #fff; font-size: 2rem; font-weight: bold; cursor: pointer;">&times;</span>
            </div>
        `;

        // Cerrar al hacer clic sobre el fondo o la X
        modal.addEventListener("click", function() {
            modal.style.display = "none";
        });

        document.body.appendChild(modal);
    }

    // Insertar datos y mostrar
    document.getElementById("modalImg").src = imagenSrc;
    document.getElementById("modalCaption").innerText = titulo || "Galería Jesús Nazareno";
    modal.style.display = "flex";
}