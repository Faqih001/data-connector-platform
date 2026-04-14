# Login Flow Debug Guide

## 🔍 Why Does It Auto-Login After Page Refresh?

This is **EXPECTED BEHAVIOR** for a session-based authentication system. Here's how it works:

### The Flow:
1. **User logs in** → Frontend calls `/api/login/` with credentials
2. **Backend authenticates** → Validates username/password, calls Django's `login()` function
3. **Session created** → Django creates session and sets `Set-Cookie: sessionid=...` in response headers
4. **Cookie stored** → Browser automatically stores this session cookie
5. **Page refresh** → Browser sends stored session cookie with each request (credentials: 'include')
6. **Auto-login check** → Frontend's `useEffect` calls `/api/user/` with the stored cookie
7. **Backend validates** → Session is still valid, returns user data
8. **User state restored** → Frontend sets `isLoggedIn=true` with user data

### Why This Happens:
- **Session cookies are persistent** across page refreshes
- **This is good security** - user doesn't have to re-enter password
- **Session expires** based on Django settings (default: 2 weeks of inactivity)

## 🐛 Issues to Fix

### Issue 1: Logout Returns 403 CSRF Error
- **Problem**: Logout endpoint has `@csrf_exempt` but still returns 403
- **Cause**: Django's CSRF middleware might be intercepting POST requests
- **Solution**: Ensure csrf_exempt is properly applied before api_view decorator

### Issue 2: Login Might Have CSRF Issues  
- **Problem**: Browser-based login would fail with CSRF token missing error
- **Cause**: Django CSRF middleware is now enabled, but frontend isn't sending CSRF token
- **Solution**: Frontend should fetch CSRF token before login, OR endpoints use `@csrf_exempt`

## Testing Commands

### Test 1: Login and Get Session Cookie
```bash
curl -c /tmp/cookies.txt -X POST http://localhost:8001/api/login/ \
  -d '{"username":"admin","password":"admin123"}' \
  -H "Content-Type: application/json"
```

### Test 2: Check Session is Valid
```bash
curl -b /tmp/cookies.txt http://localhost:8001/api/user/ 
# Should return user data
```

### Test 3: Logout
```bash
curl -b /tmp/cookies.txt -X POST http://localhost:8001/api/logout/ \
  -H "Content-Type: application/json"
```

### Test 4: Check Session is Cleared
```bash
curl -b /tmp/cookies.txt http://localhost:8001/api/user/
# Should return 401 Unauthorized
```

## Configuration Status

### Current Settings:
- CSRF Middleware: **ENABLED** ✓
- csrf_exempt on login: **YES** ✓
- csrf_exempt on logout: **YES** ✓
- CSRF_COOKIE_HTTPONLY: **False** (allows JS access)
- CSRF_TRUSTED_ORIGINS: **Configured for localhost**

### Possible Issues:
1. Decorator order might matter (@csrf_exempt before @api_view)
2. DRF might have its own CSRF handling
3. Session cookie might not have proper path/domain settings
