# Research: Neon PostgreSQL Integration

**Feature**: 001-neon-postgres-todos
**Date**: 2026-02-09
**Purpose**: Research findings for Neon Serverless PostgreSQL integration with SQLModel

## Research Questions

### 1. Neon PostgreSQL Connection Patterns

**Question**: What are the best practices for connecting to Neon Serverless PostgreSQL from Python?

**Findings**:
- **Connection String Format**: `postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require`
- **SSL Requirement**: Neon requires SSL connections (`sslmode=require` parameter mandatory)
- **Serverless Considerations**: Neon automatically scales connections, but client-side pooling still recommended
- **Connection Lifecycle**: Neon may close idle connections after timeout (typically 5 minutes)

**Decision**: Use asyncpg driver with SSL enabled and connection pooling to handle serverless behavior.

---

### 2. SQLModel + PostgreSQL Async Driver Selection

**Question**: Which async PostgreSQL driver works best with SQLModel and SQLAlchemy 2.0?

**Findings**:
- **asyncpg**: Fastest Python PostgreSQL driver, native SQLAlchemy 2.0 support, mature and stable
- **psycopg3**: Newer driver with async support, but less mature than asyncpg
- **psycopg2**: Synchronous only, not suitable for async FastAPI applications

**Comparison**:
| Feature | asyncpg | psycopg3 | psycopg2 |
|---------|---------|----------|----------|
| Async Support | ✅ Native | ✅ Native | ❌ No |
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| SQLAlchemy 2.0 | ✅ Full | ✅ Full | ⚠️ Limited |
| Maturity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Neon Compatible | ✅ Yes | ✅ Yes | ✅ Yes |

**Decision**: Use asyncpg for best performance and maturity with async operations.

---

### 3. Connection Pooling Strategy

**Question**: What connection pooling configuration is optimal for Neon Serverless?

**Findings**:
- **pool_size**: Number of persistent connections (recommended: 5-10 for serverless)
- **max_overflow**: Additional connections during bursts (recommended: 10-20)
- **pool_pre_ping**: Verify connection health before use (essential for serverless)
- **pool_recycle**: Recycle connections periodically (recommended: 3600 seconds / 1 hour)
- **Neon Limits**: Free tier supports up to 100 concurrent connections

**Best Practices**:
```python
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # Verify connections before use
    pool_size=5,             # Base connection pool
    max_overflow=10,         # Burst capacity
    pool_recycle=3600,       # Recycle after 1 hour
    echo=False               # Disable SQL logging in production
)
```

**Decision**: Use conservative pooling (5+10) to avoid hitting Neon connection limits while maintaining good performance.

---

### 4. Index Strategy for User-Scoped Queries

**Question**: What indexes are needed for efficient user-scoped todo queries?

**Findings**:
- **Primary Index**: Automatic on `id` (UUID primary key)
- **User Filtering**: Index on `user_id` for fast user-scoped queries
- **Ordered Queries**: Composite index on `(user_id, created_at)` for ordered results
- **Query Pattern**: Most queries are `WHERE user_id = ? ORDER BY created_at DESC`

**Index Performance**:
- Single `user_id` index: Good for filtering, requires separate sort
- Composite `(user_id, created_at)` index: Optimal for filtered + ordered queries
- Both indexes: Redundant, composite index covers single-column use case

**Decision**: Use composite index `(user_id, created_at)` to optimize the common query pattern.

---

### 5. UUID vs Integer Primary Keys

**Question**: Should we use UUID or auto-increment integers for primary keys?

**Findings**:

**UUID Advantages**:
- No ID enumeration attacks (security)
- Globally unique across distributed systems
- No collision risk with concurrent inserts
- Can be generated client-side if needed

**UUID Disadvantages**:
- Larger storage (16 bytes vs 4-8 bytes)
- Slightly slower index operations
- Less human-readable

**Integer Advantages**:
- Smaller storage footprint
- Faster index operations
- Sequential, predictable

**Integer Disadvantages**:
- Enables ID enumeration attacks
- Requires database coordination for uniqueness
- Not suitable for distributed systems

