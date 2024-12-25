def test_dashboard_view(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Active Properties' in response.data 