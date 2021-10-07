echo "execute the tests containing a string in its name pytest -k <substring>"
pytest -k ter -v
pytest -k parametrized -v
pytest  test_xfail_skip.py -v
