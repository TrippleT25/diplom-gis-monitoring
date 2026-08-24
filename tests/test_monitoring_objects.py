def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_monitoring_objects_require_auth(client):
    response = client.get("/monitoring-objects")

    assert response.status_code == 401


def test_create_monitoring_object(client, auth_headers):
    response = client.post(
        "/monitoring-objects",
        headers=auth_headers,
        json={
            "name": "GSM Meter 001",
            "latitude": 59.3293,
            "longitude": 18.0686,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "GSM Meter 001"
    assert data["latitude"] == 59.3293
    assert data["longitude"] == 18.0686


def test_get_monitoring_objects(client, auth_headers):
    client.post(
        "/monitoring-objects",
        headers=auth_headers,
        json={
            "name": "GSM Meter 001",
            "latitude": 59.3293,
            "longitude": 18.0686,
        },
    )

    response = client.get(
        "/monitoring-objects",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "GSM Meter 001"


def test_get_monitoring_object_by_id(client, auth_headers):
    create_response = client.post(
        "/monitoring-objects",
        headers=auth_headers,
        json={
            "name": "GSM Meter 001",
            "latitude": 59.3293,
            "longitude": 18.0686,
        },
    )

    assert create_response.status_code == 201

    object_id = create_response.json()["id"]

    response = client.get(
        f"/monitoring-objects/{object_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == object_id
    assert response.json()["name"] == "GSM Meter 001"


def test_get_missing_monitoring_object(client, auth_headers):
    response = client.get(
        "/monitoring-objects/999",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Monitoring object not found"
    }


def test_update_monitoring_object(client, auth_headers):
    create_response = client.post(
        "/monitoring-objects",
        headers=auth_headers,
        json={
            "name": "GSM Meter 001",
            "latitude": 59.3293,
            "longitude": 18.0686,
        },
    )

    assert create_response.status_code == 201

    object_id = create_response.json()["id"]

    response = client.patch(
        f"/monitoring-objects/{object_id}",
        headers=auth_headers,
        json={
            "name": "GSM Meter Updated",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "GSM Meter Updated"

    # PATCH не должен менять поля,
    # которые мы не передавали.
    assert data["latitude"] == 59.3293
    assert data["longitude"] == 18.0686


def test_delete_monitoring_object(client, auth_headers):
    create_response = client.post(
        "/monitoring-objects",
        headers=auth_headers,
        json={
            "name": "GSM Meter 001",
            "latitude": 59.3293,
            "longitude": 18.0686,
        },
    )

    assert create_response.status_code == 201

    object_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/monitoring-objects/{object_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/monitoring-objects/{object_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_invalid_latitude(client, auth_headers):
    response = client.post(
        "/monitoring-objects",
        headers=auth_headers,
        json={
            "name": "Invalid meter",
            "latitude": 100,
            "longitude": 20,
        },
    )

    assert response.status_code == 422