let currentIndex = 0;
const selectedTopic = localStorage.getItem('selectedTopic');
let filteredCards = [];

fetch(`/api/cards/?topic=${selectedTopic}`)
    .then(response => response.json())
    .then(data => {
        filteredCards = data;
        if (filteredCards.length > 0) {
            displayCard();
        } else {
            document.getElementById('word').innerText = "Нет карточек для данной темы";
            document.getElementById('transcription').innerText = "";
            document.getElementById('translation').innerText = "";
        }
    })
    .catch(error => console.error('Ошибка загрузки карточек:', error));

function displayCard() {
    if (filteredCards.length > 0) {
        const card = filteredCards[currentIndex];
        document.getElementById('word').innerText = card.word;
        document.getElementById('transcription').innerText = card.transcription;
        document.getElementById('translation').innerText = card.translation;
    }
}

function nextCard() {
    if (filteredCards.length > 0) {
        currentIndex = (currentIndex + 1) % filteredCards.length;
        displayCard();
    }
}

function prevCard() {
    if (filteredCards.length > 0) {
        currentIndex = (currentIndex - 1 + filteredCards.length) % filteredCards.length;
        displayCard();
    }
}

window.onload = displayCard;
