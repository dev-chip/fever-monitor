

# import modules
import unittest
import os

# define tests location
TESTS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == "__main__":
    # load tests
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir=TESTS_PATH, pattern="tst_*.py")
    # runs tests and output results
    testRunner = unittest.runner.TextTestRunner()
    testRunner.run(tests)
