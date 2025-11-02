let mergedData = [];
let currentCount = 10;
const STEP = 10;

async function getData() {
  const [textData, picsData] = await Promise.all([
    fetch('assignment-3-1.json').then(r => r.json()),
    fetch('assignment-3-2.json').then(r => r.json())
  ]);

  mergedData = textData.rows.flatMap(item => {
    const match = picsData.rows.find(p => p.serial === item.serial);
    if (!match?.pics) return [];

    const imgParts = match.pics.split('/');
    const jpgIdx = imgParts.findIndex(p => p.includes('.jpg'));
    if (jpgIdx === -1) return [];

    const imgPath = '/' + imgParts.slice(1, jpgIdx + 1).join('/');
    const firstImg = "https://www.travel.taipei" + imgPath;

    return [{ serial: item.serial, title: item.sname, img: firstImg }];
  });

  renderPromotions();
  appendCards(3, 3 + currentCount);
}

function createEl(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text) el.textContent = text;
  return el;
}

function renderPromotions() {
  const container = document.querySelector('.promotions');
  container.textContent = ''; // clear old ones

  mergedData.slice(0, 3).forEach((item, i) => {
    const div = createEl('div', `promotion${i + 1}`);
    const img = createEl('img');
    img.src = item.img;
    const span = createEl('span', '', item.title);
    div.append(img, span);
    container.appendChild(div);
  });
}

function appendCards(start, end) {
  const container = document.querySelector('.content_blocks');

  mergedData.slice(start, end).forEach(item => {
    const li = createEl('li', 'card');
    const img = createEl('img', 'card_img');
    img.src = item.img;

    const star = createEl('img', 'card_star');
    star.src = 'star.png';

    const span = createEl('span', 'card_text', item.title);

    li.append(img, star, span);
    container.appendChild(li);
  });
}

getData();


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







