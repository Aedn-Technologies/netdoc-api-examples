# NetDoc Pro — REST API Examples

Sample scripts demonstrating how to query NetDoc Pro's REST API from common scripting environments.

The NetDoc Pro REST API is a Business-tier feature that exposes device and diagram data over a local HTTP endpoint. Use it to integrate NetDoc Pro with Ansible inventories, asset management systems, dashboards, or any custom automation.

## Prerequisites

- NetDoc Pro Business tier installed and licensed on Windows
- REST API enabled in **Top Tool Bar → API → REST API**
- Your bearer token from the REST API settings (treat it like a password)

The API listens on `http://127.0.0.1:9742` by default and binds to loopback only.

## Authentication

Every request must include the bearer token in the `Authorization` header:
