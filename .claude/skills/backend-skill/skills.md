---
name: backend-skill
description: Build backend systems with routes, request/response handling, and database connectivity.
---

# Backend Skill

## Instructions

1. **Route generation**
   - Create RESTful routes for resources (GET, POST, PUT, DELETE)
   - Organize routes by feature or module
   - Use controllers or handlers to separate logic
   - Apply middleware for authentication and validation

2. **Request & response handling**
   - Parse request body, params, and query safely
   - Validate incoming data before processing
   - Send structured JSON responses with status codes
   - Handle errors using centralized error middleware

3. **Database connection**
   - Configure secure database connection using environment variables
   - Use ORM or query builder for database operations
   - Implement CRUD operations for core entities
   - Manage connection pooling and graceful shutdown

4. **Scalability & structure**
   - Follow MVC or modular architecture
   - Keep business logic separate from routes
   - Implement logging and monitoring
   - Prepare codebase for testing and deployment

## Best Practices
- Use consistent API naming conventions
- Never expose sensitive data in responses
- Return proper HTTP status codes
- Sanitize and validate all inputs
- Use async/await with proper error handling
- Keep controllers thin and services reusable

## Example Structure

```ts
// route
app.post("/users", async (req, res) => {
  try {
    const { email, password } = req.body;

    // create user in DB
    const user = await db.user.create({ data: { email, password } });

    res.status(201).json({ success: true, data: user });
  } catch (error) {
    res.status(500).json({ success: false, message: "Server error" });
  }
});

// database connection
await db.$connect();
