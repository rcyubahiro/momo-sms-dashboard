# MoMo SMS Transaction API Documentation

Base URL: `http://localhost:8080`

## Security

All endpoints require **Basic Authentication** with the username `admin` and password `secret`.

### Error Codes

| Code | Meaning | Description |
| :--- | :--- | :--- |
| `200` | OK | The request was successful. |
| `201` | Created | The resource was successfully created (POST). |
| `204` | No Content | The request was successful, but no content is returned (e.g., DELETE). |
| `400` | Bad Request | The request was malformed (e.g., invalid JSON, missing fields). |
| `401` | Unauthorized | Authentication failed (invalid/missing credentials). |
| `404` | Not Found | The requested resource or endpoint does not exist. |

***

## 1. List All Transactions

Retrieves a list of all mobile money transactions.

| Attribute | Value |
| :--- | :--- |
| **Endpoint** | `/transactions` |
| **Method** | `GET` |

**Request Example:**

```bash
curl -X GET http://localhost:8080/transactions -H "Authorization: Basic YWRtaW46c2VjcmV0"
