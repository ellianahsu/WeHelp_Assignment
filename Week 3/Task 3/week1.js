let mergedData = [];
async function getData() {
    // Fetch both JSON files
    const [res1, res2] = await Promise.all([
        fetch('assignment-3-1.json'),
        fetch('assignment-3-2.json')
    ]);

    // Parse both JSON files
    const [textData, picsData] = await Promise.all([
      res1.json(),
      res2.json()
    ]);
    
    textData.rows.forEach(item => {
        const match = picsData.rows.find(p => p.serial === item.serial);
        if (!match || !match.pics) return;

        const imgParts = match.pics.split('/');
        const firstJpgIndex = imgParts.findIndex(p => p.includes('.jpg'));
        if (firstJpgIndex === -1) return;

        const imgPath = '/' + imgParts.slice(1, firstJpgIndex + 1).join('/');
        const firstImg = "https://www.travel.taipei" + imgPath;

        mergedData.push({
            serial : item.serial,
            title : item.sname,
            img : firstImg
        });
    });
    
    const promotions = document.querySelector('.promotions');
    promotions.innerHTML = "";

    mergedData.slice(0,3).forEach((item, index) => {
        const promotions_block = document.createElement('div');
        promotions_block.classList.add(`promotion${index + 1}`);

        const img = document.createElement('img');
        img.src = item.img;

        const span = document.createElement('span');
        span.textContent = item.title;

        promotions_block.appendChild(img);
        promotions_block.appendChild(span);
        promotions.appendChild(promotions_block);
    });
    
    appendCards(3, 3 + currentCount);
}

function appendCards(start, end){
    const content_blocks = document.querySelector('.content_blocks');
    
    mergedData.slice(start, end).forEach((item) => {
        const li = document.createElement('li');
        li.classList.add('card');

        const img = document.createElement('img');
        img.classList.add('card_img');
        img.src = item.img;

        const star = document.createElement('img');
        star.classList.add('card_star');
        star.src = 'star.png';

        const span = document.createElement('span');
        span.classList.add('card_text');
        span.textContent = item.title;

        li.appendChild(img);
        li.appendChild(star);
        li.appendChild(span);
        content_blocks.appendChild(li);
    });
}

getData();

let currentCount = 10;
const STEP = 10;

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Get elements
    const mobileMenu = document.getElementById('mobile_menu');
    const menuList = document.getElementById('menu_list');
    const deleteIcon = document.getElementById('delete_icon');
    
    // Open menu when burger icon is clicked
    mobileMenu.addEventListener('click', function() {
        menuList.classList.add('active');
    });
    
    // Close menu when X icon is clicked
    deleteIcon.addEventListener('click', function() {
        menuList.classList.remove('active');
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!menuList.contains(event.target) && !mobileMenu.contains(event.target)) {
            menuList.classList.remove('active');
        }
    });
});







