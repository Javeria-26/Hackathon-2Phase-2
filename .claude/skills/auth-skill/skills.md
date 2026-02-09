---
name: auth-skill
description: Implement secure authentication including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **Core authentication flow**
   - User signup with validation
   - Secure user signin process
   - Session/token-based authentication
   - Proper error handling and responses

2. **Security implementation**
   - Hash passwords using bcrypt or argon2
   - Never store plain text passwords
   - Use environment variables for secrets
   - Protect routes with authentication middleware

3. **JWT token handling**
   - Generate JWT after successful login
   - Include user ID and minimal payload
   - Set expiration time for tokens
   - Verify tokens for protected endpoints

4. **Better Auth integration**
   - Configure Better Auth provider
   - Use built-in session and token management
   - Connect database adapter correctly
   - Enable secure cookie and CSRF protection

## Best Practices
- Validate all user input
- Use HTTPS in production
- Keep JWT secret secure and rotated
- Implement refresh tokens for long sessions
- Apply rate limiting on auth routes
- Follow least-privilege access control

## Example Structure

```ts
// signup
const hashedPassword = await bcrypt.hash(password, 10);

// signin
const isValid = await bcrypt.compare(password, user.password);

// generate JWT
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: "1h" }
);

// middleware protection
const decoded = jwt.verify(token, process.env.JWT_SECRET);
