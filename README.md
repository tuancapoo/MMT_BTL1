

# 📝Assignment 1- Implement HTTP server

## Task 1: HTTP server with cookie session
- ✅ Cookie-based authentication
- ✅ Session management
- ✅ Access control for protected resources
#### 🏗️ System Architecture
```
┌─────────────────────────────────────────────────┐
│          HTTP Server Layer                      │
│  ┌──────────┐        ┌─────────────┐            │
│  │  Proxy   │───────►│   Backend   │            │
│  │  :8080   │        │   :9000     │            │
│  └──────────┘        └─────────────┘            │
└─────────────────────────────────────────────────┘

```
#### 🚀 How to run

- ##### Step 1: Start Backend Server
```bash
python start_backend.py --server-ip <your-computer-ip> --server-port 9000
```
- ##### Step 2: Start Proxy Server
```bash
python start_proxy.py --server-ip <your-computer-ip> --server-port 8080
```
- #### Step 3: Open your Browser
  -   Open a browser (Incognito mode recommended)
  - Visit: `http://<your-computer-ip>:8080/`
     - ❌  401 Unauthorized (no cookie yet)
  - Visit: `http://<your-computer-ip>:8080/login`
     - ✅ Shows login form
    Login with:
         - Username: `admin`
         - Password: `password`
     - ❌ InValid: 401 Unauthorized (no cookie yet)
     - ✅ Valid: Redirect to `http://<your-computer-ip>:8080/`
  - Visit again: `http://<your-computer-ip>:8080/`
     - ✅ 200 OK (valid cookie)
