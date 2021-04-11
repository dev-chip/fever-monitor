coverage run core\tests\run_tests.py
coverage html --include="core\*" --omit="core\tests\*"
coverage report --include="core\*" --omit="core\tests\*"
del /f .coverage
pause