const navbar = document.querySelector('nav')
const navLinks = document.querySelector('nav .nav-links')
const dropdown = document.querySelector('.dropdown')
const accountButton = document.querySelector('.account-button')

window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY
    console.log(scrollPosition);

    if (scrollPosition > 50) {
        navbar.style.boxShadow = 'var(--box-shadow)'
    } else {
        navbar.style.boxShadow = 'none'
    }
})

accountButton.addEventListener('click', () => {
    dropdown.classList.toggle('hide-dropdown')
    dropdown.classList.toggle('show-dropdown')
})
