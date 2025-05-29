/* Script para funcionalidades responsivas e multilíngue */

document.addEventListener('DOMContentLoaded', function() {
    // Menu mobile toggle
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
    const mobileMenuClose = document.querySelector('.mobile-menu-close');
    
    if (hamburger && mobileMenu && mobileMenuOverlay && mobileMenuClose) {
        hamburger.addEventListener('click', function() {
            mobileMenu.classList.add('active');
            mobileMenuOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        
        function closeMenu() {
            mobileMenu.classList.remove('active');
            mobileMenuOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
        
        mobileMenuClose.addEventListener('click', closeMenu);
        mobileMenuOverlay.addEventListener('click', closeMenu);
    }
    
    // Detecção de idioma e redirecionamento
    function detectLanguage() {
        const userLang = navigator.language || navigator.userLanguage;
        const lang = userLang.split('-')[0];
        
        // Verificar se o idioma é suportado
        if (['pt', 'en', 'es'].includes(lang)) {
            return lang;
        }
        
        return 'pt'; // Idioma padrão
    }
    
    // Animações de entrada
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animateElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        animateElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    // Validação de formulários
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                
                // Mostrar mensagem de erro
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.textContent = 'Por favor, preencha todos os campos obrigatórios.';
                
                // Remover mensagem anterior se existir
                const existingError = form.querySelector('.error-message');
                if (existingError) {
                    existingError.remove();
                }
                
                form.appendChild(errorMessage);
            }
        });
    });
    
    // Funcionalidade de busca
    const searchForm = document.querySelector('.search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const destination = searchForm.querySelector('input[type="text"]').value;
            const startDate = searchForm.querySelectorAll('input')[1].value;
            const endDate = searchForm.querySelectorAll('input')[2].value;
            const tripType = searchForm.querySelector('select').value;
            
            // Redirecionar para a página de resultados com os parâmetros
            const currentLang = document.documentElement.lang || 'pt';
            window.location.href = `/${currentLang}/roteiros?destino=${encodeURIComponent(destination)}&data_ida=${encodeURIComponent(startDate)}&data_volta=${encodeURIComponent(endDate)}&tipo=${encodeURIComponent(tripType)}`;
        });
    }
    
    // Funcionalidade de filtros de roteiros
    const filtersForm = document.querySelector('.filters-form');
    
    if (filtersForm) {
        filtersForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Coletar todos os filtros selecionados
            const destinos = Array.from(filtersForm.querySelectorAll('input[name="destino"]:checked')).map(input => input.value);
            const duracoes = Array.from(filtersForm.querySelectorAll('input[name="duracao"]:checked')).map(input => input.value);
            const tipos = Array.from(filtersForm.querySelectorAll('input[name="tipo"]:checked')).map(input => input.value);
            const avaliacao = filtersForm.querySelector('input[name="avaliacao"]:checked')?.value;
            const preco = filtersForm.querySelector('#priceRange').value;
            
            // Aplicar filtros (simulação - em produção, isso seria feito via AJAX ou recarregamento da página)
            console.log('Filtros aplicados:', { destinos, duracoes, tipos, avaliacao, preco });
            
            // Mostrar mensagem de sucesso
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.textContent = 'Filtros aplicados com sucesso!';
            
            // Remover mensagem anterior se existir
            const existingMessage = document.querySelector('.success-message');
            if (existingMessage) {
                existingMessage.remove();
            }
            
            filtersForm.appendChild(successMessage);
            
            // Remover a mensagem após 3 segundos
            setTimeout(() => {
                successMessage.remove();
            }, 3000);
        });
        
        // Reset de filtros
        const resetButton = filtersForm.querySelector('button[type="reset"]');
        if (resetButton) {
            resetButton.addEventListener('click', function() {
                // Resetar o range de preço
                const priceRange = filtersForm.querySelector('#priceRange');
                const priceValue = document.getElementById('priceValue');
                
                if (priceRange && priceValue) {
                    priceRange.value = 200;
                    priceValue.textContent = 'R$ 200';
                }
                
                // Resetar radio buttons
                const radioDefault = filtersForm.querySelector('input[name="avaliacao"][value="todos"]');
                if (radioDefault) {
                    radioDefault.checked = true;
                }
            });
        }
    }
    
    // Funcionalidade de ordenação
    const sortSelect = document.getElementById('sort');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortValue = this.value;
            console.log('Ordenando por:', sortValue);
            
            // Simulação de ordenação - em produção, isso seria feito via AJAX ou recarregamento da página
            const roteirosGrid = document.querySelector('.roteiros-grid');
            
            if (roteirosGrid) {
                // Adicionar classe de animação
                roteirosGrid.classList.add('fade-in');
                
                // Remover a classe após a animação
                setTimeout(() => {
                    roteirosGrid.classList.remove('fade-in');
                }, 500);
            }
        });
    }
    
    // Funcionalidade de newsletter
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('input[type="email"]').value;
            
            if (email && email.includes('@')) {
                // Simulação de inscrição - em produção, isso seria enviado para o servidor
                console.log('Email inscrito:', email);
                
                // Limpar o campo
                this.querySelector('input[type="email"]').value = '';
                
                // Mostrar mensagem de sucesso
                const currentLang = document.documentElement.lang || 'pt';
                const successMessages = {
                    'pt': 'Inscrição realizada com sucesso!',
                    'en': 'Subscription successful!',
                    'es': '¡Suscripción exitosa!'
                };
                
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.textContent = successMessages[currentLang];
                
                // Remover mensagem anterior se existir
                const existingMessage = newsletterForm.querySelector('.success-message');
                if (existingMessage) {
                    existingMessage.remove();
                }
                
                newsletterForm.appendChild(successMessage);
                
                // Remover a mensagem após 3 segundos
                setTimeout(() => {
                    successMessage.remove();
                }, 3000);
            }
        });
    }
    
    // Funcionalidade de botões premium
    const premiumButtons = document.querySelectorAll('.premium-button');
    
    premiumButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentLang = document.documentElement.lang || 'pt';
            window.location.href = `/${currentLang}/planos`;
        });
    });
    
    // Inicialização de elementos interativos
    function initInteractiveElements() {
        // Range slider para preço
        const priceRange = document.getElementById('priceRange');
        const priceValue = document.getElementById('priceValue');
        
        if (priceRange && priceValue) {
            priceRange.addEventListener('input', function() {
                priceValue.textContent = `R$ ${this.value}`;
            });
        }
    }
    
    initInteractiveElements();
});
