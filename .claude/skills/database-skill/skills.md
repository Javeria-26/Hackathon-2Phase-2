---
name: database-skill
description: Design and manage databases including table creation, migrations, and scalable schema structure.
---

# Database Skill

## Instructions

1. **Table creation**
   - Define clear table names and primary keys
   - Use appropriate data types for each column
   - Add constraints such as NOT NULL, UNIQUE, and DEFAULT
   - Establish relationships using foreign keys

2. **Schema design**
   - Normalize data to reduce duplication
   - Plan one-to-one, one-to-many, and many-to-many relations
   - Use indexing for frequently queried columns
   - Separate authentication, user data, and logs into structured tables

3. **Migrations management**
   - Create version-controlled migration files
   - Apply incremental schema changes safely
   - Include rollback support for failed migrations
   - Keep development and production schemas synchronized

4. **Data integrity & performance**
   - Enforce referential integrity with constraints
   - Optimize queries using indexes and joins
   - Avoid unnecessary columns and large text storage
   - Monitor database size and performance regularly

## Best Practices
- Use consistent naming conventions (snake_case or camelCase)
- Never modify production tables without migrations
- Backup database before structural changes
- Keep migrations small and reversible
- Document schema relationships clearly
- Use environment-based database configurations

##
