const navbar = document.querySelector('nav')
const navLinks = document.querySelector('nav .nav-links')
const dropdown = document.querySelector('.dropdown')
const accountButton = document.querySelector('.account-button')

accountButton.addEventListener('click', () => {
    dropdown.classList.toggle('hide-dropdown')
    dropdown.classList.toggle('show-dropdown')
})