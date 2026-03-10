'use strict';

const Chatbot = {
    history: [],
    isOpen: false,
    isAuthenticated: false,
    username: null,
    loadingElement: null,

    // -----------------------------------------------------------------------
    // Inicialización
    // -----------------------------------------------------------------------

    init() {
        this.cacheDOM();

        // Salir silenciosamente si el chatbot no está en la página
        if (!this.chatbotContainer) return;

        this.checkAuth();
        this.bindEvents();
    },

    cacheDOM() {
        this.toggleBtn        = document.getElementById('chatbot-toggle-btn');
        this.chatbotContainer = document.getElementById('chatbot-container');
        this.closeBtn         = document.getElementById('chatbot-close');
        this.messagesEl       = document.getElementById('chatbot-messages');
        this.inputEl          = document.getElementById('chatbot-input');
        this.sendBtn          = document.getElementById('chatbot-send');
    },

    checkAuth() {
        this.isAuthenticated = document.body.dataset.authenticated === 'true';
        this.username        = document.body.dataset.username || null;
    },

    bindEvents() {
        this.toggleBtn?.addEventListener('click',   () => this.toggle());
        this.closeBtn?.addEventListener('click',    () => this.close());
        this.sendBtn?.addEventListener('click',     () => this.sendMessage());
        this.inputEl?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) this.sendMessage();
        });
    },

    // -----------------------------------------------------------------------
    // Visibilidad
    // -----------------------------------------------------------------------

    toggle() {
        this.isOpen ? this.close() : this.open();
    },

    open() {
        this.isOpen = true;
        this.chatbotContainer.classList.add('active');
        this.inputEl?.focus();

        if (this.history.length === 0) {
            this.addBotMessage('¡Hola! Soy tu Asistente Cultural 🌍\n¿En qué puedo ayudarte hoy?\n\nEscribe *ayuda* para ver todo lo que puedo hacer.');
        }
    },

    close() {
        this.isOpen = false;
        this.chatbotContainer.classList.remove('active');
    },

    // -----------------------------------------------------------------------
    // Mensajes
    // -----------------------------------------------------------------------

    addMessage(role, text, type = 'text') {
        const isUser = role === 'user';

        const wrapper = document.createElement('div');
        wrapper.className = `chatbot-message ${isUser ? 'user-message' : 'bot-message'}`;

        const avatar = document.createElement('div');
        avatar.className   = 'chatbot-avatar';
        avatar.textContent = isUser ? '👤' : '🤖';

        const bubble = document.createElement('div');
        bubble.className = 'chatbot-content';

        if (type === 'loading') {
            bubble.innerHTML = '<div class="chatbot-loading-dots"><span></span><span></span><span></span></div>';
        } else {
            bubble.innerHTML = this.formatText(text);
        }

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);
        this.messagesEl.appendChild(wrapper);
        this.messagesEl.scrollTop = this.messagesEl.scrollHeight;

        return wrapper;
    },

    addBotMessage(text, type = 'text') {
        return this.addMessage('bot', text, type);
    },

    formatText(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // **negrita**
            .replace(/\*(.*?)\*/g,     '<em>$1</em>')           // *cursiva*
            .replace(/\n/g,            '<br>');                  // saltos de línea
    },

    // -----------------------------------------------------------------------
    // Loading indicator  (usa loadingElement, nunca sobreescribe cacheDOM)
    // -----------------------------------------------------------------------

    showLoading() {
        this.loadingElement = this.addBotMessage('', 'loading');
        this._setSendState(true);
    },

    hideLoading() {
        this.loadingElement?.remove();
        this.loadingElement = null;
        this._setSendState(false);
    },

    _setSendState(disabled) {
        if (!this.sendBtn) return;
        this.sendBtn.disabled      = disabled;
        this.sendBtn.style.opacity = disabled ? '0.6' : '1';
        this.sendBtn.style.cursor  = disabled ? 'not-allowed' : 'pointer';
    },

    // -----------------------------------------------------------------------
    // Envío al backend
    // -----------------------------------------------------------------------

    async sendMessage() {
        const text = this.inputEl?.value.trim();
        if (!text) return;

        this.inputEl.value = '';
        this.addMessage('user', text);
        this.history.push({ role: 'user', content: text });

        this.showLoading();

        try {
            const response = await fetch('/assistant/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({ message: text, history: this.history }),
            });

            // ── Verificar que Django respondió OK ──
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            // ── Verificar que es JSON y no una página de error Django ──
            const contentType = response.headers.get('content-type') || '';
            if (!contentType.includes('application/json')) {
                throw new Error(
                    'El servidor devolvió HTML en vez de JSON. ' +
                    'Verifica que /assistant/api/chatbot/ esté en urls.py y apunte a ChatbotCulturalView.'
                );
            }

            const data = await response.json();
            this.hideLoading();

            if (data.error) {
                this.addBotMessage(`⚠️ ${data.error}`);
            } else {
                this.addBotMessage(data.message, data.type);
                this.history.push({ role: 'assistant', content: data.message });

                if (data.pais_id) {
                    this.onPaisDetected(data);
                }
            }

        } catch (error) {
            this.hideLoading();
            console.error('[Chatbot]', error);

            const msg = error.message || '';
            if (msg.includes('Failed to fetch') || msg.includes('NetworkError')) {
                this.addBotMessage('❌ Sin conexión al servidor. Verifica que Django esté corriendo.');
            } else if (msg.includes('HTML en vez de JSON')) {
                this.addBotMessage(`❌ ${error.message}`);
            } else {
                this.addBotMessage(`❌ Error inesperado: ${msg}`);
            }
        }
    },

    // -----------------------------------------------------------------------
    // Hook país detectado
    // -----------------------------------------------------------------------

    onPaisDetected(data) {
        // Extensión futura: enlace al detalle del país, mapa, etc.
        console.log('[Chatbot] País:', data.pais, '| ID:', data.pais_id);
    },

    // -----------------------------------------------------------------------
    // Favoritos
    // -----------------------------------------------------------------------

    async saveFavorite(tipId) {
        if (!this.isAuthenticated) {
            this.addBotMessage('⚠️ Debes iniciar sesión para guardar favoritos.');
            return;
        }
        await this._favoritoRequest('/assistant/api/chatbot/favorito/guardar/', tipId);
    },

    async removeFavorite(tipId) {
        if (!this.isAuthenticated) {
            this.addBotMessage('⚠️ Debes iniciar sesión para quitar favoritos.');
            return;
        }
        await this._favoritoRequest('/assistant/api/chatbot/favorito/quitar/', tipId);
    },

    async _favoritoRequest(url, tipId) {
        try {
            const res  = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({ tip_id: tipId }),
            });
            const data = await res.json();
            if (data.message) this.addBotMessage(data.message);
        } catch (err) {
            console.error('[Chatbot] Favorito error:', err);
            this.addBotMessage('❌ No se pudo completar la acción. Intenta de nuevo.');
        }
    },

    // -----------------------------------------------------------------------
    // Búsqueda directa (útil para autocompletado externo)
    // -----------------------------------------------------------------------

    async search(query, tipo = 'pais') {
        try {
            const url  = `/assistant/api/chatbot/buscar/?q=${encodeURIComponent(query)}&tipo=${tipo}`;
            const res  = await fetch(url);
            const data = await res.json();
            return data.results || [];
        } catch (err) {
            console.error('[Chatbot] Search error:', err);
            return [];
        }
    },

    // -----------------------------------------------------------------------
    // CSRF — lee la cookie que Django ya pone en el navegador
    // -----------------------------------------------------------------------

    getCsrfToken() {
        const match = document.cookie
            .split(';')
            .map(c => c.trim())
            .find(c => c.startsWith('csrftoken='));
        return match ? decodeURIComponent(match.split('=')[1]) : '';
    },
};

// -----------------------------------------------------------------------
// Bootstrap
// -----------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => Chatbot.init());