const form = document.querySelector('.assign-form')

form.addEventListener('submit', function() {
    let uuidString = document.getElementById('reviewer').value
    let uuidValue = uuidString.replace(/['"]+/g, '')
    document.getElementById('reviewer').value = uuidValue
})