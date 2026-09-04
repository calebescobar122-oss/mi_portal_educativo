document.addEventListener("DOMContentLoaded", function() {
    console.log("Portal Educativo - Jardín Escuela e Instituto Jesús Nazareno cargado correctamente.");

    // 1. RESALTAR EL ENLACE DE NAVEGACIÓN ACTIVO
    const links = document.querySelectorAll(".nav-menu a");
    const currentUrl = window.location.pathname;

    links.forEach(link => {
        const href = link.getAttribute("href");
        if (href) {
            // Comprobación exacta o si incluye la ruta (evitando '/' global rompiendo todo)
            const isHomeMatch = (currentUrl === "/" || currentUrl === "/inicio") && (href === "/" || href === "/inicio");
            const isOtherMatch = href !== "/" && href !== "/inicio" && currentUrl.includes(href);

            if (isHomeMatch || isOtherMatch) {
                link.style.color = "var(--accent-gold)";
                link.style.borderBottom = "2px solid var(--accent-gold)";
                link.style.paddingBottom = "4px";
            }
        }
    });

    // 1.1. CONTROL DEL MENÚ MÓVIL DESPLEGABLE
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");

    if (menuToggle && navMenu) {
        menuToggle.addEventListener("click", function(e) {
            e.stopPropagation();
            navMenu.classList.toggle("open");
            navMenu.classList.toggle("show");
        });

        const menuLinks = navMenu.querySelectorAll("a");
        menuLinks.forEach(link => {
            link.addEventListener("click", function() {
                navMenu.classList.remove("open");
                navMenu.classList.remove("show");
            });
        });

        // Cerrar menú al hacer clic fuera de él
        document.addEventListener("click", function(e) {
            if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                navMenu.classList.remove("open");
                navMenu.classList.remove("show");
            }
        });
    }

    // 2. ANIMACIÓN DE APARICIÓN AL HACER SCROLL (FADE-IN)
    const observerOptions = {
        root: null,
        rootMargin: "0px",
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll(".fade-in");
    animatedElements.forEach(el => observer.observe(el));

    // 3. ACORDEÓN PARA PREGUNTAS FRECUENTES (FAQ)
    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(question => {
        question.addEventListener("click", function() {
            const faqItem = this.parentElement;
            
            document.querySelectorAll(".faq-item").forEach(item => {
                if (item !== faqItem) {
                    item.classList.remove("active");
                }
            });

            faqItem.classList.toggle("active");
        });
    });

    // 4. RESPUESTA AL ENVIAR FORMULARIO
    const contactForm = document.querySelector(".contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", function(event) {
            event.preventDefault();
            alert("¡Gracias por comunicarte con el Instituto Jesús Nazareno! Nos pondremos en contacto contigo a la brevedad.");
            contactForm.reset();
        });
    }
});

// 5. MODAL PARA AMPLIAR IMÁGENES DE GALERÍA
function ampliarImagen(imagenSrc, titulo) {
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

        modal.addEventListener("click", function() {
            modal.style.display = "none";
        });

        document.body.appendChild(modal);
    }

    document.getElementById("modalImg").src = imagenSrc;
    document.getElementById("modalCaption").innerText = titulo || "Galería Jesús Nazareno";
    modal.style.display = "flex";
}