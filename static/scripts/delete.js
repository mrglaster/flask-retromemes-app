function addId(id) {
    input = document.createElement('input')
    input.setAttribute('type', 'hidden')
    input.setAttribute('name', 'id')
    input.setAttribute('value', id)
    document.getElementById('delete').appendChild(input)
    document.getElementById('delete').submit()
}