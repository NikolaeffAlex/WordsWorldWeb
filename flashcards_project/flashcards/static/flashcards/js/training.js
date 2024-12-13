document.addEventListener("DOMContentLoaded", () => {
    const cards = JSON.parse(document.getElementById("card-data").textContent);
    console.log(cards);  // Логируем все карточки, которые пришли из Django
    const cardContainer = document.getElementById("card-container");
    const nextButton = document.getElementById("next-button");

    let currentCardIndex = 0;
    let wordsSeen = new Set();
    let lastCardWasTask = false;

    // Отправка прогресса на сервер
    const sendProgress = (cardId, correct) => {
        console.log(`Sending progress for card ${cardId}, correct: ${correct}`)
        fetch('/update_progress/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            },
            body: JSON.stringify({ card_id: cardId, correct: correct })
        })
        .then(response => response.json())
        .then(data => console.log('Прогресс обновлен:', data))
        .catch(error => console.error('Ошибка обновления прогресса:', error));
    };

    // Отображение информационной карточки
    const renderInfoCard = (card) => {

        cardContainer.innerHTML = `
            <div class="flashcard">
                <p class="flashcard-word">${card.word}</p>
                <p class="flashcard-transcription">${card.transcription}</p>
                <p class="flashcard-translation">${card.translation}</p>
            </div>
        `;
        nextButton.textContent = wordsSeen.has(card.word) ? "Помню" : "Запомнил";
        console.log(nextButton.style.display);
        nextButton.style.display = "block";
    };

    // Отображение карточки с вводом слова
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
            const isCorrect = inputField.value.trim().toLowerCase() === card.word.toLowerCase();
            feedback.textContent = isCorrect ? "Правильно!" : "Неправильно!";
            feedback.style.color = isCorrect ? "green" : "red";

            sendProgress(card.id, isCorrect);

            setTimeout(() => {
                renderInfoCard(card);
                wordsSeen.add(card.word);
                lastCardWasTask = true;
            }, 1000);
        });

        document.getElementById("reveal-button").addEventListener("click", () => {
            feedback.textContent = `Правильное слово: ${card.word}`;
            feedback.style.color = "blue";

            sendProgress(card.id, false);

            setTimeout(() => {
                renderInfoCard(card);
                wordsSeen.add(card.word);
                lastCardWasTask = true;
            }, 1000);
        });
    };

    // Отображение карточки с выбором перевода
    const renderChoiceCard = (card, allCards) => {
        const incorrectOptions = shuffle(
            allCards
                .filter(c => c.word !== card.word)
                .map(c => c.translation)
        ).slice(0, 2);

        const options = shuffle([card.translation, ...incorrectOptions]);

        cardContainer.innerHTML = `
            <div class="flashcard">
                <p class="flashcard-word">${card.word}</p>
                <p class="flashcard-translation">Выберите правильный перевод:</p>
                <div id="options">
                    ${options.map(option => `<button class="option-button">${option}</button>`).join('')}
                </div>
            </div>
        `;

        document.querySelectorAll(".option-button").forEach(button => {
            button.addEventListener("click", () => {
                const isCorrect = button.textContent === card.translation;
                button.style.backgroundColor = isCorrect ? "green" : "red";

                if (!isCorrect) {
                    const correctButton = Array.from(document.querySelectorAll(".option-button"))
                        .find(btn => btn.textContent === card.translation);
                    correctButton.style.backgroundColor = "green";
                }

                sendProgress(card.id, isCorrect);

                setTimeout(() => {
                    renderInfoCard(card);
                    wordsSeen.add(card.word);
                    lastCardWasTask = true;
                }, 1000);
            });
        });
    };

    // Показ текущей карточки
    const showCard = (index) => {
        if (index < cards.length) {
            const card = cards[index];
            console.log(`Rendering card of type: ${card.type}`);  // Логируем тип карточки

            if (card.type === "info") {
                renderInfoCard(card);
                lastCardWasTask = false;
            } else if (card.type === "input") {
                renderInputCard(card);
            } else if (card.type === "choose_correct_translation") {
                renderChoiceCard(card, cards);
                lastCardWasTask = true;
            } else if (card.type === "type_word") {
                renderInputCard(card);
                lastCardWasTask = true;
            } else {
                console.log("Unknown card type: ", card.type);
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
        currentCardIndex++;
        nextButton.style.display = "none";
        showCard(currentCardIndex);
        console.log(`Next button display: ${nextButton.style.display}`);  // Логируем состояние кнопки
    });

    showCard(currentCardIndex);

    // Перемешивание массива
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
});

