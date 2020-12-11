from tests import data


def test_as_id_string():
    assert data.COURSE_74.as_id_string() == 'Course-74'
