function selectTopic(topic) {
    localStorage.setItem('selectedTopic', topic); // Сохраняем тему в localStorage
    window.location.href = "/cards/" + "?topic=" + encodeURIComponent(topic);
}
