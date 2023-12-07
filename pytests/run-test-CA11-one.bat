
#just one method
pytest --host  ca11 --port 19903 tests/symdumcicsrestapi/test_get_dump_index_endpoint.py::test_options_on_invalid_credentials -v

#just one test script
pytest --host  ca11 --port 19903 tests/symdumcicsrestapi/test_get_dump_index_endpoint.py -v
pytest --host  ca11 --port 19903 tests/symdumcicsrestapi/test_options_endpoint.py  -v
pytest --host  ca11 --port 19903 tests/symdumcicsrestapi/test_lock_unlock_endpoint.py  -v
pytest --host  ca11 --port 19903 tests/symdumcicsrestapi/test_delete_endpoint.py  -v
pytest --host  ca11 --port 19903 tests/symdumcicsrestapi/test_get_report_endpoint.py  -v

#run all symdumpcics tests
pytest --host  ca11 --port 19903 tests/symdumcicsrestapi  -v
