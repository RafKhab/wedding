document.addEventListener('DOMContentLoaded', () => {
    // --- Таймер обратного отсчета ---
    const targetDate = new Date('2026-09-19T16:00:00').getTime(); // Установим 16:00 как старт мероприятия

    function getPlural(number, one, two, five) {
        let n = Math.abs(number);
        n %= 100;
        if (n >= 5 && n <= 20) {
            return five;
        }
        n %= 10;
        if (n === 1) {
            return one;
        }
        if (n >= 2 && n <= 4) {
            return two;
        }
        return five;
    }

    function updateCountdown() {
        const now = new Date().getTime();
        const distance = targetDate - now;

        if (distance < 0) {
            document.getElementById('cd-days').innerText = "00";
            document.getElementById('cd-hours').innerText = "00";
            document.getElementById('cd-minutes').innerText = "00";
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

        document.getElementById('cd-days').innerText = days < 10 ? '0' + days : days;
        document.getElementById('cd-days').nextElementSibling.innerText = getPlural(days, 'День', 'Дня', 'Дней');
        
        document.getElementById('cd-hours').innerText = hours < 10 ? '0' + hours : hours;
        document.getElementById('cd-hours').nextElementSibling.innerText = getPlural(hours, 'Час', 'Часа', 'Часов');
        
        document.getElementById('cd-minutes').innerText = minutes < 10 ? '0' + minutes : minutes;
        document.getElementById('cd-minutes').nextElementSibling.innerText = getPlural(minutes, 'Минута', 'Минуты', 'Минут');
    }

    updateCountdown();
    setInterval(updateCountdown, 60000); // Обновляем раз в минуту

    // --- Логика формы RSVP ---
    const form = document.getElementById('rsvp-form');
    const presenceRadios = document.querySelectorAll('input[name="presence"]');
    const plusOneFields = document.getElementById('plus-one-fields');
    const submitBtn = document.getElementById('submit-btn');
    
    // Инпуты текста для стилей .filled
    const textInputs = form.querySelectorAll('input[type="text"]');

    const handleInputHighlight = (input) => {
        if (input.value.trim() !== "") {
            input.classList.add('filled');
        } else {
            input.classList.remove('filled');
        }
    };

    textInputs.forEach(input => {
        input.addEventListener('input', () => {
            handleInputHighlight(input);
            validateForm();
        });
    });

    // Обработка переключения "+1"
    presenceRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'Приду с +1') {
                plusOneFields.classList.remove('hidden');
            } else {
                plusOneFields.classList.add('hidden');
            }
            validateForm();
        });
    });

    // Добавляем слушатели на все остальные радио-кнопки и чекбоксы для валидации
    const allInputs = form.querySelectorAll('input');
    allInputs.forEach(input => {
        if (input.type === 'radio' || input.type === 'checkbox') {
            input.addEventListener('change', validateForm);
        }
    });

    // Валидация формы
    function validateForm() {
        const nameInput = document.getElementById('name');
        const nameVal = nameInput.value.trim();
        const presence = form.querySelector('input[name="presence"]:checked');
        
        let isValid = false;

        if (nameVal && presence) {
            const presenceVal = presence.value;

            if (presenceVal === 'К сожалению, не смогу') {
                // Если не сможет, достаточно имени и статуса
                isValid = true;
            } else if (presenceVal === 'Приду с радостью') {
                const food = form.querySelector('input[name="food"]:checked');
                const drinks = form.querySelectorAll('input[name="drinks"]:checked');
                
                // Аллергия может быть пустой, мы ее не форсируем, но можно проверять, если нужно
                if (food && drinks.length > 0) {
                    isValid = true;
                }
            } else if (presenceVal === 'Приду с +1') {
                const food = form.querySelector('input[name="food"]:checked');
                const drinks = form.querySelectorAll('input[name="drinks"]:checked');
                
                const guestNameInput = document.getElementById('guestName');
                const gNameVal = guestNameInput.value.trim();
                const gFood = form.querySelector('input[name="guestFood"]:checked');
                const gDrinks = form.querySelectorAll('input[name="guestDrinks"]:checked');

                if (food && drinks.length > 0 && gNameVal && gFood && gDrinks.length > 0) {
                    isValid = true;
                }
            }
        }

        if (isValid) {
            submitBtn.removeAttribute('disabled');
            submitBtn.classList.remove('incomplete');
            submitBtn.classList.add('complete');
        } else {
            submitBtn.setAttribute('disabled', 'true');
            submitBtn.classList.remove('complete');
            submitBtn.classList.add('incomplete');
        }
    }

    // Обработка отправки формы
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formMessage = document.getElementById('form-message');
        const successMessage = document.getElementById('success-message');
        
        // Блокируем кнопку
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Отправка...';
        formMessage.textContent = '';
        formMessage.className = 'form-message';

        // Сбор данных
        const formData = new FormData(form);
        const dataObj = {
            name: formData.get('name') || '',
            presence: formData.get('presence') || '',
            food: formData.get('food') || '',
            drinks: formData.getAll('drinks').join(', '),
            allergy: formData.get('allergy') || '',
            guestName: formData.get('guestName') || '',
            guestFood: formData.get('guestFood') || '',
            guestDrinks: formData.getAll('guestDrinks').join(', '),
            guestAllergy: formData.get('guestAllergy') || ''
        };

        const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxeya17K_4YHAJGJ5BD7sFD554fxKyksIYHQ3khny88vK75opTRkxoa9a3txMCSemzuBw/exec';

        try {
            const response = await fetch(GOOGLE_SCRIPT_URL, {
                method: 'POST',
                // Google Apps Script принимает POST лучше всего в формате text/plain для обхода CORS
                body: JSON.stringify(dataObj)
            });

            if (response.ok) {
                // Успех
                form.classList.add('hidden');
                document.querySelector('.rsvp-section .section-title').classList.add('hidden');
                successMessage.classList.remove('hidden');
            } else {
                throw new Error('Ошибка сети');
            }
        } catch (error) {
            console.error('Ошибка отправки:', error);
            formMessage.textContent = 'Произошла ошибка при отправке. Пожалуйста, попробуйте еще раз позже.';
            formMessage.classList.add('error');
            
            // Восстанавливаем кнопку
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
            submitBtn.textContent = originalText;
        }
    });
});
