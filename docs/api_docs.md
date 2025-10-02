# **MoMo SMS Transaction REST API**
---

## Table of Contents
1. Abstract 
2. Features   
3. API Endpoints Overview
4. Authentication & Security  
5. Testing & Validation  
6. Reflection on Basic Auth  
7. Credits & Acknowledgements

---

## 1. ABSTARCT

This **MoMo SMS Transaction API** we created, allows clients or other developers to securely access mobile money SMS records. It supports complete CRUD operations over HTTP, uses JSON formatting, and is protected using Basic Authentication. The API also integrates efficient data structures for faster access and lookup.

---

## 2. FEATURES

- Full CRUD operations (Create, Read, Update, Delete)  
- JSON-based responses  
- XML data parsed into structured JSON  
- Basic Authentication for all endpoints  
- DSA integration: Linear search vs Dictionary lookup  
- Fully tested in Postman with screenshots


## 3. API ENDPOINTS Overview

### GET /transactions

Returns all transactions.

- **Auth Required:** Yes (Basic Auth)  
- **Response:**
```json
[
  {
    "id": 1,
    "type": "Deposit",
    "amount": 1500.0,
    "sender": "123456789",
    "receiver": "998877665",
    "timestamp": "2024-09-27T08:30:00Z"
  },
  ...
]
```



### GET /transactions/{id}

Returns a specific transaction by ID.

- **Success Response:**
```json
{
  "id": 24,
  "type": "Deposit",
  "amount": 1500.0,
  "sender": "123456789",
  "receiver": "998877665",
  "timestamp": "2024-09-27T08:30:00Z"
}
```

- **Error (404):** when you happen to enter invalid ID
```json
{ "error": "Transaction not found" }
```



### POST /transactions

Creates a new transaction.

- **Request Body:**
```json
{
  "type": "Deposit",
  "amount": 1500.0,
  "sender": "123456789",
  "receiver": "998877665",
  "timestamp": "2024-09-27T08:30:00Z"
}
```

- **Response:**
```json
{
  "id": 24,
  "type": "Deposit",
  "amount": 1500.0,
  "sender": "123456789",
  "receiver": "998877665",
  "timestamp": "2024-09-27T08:30:00Z"
}
```



### PUT /transactions/{id}

Updates a transaction (e.g., amount).

- **Request Body:**
```json
{
  "amount": 2500.0
}
```

- **Response:**
```json
{
  "id": 24,
  "type": "Deposit",
  "amount": 2500.0,
  "sender": "123456789",
  "receiver": "998877665",
  "timestamp": "2024-09-27T08:30:00Z"
}
```



### DELETE /transactions/{id}

Deletes a transaction.

- **Response:**  
`204 No Content` (success)



## 4. AUTHENTICATION & SECURITY

All endpoints are protected using **Basic Authentication**.

### How to use in Postman:

- Go to the **Authorization** tab  
- Choose **Basic Auth**  
- Enter your `username` and `password` in our case username is **admin** and passcode is **secret** with base

### Unauthorized Request:

```json
{ "error": "Unauthorized" }
```

### Why Basic Auth is Weak:

- Credentials are Base64 encoded, not encrypted  
- Reused on every request  
- No session management or token revocation  

### Recommended Alternatives:

- **JWT (JSON Web Tokens)**  
- **OAuth 2.0**



## 5. TESTING & VALIDATION

Tested using **Postman**. Summary:

| Method & Endpoint         | Result              | Screenshot             |
|---------------------------|---------------------|------------------------|
| GET /transactions         | 200 OK           | ![WhatsApp Image 2025-10-02 at 19 30 22_d625b97a](https://github.com/user-attachments/assets/35966df0-3db3-466b-99d5-0e851f72985b)
  
| POST /transactions        | 201 Created      | ![WhatsApp Image 2025-10-02 at 19 30 31_b62791db](https://github.com/user-attachments/assets/13debee9-576e-48d6-aaa5-4702d5c6612e)

| GET /transactions/24      | 200 OK           | ![WhatsApp Image 2025-10-02 at 19 31 42_9b046b5f](https://github.com/user-attachments/assets/2f520a84-01c1-49cc-ac24-ef097935a97f)
  
| DELETE /transactions/24   | 204 No Content   | ![WhatsApp Image 2025-10-02 at 19 32 10_fd178554](https://github.com/user-attachments/assets/ea1f7a4b-a09e-4cf2-88c1-ee334f648200)
 
| GET /transactions/21      | 404 Not Found    | ![WhatsApp Image 2025-10-02 at 19 31 06_f640391e](https://github.com/user-attachments/assets/c7aca163-8914-444b-84da-9e5582ac2d39)

| GET without auth          | 401 Unauthorized | ![WhatsApp Image 2025-10-02 at 19 30 07_c3de7770](https://github.com/user-attachments/assets/7fae1c29-11cf-4f19-b983-785bc379ebdc)




## 6. Data Structures & Algorithms (DSA Integration)

To optimize the efficiency of retrieving transactions by ID, two different search approaches were implemented and evaluated:

### Linear Search
- Iterates through each transaction in a list until a match is found.
- **Time Complexity:** O(n)  
- Suitable for small datasets but becomes slow as the number of records increases.

### Dictionary Lookup
- Creates an index mapping each transaction's ID to its data using a dictionary.
- **Time Complexity:** O(1) average case  
- Significantly faster due to direct key access via hashing.


### Performance Test (20+ Records)

A benchmark was conducted with at least 20 transaction records. Each method was executed multiple times to compare their average time taken.

| Search Method     | Avg Time (ms) |
|-------------------|----------------|
| Linear Search     | ~15 ms         |
| Dictionary Lookup | ~1 ms          |

Dictionary lookup is approximately **10–15x faster** than linear search on average._



### Reflection

**Why is dictionary lookup faster?**  
Because Python dictionaries are implemented as hash tables, allowing near-instant access to elements using keys. Linear search, on the other hand, must check each item one by one, making it less efficient as the dataset grows.

**Other data structures that could improve search efficiency:**
- **Binary Search Tree (BST):** Useful for sorted data; O(log n) search time.
- **Trie:** Efficient for prefix-based searches (e.g., phone numbers).
- **B-Tree or Hash Map with LRU Caching:** For large datasets or disk-based storage.



## 7. REFLECTION ON BASIC AUTH

While **Basic Auth** is simple and easy to implement, it is:

- Not secure without HTTPS  
- Lacks token/session management  
- Vulnerable to interception

### Recommended Upgrade:

- **JWT** for stateless sessions  
- **OAuth 2.0** for delegated access



## 8. CREDITS & ACKNOWLEDGEMENTS

- Testing Tool: [Postman](https://www.postman.com)  
- Dataset: [modified_sms_v2.xml]([url](https://github.com/rcyubahiro/momo-sms-dashboard/blob/main/modified_sms_v2.xml))  or https://github.com/rcyubahiro/momo-sms-dashboard/blob/main/modified_sms_v2.xml

