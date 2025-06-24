// Funcionalidades JavaScript para o site Vou Livre

document.addEventListener('DOMContentLoaded', function() {
    // Menu mobile
    const hamburger = document.querySelector('.hamburger');
    const navList = document.querySelector('.nav-list');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navList.classList.toggle('show');
        });
    }
    
    // Slider automático para o banner principal (se existir)
    const heroSlider = document.querySelector('.hero-slider');
    if (heroSlider) {
        let currentSlide = 0;
        const slides = heroSlider.querySelectorAll('.hero-slide');
        const totalSlides = slides.length;
        
        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.style.display = i === index ? 'block' : 'none';
            });
        }
        
        function nextSlide() {
            currentSlide = (currentSlide + 1) % totalSlides;
            showSlide(currentSlide);
        }
        
        // Iniciar com o primeiro slide
        showSlide(0);
        
        // Mudar slide a cada 5 segundos
        setInterval(nextSlide, 5000);
    }
    
    // Validação de formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let valid = true;
            
            // Validar campos obrigatórios
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            // Validar email se existir
            const emailField = form.querySelector('input[type="email"]');
            if (emailField && emailField.value) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    valid = false;
                    emailField.classList.add('error');
                }
            }
            
            if (!valid) {
                event.preventDefault();
                alert('Por favor, preencha todos os campos obrigatórios corretamente.');
            }
        });
    });
    
    // Funcionalidade de busca
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const destination = searchForm.querySelector('input[placeholder="Para onde você quer ir?"]').value;
            const startDate = searchForm.querySelector('input[type="date"]:nth-of-type(1)').value;
            const endDate = searchForm.querySelector('input[type="date"]:nth-of-type(2)').value;
            const tripType = searchForm.querySelector('select').value;
            
            // Aqui você pode implementar a lógica de busca ou redirecionar para uma página de resultados
            window.location.href = `/roteiros?destino=${destination}&inicio=${startDate}&fim=${endDate}&tipo=${tripType}`;
        });
    }
    
    // Animação de scroll suave para links internos
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Lazy loading para imagens
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    
                    observer.unobserve(img);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            imgObserver.observe(img);
        });
    }
    
    // Contador de itens no carrinho (simulado)
    function updateCartCount() {
        const cartIcon = document.querySelector('.nav-icon .fa-shopping-cart');
        if (cartIcon) {
            // Aqui você pode obter o número real de itens do carrinho do backend
            // Por enquanto, vamos simular com um número aleatório entre 0 e 5
            const cartCount = localStorage.getItem('cartCount') || 0;
            
            if (cartCount > 0) {
                // Criar ou atualizar o badge
                let badge = cartIcon.nextElementSibling;
                if (!badge || !badge.classList.contains('cart-badge')) {
                    badge = document.createElement('span');
                    badge.classList.add('cart-badge');
                    cartIcon.parentNode.appendChild(badge);
                }
                badge.textContent = cartCount;
            }
        }
    }
    
    // Simular adição ao carrinho
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Incrementar contador do carrinho
            const currentCount = parseInt(localStorage.getItem('cartCount') || 0);
            localStorage.setItem('cartCount', currentCount + 1);
            
            // Atualizar visual
            updateCartCount();
            
            // Feedback ao usuário
            alert('Item adicionado ao carrinho!');
        });
    });
    
    // Inicializar contador do carrinho
    updateCartCount();
    
    // Newsletter signup (simulado)
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                // Aqui você enviaria o email para o backend
                // Por enquanto, vamos apenas simular sucesso
                alert('Obrigado por se inscrever em nossa newsletter!');
                emailInput.value = '';
            } else {
                alert('Por favor, insira um email válido.');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const currentLang = document.querySelector('.current-lang');
    const langDropdown = document.querySelector('.lang-dropdown');
    const languageSelector = document.querySelector('.language-selector'); // Referência ao container pai

    if (currentLang && langDropdown && languageSelector) {
        currentLang.addEventListener('click', function(event) {
            event.stopPropagation(); // Impede que o clique se propague e feche o dropdown imediatamente
            langDropdown.classList.toggle('show'); // Alterna a classe 'show'
        });

        // Fecha o dropdown se o usuário clicar em qualquer lugar fora do seletor de idioma
        document.addEventListener('click', function(event) {
            if (!languageSelector.contains(event.target)) {
                langDropdown.classList.remove('show');
            }
        });
    }

    // Você também pode adicionar lógica para o hamburger menu aqui, se ainda não tiver
    const hamburger = document.querySelector('.hamburger');
    const navList = document.querySelector('.nav-list'); // Assumindo que sua lista de navegação é .nav-list

    if (hamburger && navList) {
        hamburger.addEventListener('click', function() {
            navList.classList.toggle('active'); // Use uma classe 'active' para mostrar/esconder a nav-list no mobile
        });
    }
});
