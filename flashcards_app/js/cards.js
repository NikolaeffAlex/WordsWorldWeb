const cards = [
    { word: "tree", translation: "дерево", transcription: "[tri:]", topic: "Природа" },
    { word: "sun", translation: "солнце", transcription: "[sʌn]", topic: "Природа" },
    { word: "job", translation: "работа", transcription: "[dʒɒb]", topic: "Работа" },
    { word: "office", translation: "офис", transcription: "[ˈɒfɪs]", topic: "Работа" }
];

let currentIndex = 0;
const selectedTopic = localStorage.getItem('selectedTopic');
const filteredCards = cards.filter(card => card.topic === selectedTopic);

console.log('Selected topic:', selectedTopic);
console.log('Filtered cards:', filteredCards);

function displayCard() {
    if (filteredCards.length > 0) {
        const card = filteredCards[currentIndex];
        document.getElementById('word').innerText = card.word;
        document.getElementById('transcription').innerText = card.transcription;
        document.getElementById('translation').innerText = card.translation;
    } else {
        document.getElementById('word').innerText = "Нет карточек для данной темы";
        document.getElementById('transcription').innerText = "";
        document.getElementById('translation').innerText = "";
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
