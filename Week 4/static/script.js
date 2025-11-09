document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        agree: document.getElementById('agree'),
        submit: document.getElementById('submit'),
        email: document.getElementById('email'),
        password: document.getElementById('password'),
        hotel: document.getElementById('hotel'),
        search: document.getElementById('search')
    };

    // 登入按鈕
    elements.submit?.addEventListener('click', (e) => {
        if (!elements.agree?.checked) {
            e.preventDefault();
            alert('請勾選同意條款');
        }
    });

    // 查詢按鈕
    elements.search?.addEventListener('click', (e) => {
        e.preventDefault();
        const hotelId = parseInt(elements.hotel?.value);
        
        if (isNaN(hotelId) || hotelId <= 0) {
            alert('請輸入正整數');
        } else {
            window.location.href = `/hotel/${hotelId}`;
        }
    });
});