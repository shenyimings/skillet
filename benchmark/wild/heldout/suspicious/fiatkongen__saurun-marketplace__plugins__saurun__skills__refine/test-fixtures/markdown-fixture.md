# API Gateway Configuration Guide

## Overview

This document describes how to configure the API gateway for our application. The gateway handles all incoming requests and routes them to the appropriate microservice. The API gateway is responsible for routing requests to the correct service.

## Setup

### Prerequisites

- Node.js 18+
- Docker installed
- Access to the configuration repository

### Installation

1. Clone the repo
2. Run `npm install`
3. Configure the environment variables appropriately
4. Start the gateway

## Configuration

The gateway uses a YAML config file located at `config/gateway.yml`. See the [Configuration Reference](#configuration-reference) for all available options.

### Rate Limiting

Rate limiting can be configured per-route or globally. The system supports both fixed-window and sliding-window algorithms.

- Configure rate limits in the config file
- Set the window size
- Define the max requests per window
- Set the burst limit

TODO: decide on default rate limit values for production

### Authentication

The gateway supports multiple authentication methods:

* JWT tokens
* API keys
- OAuth2
- Basic auth (deprecated)

Users should authenticate using the appropriate method. When a client sends a request, the gateway validates the token and forwards the request to the downstream service. Customers who need higher rate limits can request an API key upgrade.

### Routing

Routes are defined in the configuration file. Each route specifies:

1. The path pattern
2. The target service
3. Any middleware to apply

The routing engine supports path parameters, query string matching, and header-based routing. The routing system also handles path parameters and query strings.

### Error Handling

When an error occurs, the gateway should handle it properly. Errors from downstream services are forwarded to the client with appropriate status codes.

For 5xx errors:
- Log the error
- Return a generic error message
- etc.

### Monitoring

The gateway exposes metrics at `/metrics` endpoint. See the [Monitoring Setup](#monitoring-dashboard) section for Grafana dashboard configuration.

Health checks are available at:

- `/health`

## Deployment

### Staging

Deploy to staging using the standard deployment process. Make sure to update the config as needed.

### Production

Production deployment requires approval from the team lead. The deployment pipeline will:

1. Run tests
2. Build the Docker image
3. Deploy to k8s
4. Run smoke tests

NOTE: Production deployments should never happen on Fridays.

FIXME: automate the approval workflow

### Rollback

In case of issues, rollback to the previous version. The rollback process should work correctly in all cases.

## Troubleshooting

### Common Issues

If the gateway is not responding:

1. Check the logs
2. Verify the configuration
3. Restart the service

If authentication is failing, verify that the JWT secret matches between the gateway and the identity provider. Ensure the customer's token has not expired.

## Configuration Reference Guide

| Option | Type | Description |
|--------|------|-------------|
| `port` | number | The port to listen on |
| `logLevel` | string | Log level (debug, info, warn, error) |
| `rateLimit.window` | number | Rate limit window in ms |
| `rateLimit.max` | number | Max requests per window |
| `auth.jwtSecret` | string | Secret for JWT validation |
| `auth.apiKeyHeader` | string | Header name for API keys |

## Appendix

For more information, contact the platform team.
