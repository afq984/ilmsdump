from tests import data


def test_as_id_string():
    assert data.COURSE_74.as_id_string() == 'Course-74'


def test_get_meta():
    assert data.COURSE_46274.get_meta() == {
        'id': 46274,
        'serial': '10910CS542200',
        'name': '平行程式Parallel Programming',
        'is_admin': False,
    }
