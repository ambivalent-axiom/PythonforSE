.PHONY: start star_build stop unit_tests

UNIT_TESTS=pytest tests --asyncio-mode=strict

start:
	@docker-compose up -d

start_build:
	@docker-compose up --build -d

stop:
	@docker-compose down

unit_tests:
	@docker-compose exec -T app-test $(UNIT_TESTS)

unit_tests_local:
	@$(UNIT_TESTS)

check_lint:
	@docker-compose exec app-test mypy . && isort --check-only && black --check && flake8 app models tests

fix_lint:
	@docker-compose exec app-test isort . && black .
