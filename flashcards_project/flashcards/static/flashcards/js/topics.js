document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-training');

    startButton.addEventListener('click', () => {
        // Считываем выбранные темы
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        const selectedTopics = Array.from(checkboxes).map(checkbox => checkbox.value);

        if (selectedTopics.length === 0) {
            alert('Пожалуйста, выберите хотя бы одну тему для тренировки.');
            return;
        }

        // Перенаправление на тренировку с передачей выбранных тем
        const url = `/training/?topics=${encodeURIComponent(selectedTopics.join(','))}`;
        window.location.href = url;
    });
});