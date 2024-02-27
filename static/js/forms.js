// FILE UPLOAD FORM
const fileUploadForm = document.querySelector('.upload-form')
const picUpdateButton = document.querySelector('button.pic-update')

picUpdateButton.addEventListener('click', function() {
    fileUploadForm.classList.toggle('show')
    fileUploadForm.classList.toggle('hide')

    picUpdateButton.textContent = fileUploadForm.classList.contains('hide') ? 'Update' : 'Cancel'
    picUpdateButton.style.backgroundColor = fileUploadForm.classList.contains('hide') ? '#B28D1B' : 'rgba(238, 107, 107)'
})


// DETAILS UPDATE FORM
const detailForm = document.querySelector('.detail-form')
const detailUpdateButton = document.querySelector('button.detail-update')

detailUpdateButton.addEventListener('click', function() {
    detailForm.classList.toggle('show')
    detailForm.classList.toggle('hide')

    detailUpdateButton.textContent = detailForm.classList.contains('hide') ? 'Change' : 'Cancel'
    detailUpdateButton.style.backgroundColor = detailForm.classList.contains('hide') ? '#B28D1B' : 'rgba(238, 107, 107)'
})


// EMAIL FORM
const emailForm = document.querySelector('.email-form')
const emailUpdateButton = document.querySelector('button.email-update')

emailUpdateButton.addEventListener('click', function() {
    emailForm.classList.toggle('show')
    emailForm.classList.toggle('hide')

    emailUpdateButton.textContent = emailForm.classList.contains('hide') ? 'Change' : 'Cancel'
    emailUpdateButton.style.backgroundColor = emailForm.classList.contains('hide') ? '#B28D1B' : 'rgba(238, 107, 107)'
})


// PASSWORD FORM
const passwordForm = document.querySelector('.password-form')
const passwordUpdateButton = document.querySelector('button.password-update')

passwordUpdateButton.addEventListener('click', function() {
    passwordForm.classList.toggle('show')
    passwordForm.classList.toggle('hide')

    passwordUpdateButton.textContent = passwordForm.classList.contains('hide') ? 'Change Password' : 'Cancel'
    passwordUpdateButton.style.backgroundColor = passwordForm.classList.contains('hide') ? '#B28D1B' : 'rgba(238, 107, 107)'
})


