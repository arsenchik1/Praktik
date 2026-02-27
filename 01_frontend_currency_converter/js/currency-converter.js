// Конвертер валют - Frontend приложение

class CurrencyConverter {
    constructor() {
        this.apiUrl = 'https://api.exchangerate-api.com/v4/latest/';
        this.currencies = [];
        this.rates = {};
        this.baseCurrency = 'USD';
        this.lastUpdate = null;
        
        this.init();
    }

    async init() {
        // Загружаем валюты
        await this.loadCurrencies();
        
        // Инициализируем DOM элементы
        this.initElements();
        
        // Загружаем курсы
        await this.loadRates();
        
        // Настраиваем обработчики событий
        this.initEventListeners();
        
        // Определяем базовую валюту пользователя
        this.detectUserCurrency();
    }

    initElements() {
        this.converterPage = document.getElementById('converter-page');
        this.ratesPage = document.getElementById('rates-page');
        this.navBtns = document.querySelectorAll('.nav-btn');
        this.fromSelect = document.getElementById('from-currency');
        this.toSelect = document.getElementById('to-currency');
        this.baseSelect = document.getElementById('base-currency');
        this.amountInput = document.getElementById('amount');
        this.textInput = document.getElementById('text-input');
        this.convertBtn = document.getElementById('convert-btn');
        this.swapBtn = document.getElementById('swap-currencies');
        this.resultBox = document.getElementById('result');
        this.ratesTable = document.getElementById('rates-table');
        this.lastUpdateEl = document.getElementById('last-update');
    }

