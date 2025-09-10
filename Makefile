# AkMon Makefile

.PHONY: help install test run demo clean lint format

help:
	@echo "AkMon 可用命令:"
	@echo "  install    - 安装依赖"
	@echo "  test       - 运行测试"
	@echo "  run        - 运行应用"
	@echo "  demo       - 运行演示"
	@echo "  clean      - 清理临时文件"
	@echo "  lint       - 代码检查"
	@echo "  format     - 代码格式化"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v --cov=src/akmon --cov-report=html

run:
	python -m src.akmon.app

demo:
	python run_demo.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -f akmon.log

lint:
	flake8 src/ tests/
	mypy src/akmon/

format:
	black src/ tests/
	isort src/ tests/
