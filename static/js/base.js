const navbar = document.querySelector('nav')
const navLinks = document.querySelector('nav .nav-links')
const accountOptions = document.querySelector('.account-options')
const accountButton = document.querySelector('.account-button')

accountButton.addEventListener('click', () => {
    navbar.classList.toggle('expand')
    navLinks.classList.toggle('align-top')
    accountOptions.classList.toggle('none')
    accountOptions.classList.toggle('flex')
})