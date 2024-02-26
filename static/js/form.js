// FILE UPLOAD FORM
const fileUploadForm = document.querySelector('.upload-form')
const updateButton = document.querySelector('button.update')

updateButton.addEventListener('click', function() {
    fileUploadForm.classList.toggle('show')
    fileUploadForm.classList.toggle('hide')

    updateButton.textContent = fileUploadForm.classList.contains('hide') ? 'Update' : 'Cancel'
    updateButton.style.backgroundColor = fileUploadForm.classList.contains('hide') ? '#B28D1B' : 'rgba(238, 107, 107)'
})


