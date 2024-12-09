document.addEventListener("DOMContentLoaded", () => {
    const cards = JSON.parse(document.getElementById("card-data").textContent); // Получаем карточки
    const cardContainer = document.getElementById("card-container");
    const nextButton = document.getElementById("next-button");

    let currentCardIndex = 0;
    let wordsSeen = new Set();  // Множество для хранения уже встреченных слов
    let lastCardWasTask = false;  // Флаг для отслеживания, было ли задание перед карточкой с информацией

    // Функция для отправки прогресса на сервер
    function sendProgress(cardId, correct) {
        console.log("sendProgress вызвана с данными:", cardId, correct);
        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
        console.log('CSRF Token:', csrfToken);// Получаем CSRF токен

        fetch('/update_progress/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // CSRF токен для POST-запросов
            },
            body: JSON.stringify({
                card_id: cardId,
                correct: correct
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Progress updated:', data);
                    // Можно обновить интерфейс, например, показать актуальную точность
                } else {
                    console.error('Error updating progress:', data.message);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    // Функция для отображения информационной карточки
    const renderInfoCard = (card) => {
        cardContainer.innerHTML = `
            <div class="flashcard">
                <p class="flashcard-word">${card.word}</p>
                <p class="flashcard-transcription">${card.transcription}</p>
                <p class="flashcard-translation">${card.translation}</p>
            </div>
        `;

        // Если слово встречается впервые в тренировке
        if (!wordsSeen.has(card.word)) {
            nextButton.textContent = "Запомнил";  // Если слово встречается впервые
        } else {
            nextButton.textContent = "Помню";  // Если слово уже встречалось
        }

        nextButton.style.display = "block";  // Показываем кнопку
    };

    // Функция для отображения карточки с вводом слова
    const renderInputCard = (card) => {
        cardContainer.innerHTML = `
            <div class="flashcard">
                <p class="flashcard-translation">Перевод: ${card.translation}</p>
                <input type="text" id="user-input" placeholder="Введите слово" class="input-field"/>
                <button id="check-button" class="nav-button">Проверить</button>
                <button id="reveal-button" class="nav-button">Не помню</button>
                <p id="feedback" class="feedback"></p>
            </div>
        `;

        const inputField = document.getElementById("user-input");
        const feedback = document.getElementById("feedback");

        document.getElementById("check-button").addEventListener("click", () => {
            const userInput = inputField.value.trim().toLowerCase();
            const isCorrect = userInput === card.word.toLowerCase();

            if (isCorrect) {
                inputField.style.borderColor = "green";
                inputField.style.backgroundColor = "#d4edda";
                feedback.textContent = "Правильно!";
                feedback.style.color = "green";
            } else {
                inputField.style.borderColor = "red";
                inputField.style.backgroundColor = "#f8d7da";
                feedback.textContent = `Неправильно!`;
                feedback.style.color = "red";
            }

            // Отправляем прогресс на сервер
            sendProgress(card.id, isCorrect);

            // После выполнения задания, показываем карточку с информацией через 1 секунду
            setTimeout(() => {
                renderInfoCard(card);  // Показываем карточку с информацией
                wordsSeen.add(card.word);  // Добавляем слово в множество встреченных
                lastCardWasTask = true;  // Помечаем, что было задание
            }, 1000); // Задержка 1 секунда
        });

        document.getElementById("reveal-button").addEventListener("click", () => {
            feedback.textContent = `Правильное слово: ${card.word}`;
            feedback.style.color = "blue";

            console.log("sendProgress вызвана:", card.id, isCorrect);  // Лог для отладки

            // Отправляем прогресс на сервер
            sendProgress(card.id, false);

            // После выполнения задания, показываем карточку с информацией через 1 секунду
            setTimeout(() => {
                renderInfoCard(card);  // Показываем карточку с информацией
                wordsSeen.add(card.word);  // Добавляем слово в множество встреченных
                lastCardWasTask = true;  // Помечаем, что было задание
            }, 1000); // Задержка 1 секунда
        });
    };

    // Функция для отображения карточки с выбором правильного перевода
    const renderChoiceCard = (card, allCards) => {
        // Получаем случайные переводы для неверных вариантов
        const otherTranslations = allCards
            .filter((c) => c.word !== card.word) // Исключаем перевод текущего слова
            .map((c) => c.translation);

        // Перемешиваем переводы, чтобы случайные варианты не повторялись
        const incorrectOptions = shuffle(otherTranslations).slice(0, 2); // Два случайных перевода
        const options = [card.translation, ...incorrectOptions]; // Объединяем правильный вариант с двумя неправильными

        // Перемешиваем все варианты, чтобы правильный вариант не был всегда первым
        shuffle(options);

        cardContainer.innerHTML = `
            <div class="flashcard">
                <p class="flashcard-word">${card.word}</p>
                <p class="flashcard-translation">Выберите правильный перевод:</p>
                <div id="options">
                    <button class="option-button" data-correct="${card.translation}">${options[0]}</button>
                    <button class="option-button" data-correct="${card.translation}">${options[1]}</button>
                    <button class="option-button" data-correct="${card.translation}">${options[2]}</button>
                </div>
            </div>
        `;

        const optionButtons = document.querySelectorAll(".option-button");

        optionButtons.forEach((button) => {
            button.addEventListener("click", () => {
                const isCorrect = button.textContent === card.translation;

                if (isCorrect) {
                    button.style.backgroundColor = "green"; // Правильный ответ
                } else {
                    button.style.backgroundColor = "red"; // Неправильный ответ
                    const correctButton = Array.from(optionButtons).find(
                        (btn) => btn.textContent === card.translation
                    );
                    correctButton.style.backgroundColor = "green"; // Подсвечиваем правильный ответ
                }

                // Отправляем прогресс на сервер
                sendProgress(card.id, isCorrect);

                // После выполнения задания, показываем карточку с информацией через 1 секунду
                setTimeout(() => {
                    renderInfoCard(card);  // Показываем карточку с информацией
                    wordsSeen.add(card.word);  // Добавляем слово в множество встреченных
                    lastCardWasTask = true;  // Помечаем, что было задание
                }, 1000); // Задержка 1 секунда
            });
        });
    };

    // Функция для отображения карточек
    const showCard = (index) => {
        console.log("Показываем карточку с индексом:", index);
        if (index < cards.length) {
            const card = cards[index];

            if (card.type === "info") {
                if (lastCardWasTask) {
                    renderInfoCard(card);  // Показываем карточку с информацией
                    lastCardWasTask = false;  // После карточки с информацией, задание должно быть следующей карточкой
                } else {
                    renderInfoCard(card);  // Показываем карточку с информацией
                    lastCardWasTask = false;  // Карточка с информацией без задания
                }
            } else if (card.type === "input") {
                renderInputCard(card);  // Карточка с вводом слова
            } else if (card.type === "choice") {
                renderChoiceCard(card, cards);  // Карточка с выбором перевода
                lastCardWasTask = true;  // Помечаем, что было задание
            }
        } else {
            cardContainer.innerHTML = `
                <div class="flashcard">
                    <h2>Тренировка завершена!</h2>
                    <button class="nav-button" onclick="window.location.href='/topics/'">Вернуться к темам</button>
                </div>
            `;
            nextButton.style.display = "none";
        }
    };

    nextButton.addEventListener("click", () => {
        console.log("Кнопка 'Далее' нажата");
        currentCardIndex++;
        nextButton.style.display = "none"; // Скрываем кнопку "Далее"
        showCard(currentCardIndex);
    });

    showCard(currentCardIndex); // Отображаем первую карточку
});

// Функция для случайного перемешивания элементов
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Перестановка элементов
    }
    return array;
}
