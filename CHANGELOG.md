# Changelog

All notable changes to this project will be documented here.
Follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.0] - 2024-03-21
### Added
- JWT authentication module with token creation and verification
- Redis and in-memory rate limiting (sliding window algorithm)
- Response caching with Redis and in-memory backends
- Structured JSON logging and `@timed` decorator
- Security headers middleware (CSP, X-Frame-Options, XSS, Referrer-Policy)
- Cursor-based and offset pagination utilities
- Input validation helpers (email, phone, slug, URL)
- Structured error handlers for HTTP 4xx/5xx and validation errors
- Health check endpoint (`GET /health`)
- Docker multi-stage build with non-root user
- docker-compose with Redis, Prometheus, and Grafana
- GitHub Actions CI: lint, typecheck, test (multi-python), security scan, Docker build
