document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".training-card"); // Получаем все карточки
    const nextButton = document.getElementById("next-button"); // Кнопка "Запомнил"
    let currentCardIndex = 0; // Индекс текущей карточки

    // Функция для отображения текущей карточки
    const showCard = (index) => {
        cards.forEach((card, i) => {
            card.style.display = i === index ? "block" : "none"; // Показываем только текущую карточку
        });
    };

    // Обработчик кнопки "Запомнил"
    nextButton.addEventListener("click", () => {
        if (currentCardIndex < cards.length - 1) {
            currentCardIndex++;
            showCard(currentCardIndex);
        } else {
            alert("Тренировка завершена!");
            window.location.href = "/topics/"; // Перенаправляем на страницу выбора тем
        }
    });

    // Отображаем первую карточку при загрузке
    showCard(currentCardIndex);
});
