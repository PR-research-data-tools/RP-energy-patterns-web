// JavaScript Document

const imgCollectorUrl = "/ese/api/v1/images/";
const containerId = "image-gallery";
const loadAtStart = 12;
const loadWhenScrolling = 8;

let container;
let currentIndex = 0;
let maxIndex = 196;


function addPads(data) {
    data.forEach(img => {
        const responsive = document.createElement('div');
        responsive.classList.add("responsive");
        responsive.innerHTML = `
        <div class="gallery">
            <a target="_blank" href="${img.url}"> <img src="${img.download_url}" alt="id:${img.id}" width="${img.width}" height="${img.height}"> </a>
            <div class="desc">Author: ${img.author}</div>
        </div>
        `;
        container.appendChild(responsive);
    });
}


function fetchImageJSON(num = 1) {
    console.log(currentIndex);
    return new Promise(resolve => {
        const url = `${imgCollectorUrl}?offset=${currentIndex}&length=${num}`;
        fetch(url)
        .then(response => response.json())
        .then(payload => {
            if (payload.length > 0) {
                currentIndex += payload.length;
                addPads(payload);
            }
            else {
                maxIndex = currentIndex;
            }
            if (currentIndex >= maxIndex) {
                document.removeEventListener('scroll', recurrentLoad, false);
                window.removeEventListener('resize', recurrentLoad, false);
            }
            resolve();
        });
    });
}


function pageInit() {
    container = document.getElementById(containerId);
    initialLoad();
}

async function initialLoad() {
    await fetchImageJSON(loadAtStart);
    recurrentLoad();
}

async function recurrentLoad() {
    document.removeEventListener('scroll', recurrentLoad, false);
    window.removeEventListener('resize', recurrentLoad, false);

    while ((document.documentElement.scrollHeight <= window.scrollY + window.innerHeight) && (currentIndex < maxIndex)) {
        await fetchImageJSON(loadWhenScrolling);
    }
    
    document.addEventListener('scroll', recurrentLoad, false);
    window.addEventListener('resize', recurrentLoad, false);
}


// For static version
function loadEverything() {
    container = document.getElementById(containerId);
    fetchImageJSON(maxIndex);
}