    initEventListeners() {
        // Навигация
        this.navBtns.forEach(btn => {
            btn.addEventListener('click', () => this.switchPage(btn.dataset.page));
        });

        // Конвертация
        this.convertBtn.addEventListener('click', () => this.convert());
        this.swapBtn.addEventListener('click', () => this.swapCurrencies());
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.parseTextInput();
        });

        // Изменение базовой валюты
        this.baseSelect.addEventListener('change', () => {
            this.baseCurrency = this.baseSelect.value;
            this.loadRates();
        });

        // Автоматическая конвертация при вводе суммы
        this.amountInput.addEventListener('input', () => this.convert());
        this.fromSelect.addEventListener('change', () => this.convert());
        this.toSelect.addEventListener('change', () => this.convert());
    }

    async loadCurrencies() {
        try {
            const response = await fetch(`${this.apiUrl}USD`);
            const data = await response.json();
            this.currencies = Object.keys(data.rates).sort();
            this.populateCurrencySelects();
        } catch (error) {
            console.error('Ошибка загрузки валют:', error);
            this.showError('Не удалось загрузить список валют');
        }
    }

    populateCurrencySelects() {
        const options = this.currencies.map(currency => 
            `<option value="${currency}">${currency}</option>`
        ).join('');

        this.fromSelect.innerHTML = options;
        this.toSelect.innerHTML = options;
        this.baseSelect.innerHTML = options;

        // Устанавливаем значения по умолчанию
        this.fromSelect.value = 'USD';
        this.toSelect.value = 'RUB';
        this.baseSelect.value = 'USD';
    }

    async loadRates() {
        try {
            this.showLoading();
            
            const response = await fetch(`${this.apiUrl}${this.baseCurrency}`);
            const data = await response.json();
            
            this.rates = data.rates;
            this.lastUpdate = new Date();
            
            this.displayRates();
            this.updateLastUpdateTime();
        } catch (error) {
            console.error('Ошибка загрузки курсов:', error);
            this.showError('Не удалось загрузить курсы валют');
        } finally {
            this.hideLoading();
        }
    }

    displayRates() {
        const ratesHtml = Object.entries(this.rates)
            .sort()
            .map(([currency, rate]) => `
                <div class="rate-row">
                    <span class="currency">${currency}</span>
                    <span class="rate">${rate.toFixed(4)}</span>
                </div>
            `).join('');

        this.ratesTable.innerHTML = ratesHtml;
    }

    updateLastUpdateTime() {
        if (this.lastUpdate) {
            const timeStr = this.lastUpdate.toLocaleTimeString();
            const dateStr = this.lastUpdate.toLocaleDateString();
            this.lastUpdateEl.textContent = `Последнее обновление: ${dateStr} ${timeStr}`;
        }
    }

    async convert() {
        const amount = parseFloat(this.amountInput.value);
        const fromCurrency = this.fromSelect.value;
        const toCurrency = this.toSelect.value;

        if (!amount || amount <= 0) {
            this.resultBox.textContent = 'Введите корректную сумму';
            return;
        }

        try {
            // Загружаем актуальные курсы для конвертации
            const response = await fetch(`${this.apiUrl}${fromCurrency}`);
            const data = await response.json();
            
            const rate = data.rates[toCurrency];
            const result = amount * rate;

            this.resultBox.innerHTML = `
                <div>
                    <div style="font-size: 0.8em; color: #666; margin-bottom: 5px;">
                        ${amount} ${fromCurrency} =
                    </div>
                    <div style="font-size: 1.2em; color: #667eea;">
                        ${result.toFixed(2)} ${toCurrency}
                    </div>
                    <div style="font-size: 0.7em; color: #999; margin-top: 5px;">
                        Курс: 1 ${fromCurrency} = ${rate.toFixed(4)} ${toCurrency}
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Ошибка конвертации:', error);
            this.resultBox.textContent = 'Ошибка при конвертации';
        }
    }

    parseTextInput() {
        const text = this.textInput.value.trim().toLowerCase();
        const match = text.match(/(\d+(?:\.\d+)?)\s*([a-z]{3})\s+(?:in|to)\s+([a-z]{3})/i);

        if (match) {
            const amount = parseFloat(match[1]);
            const fromCurrency = match[2].toUpperCase();
            const toCurrency = match[3].toUpperCase();

            if (this.currencies.includes(fromCurrency) && this.currencies.includes(toCurrency)) {
                this.amountInput.value = amount;
                this.fromSelect.value = fromCurrency;
                this.toSelect.value = toCurrency;
                this.convert();
            } else {
                this.resultBox.textContent = 'Неверный код валюты';
            }
        } else {
            this.resultBox.textContent = 'Неверный формат. Пример: 15 usd in rub';
        }
    }

    swapCurrencies() {
        const fromValue = this.fromSelect.value;
        const toValue = this.toSelect.value;
        
        this.fromSelect.value = toValue;
        this.toSelect.value = fromValue;
        
        this.convert();
    }

    switchPage(page) {
        // Обновляем кнопки навигации
        this.navBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.page === page);
        });

        // Показываем нужную страницу
        if (page === 'converter') {
            this.converterPage.classList.add('active');
            this.ratesPage.classList.remove('active');
        } else {
            this.converterPage.classList.remove('active');
            this.ratesPage.classList.add('active');
            this.loadRates(); // Обновляем курсы при переходе на страницу
        }
    }

    detectUserCurrency() {
        // Пытаемся определить валюту пользователя по языку
        const language = navigator.language || navigator.userLanguage;
        
        const currencyMap = {
            'ru': 'RUB',
            'en-US': 'USD',
            'en-GB': 'GBP',
            'de': 'EUR',
            'fr': 'EUR',
            'jp': 'JPY',
            'cn': 'CNY'
        };

        const detectedCurrency = currencyMap[language] || 'USD';
        
        if (this.currencies.includes(detectedCurrency)) {
            this.baseSelect.value = detectedCurrency;
            this.fromSelect.value = detectedCurrency;
        }
    }

    showLoading() {
        this.ratesTable.innerHTML = '<div class="loading" style="margin: 20px auto;"></div>';
    }

    hideLoading() {
        // Убирается автоматически при displayRates
    }

    showError(message) {
        this.ratesTable.innerHTML = `<div style="color: red; text-align: center; padding: 20px;">${message}</div>`;
    }
}

// Запускаем приложение после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    new CurrencyConverter();
});