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