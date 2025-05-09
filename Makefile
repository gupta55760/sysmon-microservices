# Run Selenium GUI tests (sequential)
test-selenium:
	@echo "Running Selenium tests..."
	@mkdir -p tests/reports/selenium
	@bash -c 'pytest tests/gui/selenium \
	  --html=tests/reports/selenium/report.html \
	  --self-contained-html -rA $(TEST_ARGS) \
	  | tee tests/reports/selenium/full_log.txt && \
	  grep -A 10 "short test summary info" tests/reports/selenium/full_log.txt | tail -n 20 > tests/reports/selenium/summary.txt || echo "No summary generated."'

# Run Selenium GUI tests in parallel
test-selenium-parallel:
	@echo "Running Selenium tests in parallel..."
	@mkdir -p tests/reports/selenium
	@bash -c 'pytest -n auto tests/gui/selenium \
	  --html=tests/reports/selenium/report.html \
	  --self-contained-html -rA $(TEST_ARGS) \
	  | tee tests/reports/selenium/full_log.txt && \
	  grep -A 10 "short test summary info" tests/reports/selenium/full_log.txt | tail -n 20 > tests/reports/selenium/summary.txt || echo "No summary generated."'

# Run Playwright tests (sequential)
test-playwright:
	@echo "Running Playwright tests..."
	@mkdir -p tests/reports/logs
	@npx playwright test tests/gui/playwright > tests/reports/logs/full_log.txt 2>&1 || true
	@echo "Finished test run. Extracting summary..."
	@mkdir -p tests/reports/playwright/logs
	@grep -E "✓|✘|passed|failed|PASS|FAIL" tests/reports/logs/full_log.txt > tests/reports/playwright/logs/summary.txt || touch tests/reports/playwright/logs/summary.txt
	@echo "Test Summary:"
	@cat tests/reports/playwright/logs/summary.txt

# Run Playwright tests in parallel (explicit workers)
test-playwright-parallel:
	@echo "Running Playwright tests in parallel..."
	@mkdir -p tests/reports/logs
	@npx playwright test tests/gui/playwright --workers=4 $(TEST_ARGS) > tests/reports/logs/full_log.txt 2>&1 || true
	@mkdir -p tests/reports/playwright/logs
	@grep -E "✓|✘|passed|failed" tests/reports/logs/full_log.txt > tests/reports/playwright/logs/summary.txt || touch tests/reports/playwright/logs/summary.txt 
	@echo "Test Summary:"
	@cat tests/reports/playwright/logs/summary.txt

# Run API tests (sequential)
test-api:
	@echo "Running API tests..."
	@mkdir -p tests/reports/api
	@bash -c 'pytest tests/api \
	  --html=tests/reports/api/report.html \
	  --self-contained-html -rA $(TEST_ARGS) \
	  | tee tests/reports/api/full_log.txt && \
	  grep -A 10 "short test summary info" tests/reports/api/full_log.txt | tail -n 20 > tests/reports/api/summary.txt || echo "No summary generated."'

# Run API tests in parallel
test-api-parallel:
	@echo "Running API tests in parallel..."
	@mkdir -p tests/reports/api
	@bash -c 'pytest -n auto tests/api \
	  --html=tests/reports/api/report.html \
	  --self-contained-html -rA $(TEST_ARGS) \
	  | tee tests/reports/api/full_log.txt && \
	  grep -A 10 "short test summary info" tests/reports/api/full_log.txt | tail -n 20 > tests/reports/api/summary.txt || echo "No summary generated."'

# Clean old reports
clean-reports:
	rm -rf tests/reports/selenium/* tests/reports/playwright/* tests/reports/api/*

# Run all suites sequentially
test-all: clean-reports test-selenium test-playwright test-api
	@echo "✅ All tests complete. Summaries saved."

# Run all suites in parallel (background jobs)
test-all-parallel:
	@echo "Running all suites in parallel..."
	@mkdir -p tests/reports/selenium tests/reports/playwright tests/reports/api
	$(MAKE) test-selenium TEST_ARGS="$(TEST_ARGS)" & \
	$(MAKE) test-playwright TEST_ARGS="$(TEST_ARGS)" & \
	$(MAKE) test-api TEST_ARGS="$(TEST_ARGS)" & \
	wait
	@echo "✅ All suites completed (parallel)."

# Run all suites in parallel using worker-based concurrency
test-all-parallel-workers:
	@echo "Running all suites in parallel (using workers)..."
	@mkdir -p tests/reports/selenium tests/reports/playwright tests/reports/api
	$(MAKE) test-selenium-parallel TEST_ARGS="$(TEST_ARGS)" & \
	$(MAKE) test-playwright-parallel TEST_ARGS="$(TEST_ARGS)" & \
	$(MAKE) test-api-parallel TEST_ARGS="$(TEST_ARGS)" & \
	wait
	@echo "✅ All worker-based parallel test suites completed."

.PHONY: test-selenium test-selenium-parallel test-playwright test-playwright-parallel test-api test-api-parallel clean-reports test-all test-all-parallel test-all-parallel-workers

