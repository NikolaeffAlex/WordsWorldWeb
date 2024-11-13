function selectTopic(topic) {
    localStorage.setItem('selectedTopic', topic); // Сохраняем выбранную тему
    window.location.href = 'cards.html';          // Переходим на страницу карточек
}

