from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_wells():
    response = client.get("/wells")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_wells_by_id():
    response = client.get("/wells/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "well 1",
        "field": "NORTH",
    }


def test_getting_non_existing_well():
    response = client.get("/wells/10")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Well not found"
    }


def test_get_materials():
    response = client.get("/materials")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_materials_by_name():
    response = client.get("/materials/water")
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "water",
        "uom": "M3",
    }


def test_get_non_existing_material():
    response = client.get("/materials/diamond")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Material not found"
    }


def test_get_daily_productions_by_well():
    response = client.get("/Productions/wells/2")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_daily_productions_by_non_existing_well():
    response = client.get("/Productions/wells/10")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Well not found"
    }


def test_get_daily_productions_by_date():
    response = client.get("/Productions/date/2023-01-10")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_well():
    response = client.post(
        "/wells/new",
        json={"name": "well 5", "field": "CENTER"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 5,
        "name": "well 5",
        "field": "CENTER",
    }


def test_create_existing_well():
    response = client.post(
        "/wells/new",
        json={"name": "well 5", "field": "CENTER"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Well already exists"}


def test_create_well_with_wrong_field():
    response = client.post(
        "/wells/new",
        json={"name": "well 6", "field": "SOUTH WEST"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Field must be SOUTH, NORTH or CENTER"}


def test_create_material():
    response = client.post(
        "/materials/new/",
        json={"name": "gold", "uom": "Tonne"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 4,
        "name": "gold",
        "uom": "Tonne"
    }


def test_create_existing_material():
    response = client.post(
        "/materials/new",
        json={"name": "oil", "uom": "M3"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Material already exists"}


def test_create_material_with_wrong_uom():
    response = client.post(
        "/materials/new",
        json={"name": "diamond", "uom": "KG"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "UOM must be M3 or Tonne"}


def test_create_daily_production():
    response = client.post(
        "/productions/new/1/2",
        json={"production_date": "2023-02-20", "qte": 2000.},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 12,
        "well_id": 1,
        "material_id": 2,
        "production_date": "2023-02-20",
        "qte": 2000.0,
    }


def test_delete_daily_production():
    response = client.delete(
        "/productions/delete/oil/3/2023-01-10",
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Successfully Deleted"}


def test_delete_non_existing_daily_production():
    response = client.delete(
        "/productions/delete/oil/3/2023-01-11",
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Well or Material or DailProduction not found'}


def test_update_well():
    response = client.put(
        "/wells/update/2",
        json={"name": "well updated", "field": "NORTH", "id": 1}
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "well updated",
        "field": "NORTH",
        "id": 2
    }


def test_update_non_existing_well():
    response = client.put(
        "/wells/update/10",
        json={"name": "well updated", "field": "NORTH", "id": 1}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Well not found'}
