#!/bin/bash
# Run tests with coverage

echo "Running tests with coverage..."
pytest tests/ -v --cov=. --cov-report=html --cov-report=term

echo ""
echo "Coverage report generated in htmlcov/index.html"
