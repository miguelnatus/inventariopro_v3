/**
 * InventarioPro AI Assistant
 * Funcionalidades de IA integradas ao sistema
 */

class AIAssistant {
    constructor() {
        this.baseUrl = '/api/ai/';
        this.isLoading = false;
        this.init();
    }

    init() {
        this.setupEventEnhancer();
        this.setupProductSuggestions();
        this.setupChatWidget();
        this.setupContextHelp();
    }

    // Utilitário para fazer requisições AJAX
    async makeRequest(url, data) {
        if (this.isLoading) return null;
        
        this.isLoading = true;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('Erro na requisição:', error);
            return { error: 'Erro de conexão' };
        } finally {
            this.isLoading = false;
        }
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    // 1. Assistente de Formulários de Eventos
    setupEventEnhancer() {
        const eventForms = document.querySelectorAll('form[data-ai-enhance="event"]');
        
        eventForms.forEach(form => {
            this.addEventEnhancer(form);
        });
    }

    addEventEnhancer(form) {
        const nameField = form.querySelector('input[name="nome"], input[name="title"]');
        const descField = form.querySelector('textarea[name="descricao"], textarea[name="description"]');
        
        if (!nameField || !descField) return;

        // Criar botão de IA
        const aiButton = document.createElement('button');
        aiButton.type = 'button';
        aiButton.className = 'btn btn-outline-primary btn-sm ms-2';
        aiButton.innerHTML = '<i class="bx bx-brain me-1"></i>Melhorar com IA';
        aiButton.onclick = () => this.enhanceEventDescription(nameField, descField);

        // Adicionar após o campo de descrição
        descField.parentNode.appendChild(aiButton);

        // Adicionar área de resultado
        const resultDiv = document.createElement('div');
        resultDiv.id = 'ai-enhancement-result';
        resultDiv.className = 'mt-3';
        resultDiv.style.display = 'none';
        descField.parentNode.appendChild(resultDiv);
    }

