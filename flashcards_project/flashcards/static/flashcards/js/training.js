document.addEventListener("DOMContentLoaded", () => {
    const cards = JSON.parse(document.getElementById("card-data").textContent); // Получаем карточки
    const cardContainer = document.getElementById("card-container");
    const nextButton = document.getElementById("next-button");
    console.log(cards);

    let currentCardIndex = 0;

    // Функция для отображения информационной карточки
    const renderInfoCard = (card) => {
        cardContainer.innerHTML = `
            <div class="flashcard">
                <p class="flashcard-word">${card.word}</p>
                <p class="flashcard-transcription">${card.transcription}</p>
                <p class="flashcard-translation">${card.translation}</p>
            </div>
        `;
        nextButton.style.display = "block";
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
            if (userInput === card.word.toLowerCase()) {
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
            nextButton.style.display = "block"; // Показываем кнопку "Далее"
        });

        document.getElementById("reveal-button").addEventListener("click", () => {
            feedback.textContent = `Правильное слово: ${card.word}`;
            feedback.style.color = "blue";
            nextButton.style.display = "block"; // Показываем кнопку "Далее"
        });
    };

    // Функция для отображения карточек
    const showCard = (index) => {
        if (index < cards.length) {
            const card = cards[index];
            if (card.type === "info") {
                renderInfoCard(card); // Информационная карточка
            } else if (card.type === "input") {
                renderInputCard(card); // Карточка с вводом слова
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
        nextButton.style.display = "none"; // Скрываем кнопку "Далее"
        showCard(currentCardIndex);
    });

    showCard(currentCardIndex); // Отображаем первую карточку
});
