// Merge place name + img
let mergedData = [];
// default 10 cards
let currentCount = 10;
// Click more load 10 cards
const STEP = 10;

// Function: 取得處理資料
async function getData() {
  const [textData, picsData] = await Promise.all([
  // 2 JSON files 分別存到 textData 和 picsData
  // Promise.all - 同時load 2個檔案，加快速度
  // async/await - 等待資料load完成後再處理，避免錯誤
    fetch('assignment-3-1.json').then(r => r.json()),
    // .then(r => r.json()) = 回應轉換JSON格式
    fetch('assignment-3-2.json').then(r => r.json())
  ]); 

  // Merge 2 JSON files 
  mergedData = textData.rows.flatMap(item => {
    // flatMap = review每個景點，將result「攤平」成1D array
    // 自動移除空array []
    const match = picsData.rows.find(p => p.serial === item.serial);
    // 圖片中尋找「編號相同」景點
    // find() = 找第一個符合條件的項目

    if (!match?.pics) return [];
    // 如找不到配對，或沒有圖片，回傳空array(flatMap自動過濾掉）

    const imgParts = match.pics.split('/');
    const jpgIdx = imgParts.findIndex(p => p.includes('.jpg'));
    if (jpgIdx === -1) return [];

    const imgPath = '/' + imgParts.slice(1, jpgIdx + 1).join('/');
    const firstImg = "https://www.travel.taipei" + imgPath;

    return [{ serial: item.serial, title: item.sname, img: firstImg }];
  });

  renderPromotions();
  // 呼叫Fuction：顯示前3個景點
  appendCards(3, 3 + currentCount);
  // 呼叫Function：第4個景點，顯示10張卡片
}


// createEL: Create New HTML elements 
function createEl(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className; // 檢查有沒有 className
  if (text) el.textContent = text; // 檢查有沒有 text
  return el;
}


// 顯示前3個景點
function renderPromotions() {
  const container = document.querySelector('.promotions');
  // Find class="promotions"
  container.textContent = ''; 
  // Clean container

  mergedData.slice(0, 3).forEach((item, i) => {
    // First 3 places
    const div = createEl('div', `promotion${i + 1}`);
    // 創建 div，class 為 'promotion1', 'promotion2', 'promotion3'..etc

    const img = createEl('img');
    img.src = item.img;

    const span = createEl('span', '', item.title);
    div.append(img, span);

    container.appendChild(div);
    // div append .promotions 容器
  });
}

// 顯示卡片 10 cards
function appendCards(start, end) {
  const container = document.querySelector('.content_blocks');
  // 找卡片容器 <ul class="content_blocks">

  mergedData.slice(start, end).forEach(item => {
    // slice(start, end) - 取指定範圍景點

    const li = createEl('li', 'card');
    // <li>, class="card"

    const img = createEl('img', 'card_img');
    img.src = item.img;
    // 圖片

    const star = createEl('img', 'card_star');
    star.src = 'star.png';
    // 星星

    const span = createEl('span', 'card_text', item.title);
    // 景點名稱

    li.append(img, star, span);
    // append 圖片、星星、文字到 <li> 
    container.appendChild(li);
    // 整個卡片加到容器
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







