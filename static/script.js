document.addEventListener("DOMContentLoaded", () => {
    // Menú desplegable para dispositivos móviles
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");

    if (menuToggle && navMenu) {
        menuToggle.addEventListener("click", () => {
            navMenu.classList.toggle("active");
        });
    }

    // Funcionalidad de Acordeón para Preguntas Frecuentes (FAQ) u otras secciones interactivas
    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(question => {
        question.addEventListener("click", () => {
            const answer = question.nextElementSibling;
            const icon = question.querySelector(".faq-icon");

            // Cerrar otras respuestas abiertas
            faqQuestions.forEach(item => {
                if (item !== question) {
                    item.nextElementSibling.style.maxHeight = null;
                    const otherIcon = item.querySelector(".faq-icon");
                    if (otherIcon) otherIcon.textContent = "+";
                }
            });

            if (answer.style.maxHeight) {
                answer.style.maxHeight = null;
                if (icon) icon.textContent = "+";
            } else {
                answer.style.maxHeight = answer.scrollHeight + "px";
                if (icon) icon.textContent = "-";
            }
        });
    });
});