**Security Consideration**: ID enumeration allows attackers to guess valid IDs and potentially probe for unauthorized access.

**Decision**: Use UUID for security (prevent enumeration) and distributed system compatibility.

---

### 6. Transaction Isolation Levels

**Question**: What transaction isolation level is appropriate for concurrent todo operations?

**Findings**:
- **PostgreSQL Default**: READ COMMITTED (prevents dirty reads)
- **READ COMMITTED**: Sees only committed data, allows non-repeatable reads
- **REPEATABLE READ**: Prevents non-repeatable reads, may cause serialization errors
- **SERIALIZABLE**: Full isolation, highest overhead

**Concurrent Scenarios**:
1. Two users creating tasks simultaneously: No conflict (different user_id)
2. Same user creating multiple tasks: No conflict (independent inserts)
3. User updating task while another reads: READ COMMITTED handles this safely

**Decision**: Use PostgreSQL default (READ COMMITTED). No need for stricter isolation for todo app use case.

---

### 7. SQLModel Field Validation

**Question**: How should we enforce field length limits and validation?

**Findings**:
- **SQLModel Field Constraints**: `Field(max_length=N)` enforces at Pydantic level
- **Database Constraints**: VARCHAR(N) enforces at database level
- **Custom Validators**: `@field_validator` for complex validation logic

**Validation Strategy**:
```python
class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(default="", max_length=5000)

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

**Decision**: Use SQLModel Field constraints + custom validators for comprehensive validation.

---

### 8. Migration from SQLite to PostgreSQL

**Question**: What changes are needed to migrate from SQLite to PostgreSQL?

**Findings**:

**Connection String Changes**:
- SQLite: `sqlite:///./todos.db`
- PostgreSQL: `postgresql+asyncpg://user:pass@host/db?sslmode=require`

**Type Mapping Differences**:
| SQLModel Type | SQLite | PostgreSQL |
|---------------|--------|------------|
| str | TEXT | VARCHAR |
| int | INTEGER | INTEGER |
| bool | INTEGER (0/1) | BOOLEAN |
| datetime | TEXT (ISO) | TIMESTAMP |
| UUID | TEXT | UUID |

**Async Changes**:
- SQLite: `aiosqlite` driver
- PostgreSQL: `asyncpg` driver
- Engine: `create_async_engine()` (same for both)
- Session: `AsyncSession` (same for both)

**Schema Compatibility**:
- SQLModel abstracts most differences
- UUID handling: PostgreSQL has native UUID type
- Timestamps: PostgreSQL has native TIMESTAMP type

**Decision**: Minimal code changes needed. Update connection string and add asyncpg dependency.

---

## Summary of Key Decisions

| Decision Area | Choice | Rationale |
|--------------|--------|-----------|
| Async Driver | asyncpg | Best performance, mature, native SQLAlchemy 2.0 support |
| Connection Pooling | pool_size=5, max_overflow=10 | Conservative for serverless, avoids connection limits |
| Primary Keys | UUID | Security (no enumeration), distributed system ready |
| Indexes | Composite (user_id, created_at) | Optimizes common query pattern |
| Isolation Level | READ COMMITTED (default) | Sufficient for todo app, no complex transactions |
| Field Validation | SQLModel Field + validators | Comprehensive validation at model level |
| Migration Strategy | Schema recreation | New Neon instance, no production data to migrate |

---

## Implementation Checklist

- [ ] Add asyncpg to requirements.txt
- [ ] Update DATABASE_URL in .env to Neon connection string
- [ ] Configure connection pooling parameters in database.py
- [ ] Add composite index to Todo model
- [ ] Update field validators for title/description
- [ ] Test connection to Neon PostgreSQL
- [ ] Verify SSL connection established
- [ ] Run schema creation (create_db_and_tables)
- [ ] Test CRUD operations with Neon backend
- [ ] Validate query performance (<100ms target)

---

## References

- [Neon Documentation](https://neon.tech/docs)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Connection Pooling](https://www.postgresql.org/docs/current/runtime-config-connection.html)