    async enhanceEventDescription(nameField, descField) {
        const draft = `${nameField.value}\n${descField.value}`;
        
        if (!draft.trim()) {
            alert('Digite pelo menos o nome ou uma descrição básica do evento.');
            return;
        }

        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bx bx-loader-alt bx-spin me-1"></i>Processando...';
        button.disabled = true;

        try {
            const result = await this.makeRequest(this.baseUrl + 'enhance-event/', {
                draft: draft
            });

            if (result.success) {
                this.showEnhancementResult(result.enhanced, nameField, descField);
            } else {
                alert('Erro: ' + (result.error || 'Não foi possível processar'));
            }
        } catch (error) {
            alert('Erro de conexão. Tente novamente.');
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    showEnhancementResult(enhanced, nameField, descField) {
        const resultDiv = document.getElementById('ai-enhancement-result');
        
        resultDiv.innerHTML = `
            <div class="card border-primary">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0"><i class="bx bx-brain me-2"></i>Sugestões da IA</h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Título Sugerido:</label>
                            <p class="border p-2 bg-light">${enhanced.titulo || 'N/A'}</p>
                            <button class="btn btn-sm btn-outline-primary" onclick="aiAssistant.applyField('${nameField.id}', '${enhanced.titulo}')">
                                Aplicar Título
                            </button>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label fw-bold">Local Sugerido:</label>
                            <p class="border p-2 bg-light">${enhanced.local_sugerido || 'N/A'}</p>
                        </div>
                    </div>
                    <div class="mt-3">
                        <label class="form-label fw-bold">Descrição Melhorada:</label>
                        <div class="border p-3 bg-light" style="max-height: 200px; overflow-y: auto;">
                            ${enhanced.descricao || 'N/A'}
                        </div>
                        <button class="btn btn-sm btn-outline-primary mt-2" onclick="aiAssistant.applyField('${descField.id}', \`${enhanced.descricao}\`)">
                            Aplicar Descrição
                        </button>
                    </div>
                    <div class="mt-3">
                        <label class="form-label fw-bold">Instruções de Acesso:</label>
                        <div class="border p-2 bg-light">
                            ${enhanced.instrucoes_acesso || 'N/A'}
                        </div>
                    </div>
                    <div class="mt-3 text-end">
                        <button class="btn btn-success me-2" onclick="aiAssistant.applyAllEnhancements('${nameField.id}', '${descField.id}', ${JSON.stringify(enhanced).replace(/"/g, '&quot;')})">
                            <i class="bx bx-check me-1"></i>Aplicar Tudo
                        </button>
                        <button class="btn btn-secondary" onclick="aiAssistant.hideEnhancementResult()">
                            Fechar
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        resultDiv.style.display = 'block';
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }

    applyField(fieldId, value) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = value;
            field.dispatchEvent(new Event('change'));
        }
    }

    applyAllEnhancements(nameFieldId, descFieldId, enhanced) {
        this.applyField(nameFieldId, enhanced.titulo);
        this.applyField(descFieldId, enhanced.descricao);
        this.hideEnhancementResult();
        
        // Mostrar notificação de sucesso
        this.showNotification('Sugestões aplicadas com sucesso!', 'success');
    }

    hideEnhancementResult() {
        const resultDiv = document.getElementById('ai-enhancement-result');
        if (resultDiv) {
            resultDiv.style.display = 'none';
        }
    }

    // 2. Sugestões de Produtos
    setupProductSuggestions() {
        const productForms = document.querySelectorAll('form[data-ai-suggest="products"]');
        
        productForms.forEach(form => {
            this.addProductSuggester(form);
        });
    }

    addProductSuggester(form) {
        // Criar campo de entrada para descrição
        const suggestDiv = document.createElement('div');
        suggestDiv.className = 'mb-3 border p-3 bg-light';
        suggestDiv.innerHTML = `
            <label class="form-label fw-bold">
                <i class="bx bx-brain me-2"></i>Assistente de Produtos
            </label>
            <div class="input-group">
                <input type="text" class="form-control" id="product-description" 
                       placeholder="Descreva o que você precisa (ex: equipamentos de som para evento)">
                <button class="btn btn-outline-primary" type="button" onclick="aiAssistant.suggestProducts()">
                    <i class="bx bx-search me-1"></i>Sugerir
                </button>
            </div>
            <div id="product-suggestions" class="mt-3" style="display: none;"></div>
        `;
        
        form.insertBefore(suggestDiv, form.firstChild);
    }

    async suggestProducts() {
        const descInput = document.getElementById('product-description');
        const description = descInput.value.trim();
        
        if (!description) {
            alert('Digite uma descrição do que você precisa.');
            return;
        }

        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bx bx-loader-alt bx-spin me-1"></i>Buscando...';
        button.disabled = true;

        try {
            const result = await this.makeRequest(this.baseUrl + 'suggest-products/', {
                description: description
            });

            if (result.success) {
                this.showProductSuggestions(result.suggestions);
            } else {
                alert('Erro: ' + (result.error || 'Não foi possível processar'));
            }
        } catch (error) {
            alert('Erro de conexão. Tente novamente.');
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    showProductSuggestions(suggestions) {
        const suggestionsDiv = document.getElementById('product-suggestions');
        
        let html = '<h6>Sugestões de Produtos:</h6>';
        
        if (suggestions.produtos && suggestions.produtos.length > 0) {
            html += '<div class="row">';
            suggestions.produtos.forEach((produto, index) => {
                html += `
                    <div class="col-md-6 mb-2">
                        <div class="card card-body">
                            <h6>${produto.nome}</h6>
                            <small class="text-muted">Categoria: ${produto.categoria}</small>
                            <small class="text-success">Preço estimado: ${produto.preco_estimado}</small>
                            <button class="btn btn-sm btn-outline-primary mt-2" 
                                    onclick="aiAssistant.addSuggestedProduct('${produto.nome}', '${produto.categoria}', '${produto.preco_estimado}')">
                                <i class="bx bx-plus me-1"></i>Adicionar
                            </button>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        if (suggestions.categorias && suggestions.categorias.length > 0) {
            html += '<h6 class="mt-3">Categorias Sugeridas:</h6>';
            html += '<div class="d-flex flex-wrap gap-2">';
            suggestions.categorias.forEach(categoria => {
                html += `<span class="badge bg-secondary">${categoria}</span>`;
            });
            html += '</div>';
        }
        
        suggestionsDiv.innerHTML = html;
        suggestionsDiv.style.display = 'block';
    }

    addSuggestedProduct(nome, categoria, preco) {
        // Preencher campos do formulário se existirem
        const nomeField = document.querySelector('input[name="nome"]');
        const categoriaField = document.querySelector('select[name="categoria"], input[name="categoria"]');
        const precoField = document.querySelector('input[name="preco"]');
        
        if (nomeField) nomeField.value = nome;
        if (categoriaField) categoriaField.value = categoria;
        if (precoField) precoField.value = preco.replace('R$ ', '').replace(',', '.');
        
        this.showNotification(`Produto "${nome}" adicionado ao formulário!`, 'success');
    }

    // 3. Widget de Chat para FAQ
    setupChatWidget() {
        this.createChatWidget();
    }

    createChatWidget() {
        const chatWidget = document.createElement('div');
        chatWidget.id = 'ai-chat-widget';
        chatWidget.className = 'ai-chat-widget';
        chatWidget.innerHTML = `
            <div class="chat-toggle" onclick="aiAssistant.toggleChat()">
                <i class="bx bx-message-dots"></i>
            </div>
            <div class="chat-window" style="display: none;">
                <div class="chat-header">
                    <h6><i class="bx bx-brain me-2"></i>Assistente IA</h6>
                    <button class="btn-close" onclick="aiAssistant.toggleChat()"></button>
                </div>
                <div class="chat-messages" id="chat-messages">
                    <div class="message assistant">
                        Olá! Sou seu assistente do InventarioPro. Como posso ajudar?
                    </div>
                </div>
                <div class="chat-input">
                    <div class="input-group">
                        <input type="text" class="form-control" id="chat-input" 
                               placeholder="Digite sua pergunta..." onkeypress="aiAssistant.handleChatKeyPress(event)">
                        <button class="btn btn-primary" onclick="aiAssistant.sendChatMessage()">
                            <i class="bx bx-send"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(chatWidget);
    }

    toggleChat() {
        const chatWindow = document.querySelector('.chat-window');
        const isVisible = chatWindow.style.display !== 'none';
        chatWindow.style.display = isVisible ? 'none' : 'block';
        
        if (!isVisible) {
            document.getElementById('chat-input').focus();
        }
    }

    handleChatKeyPress(event) {
        if (event.key === 'Enter') {
            this.sendChatMessage();
        }
    }

    async sendChatMessage() {
        const input = document.getElementById('chat-input');
        const question = input.value.trim();
        
        if (!question) return;
        
        // Adicionar mensagem do usuário
        this.addChatMessage(question, 'user');
        input.value = '';
        
        // Mostrar indicador de digitação
        this.addChatMessage('Digitando...', 'assistant', true);
        
        try {
            const result = await this.makeRequest(this.baseUrl + 'chat-faq/', {
                question: question,
                context: window.location.pathname
            });
            
            // Remover indicador de digitação
            this.removeChatTyping();
            
            if (result.success) {
                this.addChatMessage(result.answer, 'assistant');
            } else {
                this.addChatMessage('Desculpe, não consegui processar sua pergunta.', 'assistant');
            }
        } catch (error) {
            this.removeChatTyping();
            this.addChatMessage('Erro de conexão. Tente novamente.', 'assistant');
        }
    }

    addChatMessage(message, sender, isTyping = false) {
        const messagesDiv = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}${isTyping ? ' typing' : ''}`;
        messageDiv.textContent = message;
        
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    removeChatTyping() {
        const typingMessage = document.querySelector('.message.typing');
        if (typingMessage) {
            typingMessage.remove();
        }
    }

    // 4. Ajuda Contextual
    setupContextHelp() {
        this.loadContextHelp();
    }

    async loadContextHelp() {
        const page = this.getCurrentPage();
        
        try {
            const response = await fetch(`${this.baseUrl}context-help/?page=${page}`);
            const result = await response.json();
            
            if (result.success) {
                this.showContextHelp(result.help);
            }
        } catch (error) {
            console.log('Ajuda contextual não disponível');
        }
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('dashboard')) return 'dashboard';
        if (path.includes('eventos')) return 'eventos';
        if (path.includes('produtos')) return 'produtos';
        if (path.includes('propostas')) return 'propostas';
        return 'geral';
    }

    showContextHelp(help) {
        // Adicionar dica contextual discreta no topo da página
        const helpDiv = document.createElement('div');
        // helpDiv.className = 'alert alert-info alert-dismissible fade show';
        // helpDiv.innerHTML = `
        //     <i class="bx bx-info-circle me-2"></i>
        //     <strong>${help.title}:</strong> ${help.description}
        //     <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        // `;
        
        const container = document.querySelector('.container-fluid');
        if (container) {
            container.insertBefore(helpDiv, container.firstChild);
        }
    }

    // Utilitários
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.aiAssistant = new AIAssistant();
});

// CSS para o widget de chat
const chatStyles = `
.ai-chat-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;
}

.chat-toggle {
    width: 60px;
    height: 60px;
    background: var(--primary-color);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

.chat-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.chat-window {
    position: absolute;
    bottom: 70px;
    right: 0;
    width: 350px;
    height: 400px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
}

.chat-header {
    background: var(--primary-color);
    color: white;
    padding: 15px;
    border-radius: 10px 10px 0 0;
    display: flex;
    justify-content: between;
    align-items: center;
}

.chat-messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.message {
    max-width: 80%;
    padding: 10px 15px;
    border-radius: 15px;
    word-wrap: break-word;
}

.message.user {
    background: var(--primary-color);
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 5px;
}

.message.assistant {
    background: #f1f3f4;
    color: #333;
    align-self: flex-start;
    border-bottom-left-radius: 5px;
}

.message.typing {
    font-style: italic;
    opacity: 0.7;
}

.chat-input {
    padding: 15px;
    border-top: 1px solid #eee;
}

@media (max-width: 768px) {
    .chat-window {
        width: 300px;
        height: 350px;
    }
}
`;

// Adicionar estilos ao documento
const styleSheet = document.createElement('style');
styleSheet.textContent = chatStyles;
document.head.appendChild(styleSheet);

