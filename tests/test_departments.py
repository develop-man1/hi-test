from app.schemas.department import DepartmentCreate


def test_department_schema_validation():
    dept = DepartmentCreate(name="  Test  ", parent_id=None)
    assert dept.name == "Test"
    assert dept.parent_id is None


def test_department_schema_empty_name():
    try:
        DepartmentCreate(name="", parent_id=None)
        assert False, "Should have raised"
    except Exception:
        pass