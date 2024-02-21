def test_add_book(client):
    response = client.post('/book', json={
        'name': 'The Hobbit',
        'author': 'J.R.R. Tolkien',
        'genre': 'Fantasy',
        'pages': 295,
        'read': False
    })

    assert response.status_code == 200
    assert response.json == {
        'author': 'J.R.R. Tolkien',
        'genre': 'Fantasy',
        'id': 1,
        'name': 'The Hobbit',
        'pages': 295,
        'read': False
    }

def test_get_books(client):
    response = client.get('/books')

    assert response.status_code == 200
    data = response.json
    print(data)
    assert isinstance(data, list)  # Check if the response data is a list
    assert any('name' in item for item in data)  # Check if 'name' exists in at least one item in the list

def test_get_book(client):
    response = client.get('/book/1')

    assert response.status_code == 200
    assert response.json == {
        'author': 'J.R.R. Tolkien',
        'genre': 'Fantasy',
        'id': 1,
        'name': 'The Hobbit',
        'pages': 295,
        'read': False
    }

def test_update_book(client):
    response = client.put('/book/1', json={
        'author': 'J.R.R. Jolkien',
        'genre': 'Bantasy',
        'name': 'The Bobbit',
        'pages': 420,
        'read': True
    })

    assert response.status_code == 200
    assert response.json == {
        'author': 'J.R.R. Jolkien',
        'genre': 'Bantasy',
        'id': 1,
        'name': 'The Bobbit',
        'pages': 420,
        'read': True
    }

def test_delete_book(client):
    response = client.delete('/book/1')

    assert response.status_code == 200
    assert response.json == {'message': 'Book deleted'}

    response = client.get('/book/1')
    assert response.status_code == 404
    assert response.json == {'message': 'Book not found'}

