# Serverless Transaction Analyzer

A small AWS Lambda-based application that analyzes transaction data stored in Amazon S3 and presents category totals through a web interface.

## Architecture

- A web-facing Lambda function serves the interface.
- Transaction content is stored in Amazon S3.
- A Python Lambda function parses the data and calculates totals.
- API endpoints connect the browser interface to the backend.
- The UI presents transaction details and a category breakdown.

## Repository contents

- `html.py` — web response/interface function
- `calculation.py` — transaction parsing and aggregation logic

## Deployment considerations

Before deploying your own copy:

1. Create private S3 storage for uploaded transaction data.
2. Give each Lambda function only the permissions it requires.
3. Configure API authentication, request validation, and CORS.
4. Store bucket names and other environment-specific values in configuration.
5. Enable structured logs while avoiding sensitive transaction content.
6. Add retention and deletion controls for uploaded files.

## Privacy and security

Transaction data is sensitive. Do not use public buckets or unauthenticated write endpoints, and do not log raw financial records. Treat the included public endpoints as demonstration infrastructure that may be unavailable or unsuitable for real data.

> This project is a serverless proof of concept, not financial or accounting software.
