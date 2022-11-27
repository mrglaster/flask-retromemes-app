function addId(id, action) {
    
    switch (action) {
        case 'delete':
            input = document.createElement('input')
            input.setAttribute('name', 'id')
            input.setAttribute('value', id)
            document.getElementById('delete').appendChild(input)
            document.getElementById('delete').submit()
            break;
        case 'like':
            input = document.createElement('input')
            input.setAttribute('name', 'id')
            input.setAttribute('value', id)
            document.getElementById('like').appendChild(input)
            document.getElementById('like').submit()
            break;
        case 'dislike':
            input = document.createElement('input')
            input.setAttribute('name', 'id')
            input.setAttribute('value', id)
            document.getElementById('dislike').appendChild(input)
            document.getElementById('dislike').submit()
            break;
    }
}