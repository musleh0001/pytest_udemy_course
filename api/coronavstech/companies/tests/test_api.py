import json
import pytest
from django.urls import reverse
from companies.models import Company



companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db


# {basename}-list/create/update/destroy
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []

# -------------- Test Get Companies ----------------- #
def test_one_company_exists_should_succeed(client) -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""

# --------------- Test Post Companies ------------------ #
def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}

def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="apple")
    response = client.post(path=companies_url, data={"name": "apple"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["company with this name already exists."]}

def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "test company name"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "test company name"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""

def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(path=companies_url, data={"name": "test company name", "status": "Layoffs"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"

def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(path=companies_url, data={"name": "test company name", "status": "WrongStatus"})
    assert response.status_code == 400
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice." in str(response.content)

@pytest.mark.xfail
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2

@pytest.mark.skip
def test_should_be_skiped() -> None:
    assert 1 == 2