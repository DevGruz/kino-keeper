.PHONY: test

test:
	@echo "Starting test environment..."
	@docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit > /dev/null 2>&1
	@docker-compose -f docker-compose.test.yml logs kino-keeper-app-test
	@docker-compose -f docker-compose.test.yml down > /dev/null 2>&1
	@echo "Test environment stopped."
