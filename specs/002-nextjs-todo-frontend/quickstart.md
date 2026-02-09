# Quickstart Guide: Next.js Todo Frontend

**Date**: 2026-02-08
**Feature**: 002-nextjs-todo-frontend
**Purpose**: Setup and development instructions for the Next.js Todo Frontend application

---

## Prerequisites

Before starting development, ensure you have the following installed:

- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 9.0.0 or higher (comes with Node.js)
- **Git**: For version control
- **Code Editor**: VS Code recommended with TypeScript and ESLint extensions
- **Modern Browser**: Chrome, Firefox, Safari, or Edge (latest version)

**Optional**:
- **Backend API**: FastAPI backend running (or use mock API for development)
- **Database**: Neon PostgreSQL (accessed via backend)

---

## Initial Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Checkout the frontend feature branch
git checkout 002-nextjs-todo-frontend
```

### 2. Navigate to Frontend Directory

```bash
cd frontend
```

### 3. Install Dependencies

```bash
# Install all npm packages
npm install

# This will install:
# - Next.js 16+
# - React 18+
# - Better Auth
# - TypeScript
# - Development dependencies (Jest, Testing Library, ESLint)
```

**Expected Installation Time**: 2-3 minutes

### 4. Environment Configuration

```bash
# Copy the environment template
cp .env.example .env.local

# Open .env.local in your editor
```

**Configure the following environment variables**:

```bash
# .env.local

# Backend API URL (required)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration (required)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_SECRET=your-secret-key-here-min-32-characters

# Optional: Development settings
NODE_ENV=development
```

**Environment Variable Descriptions**:

- `NEXT_PUBLIC_API_URL`: Base URL for the FastAPI backend
  - Development: `http://localhost:8000`
  - Production: Your deployed backend URL

- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth API endpoint
  - Development: `http://localhost:3000/api/auth`
  - Production: `https://yourdomain.com/api/auth`

- `BETTER_AUTH_SECRET`: Secret key for JWT signing (minimum 32 characters)
  - Generate with: `openssl rand -base64 32`
  - **IMPORTANT**: Use different secrets for dev/staging/production

**Security Notes**:
- Never commit `.env.local` to version control
- Use strong, unique secrets for each environment
- Rotate secrets regularly in production

---

## Development

### Start Development Server

```bash
# Start Next.js development server
npm run dev
```

**Output**:
```
> frontend@1.0.0 dev
> next dev

- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully in 2.5s
```

**Access the application**:
- Open browser to: `http://localhost:3000`
- Hot reload enabled - changes reflect automatically

### Development Workflow

1. **Start Backend API** (if available):
   ```bash
   # In a separate terminal
   cd ../backend
   uvicorn main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   npm run dev
   ```

3. **Make Changes**:
   - Edit files in `app/`, `components/`, or `lib/`
   - Save changes - browser auto-refreshes
   - Check console for errors

4. **Test Changes**:
   - Manual testing in browser
   - Run automated tests: `npm test`

---

## Available Commands

### Development Commands

```bash
# Start development server with hot reload
npm run dev

# Build production bundle
npm run build

# Start production server (requires build first)
npm start

# Run development and production builds
npm run build && npm start
```

### Testing Commands

```bash
# Run all tests once
npm test

# Run tests in watch mode (re-runs on file changes)
npm test -- --watch

# Run tests with coverage report
npm test -- --coverage

# Run specific test file
npm test -- LoginForm.test.tsx
```

### Code Quality Commands

```bash
# Run ESLint to check code quality
npm run lint

# Run ESLint and auto-fix issues
npm run lint -- --fix

# Run TypeScript type checking
npm run type-check

# Format code with Prettier (if configured)
npm run format
```

### Build Commands

```bash
# Create optimized production build
npm run build

# Analyze bundle size
npm run build -- --analyze

# Clean build artifacts
rm -rf .next
```

---

## Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page
│   ├── (auth)/                  # Public routes
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (protected)/             # Protected routes
│   │   ├── layout.tsx
│   │   └── dashboard/page.tsx
│   └── api/                     # API routes
│       └── auth/[...auth]/route.ts
├── components/                   # React components
│   ├── auth/                    # Auth components
│   ├── todo/                    # Todo components
│   ├── ui/                      # UI components
│   └── layout/                  # Layout components
├── lib/                         # Utilities and libraries
│   ├── auth/                    # Auth utilities
│   ├── api/                     # API client
│   └── utils/                   # General utilities
├── types/                       # TypeScript types
├── styles/                      # Global styles
├── public/                      # Static assets
├── tests/                       # Test files
├── .env.local                   # Environment variables (not committed)
├── .env.example                 # Environment template
├── next.config.js               # Next.js configuration
├── tsconfig.json                # TypeScript configuration
├── package.json                 # Dependencies
└── README.md                    # Project documentation
```

---

## First-Time Setup Checklist

- [ ] Node.js 18+ installed
- [ ] Repository cloned
- [ ] Dependencies installed (`npm install`)
- [ ] Environment variables configured (`.env.local`)
- [ ] Backend API running (or mock API configured)
- [ ] Development server started (`npm run dev`)
- [ ] Application accessible at `http://localhost:3000`
- [ ] Can register a new user account
- [ ] Can log in with registered account
- [ ] Can access dashboard after login

---

## Common Development Tasks

### Create a New Component

```bash
# Create component file
touch components/todo/NewComponent.tsx

# Create component test file
touch tests/components/todo/NewComponent.test.tsx
```

**Component Template**:
```typescript
// components/todo/NewComponent.tsx
import React from 'react'

interface NewComponentProps {
  // Define props
}

export default function NewComponent({ }: NewComponentProps) {
  return (
    <div>
      {/* Component content */}
    </div>
  )
}
```

### Add a New Route

```bash
# Create new route directory
mkdir -p app/new-route

# Create page file
touch app/new-route/page.tsx
```

**Page Template**:
```typescript
// app/new-route/page.tsx
export default function NewRoutePage() {
  return (
    <div>
      <h1>New Route</h1>
    </div>
  )
}
```

### Add API Client Method

```typescript
// lib/api/todos.ts
export const todoApi = {
  // Add new method
  newMethod: async (userId: string, data: any) => {
    return client.post(`/api/${userId}/new-endpoint`, data)
  }
}
```

---

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Writing Tests

**Component Test Example**:
```typescript
// tests/components/todo/TodoItem.test.tsx
import { render, screen } from '@testing-library/react'
import TodoItem from '@/components/todo/TodoItem'

describe('TodoItem', () => {
  it('renders todo title', () => {
    const todo = {
      id: '1',
      title: 'Test Todo',
      description: 'Test description',
      completed: false,
      userId: 'user1',
      createdAt: '2026-02-08T10:00:00Z',
      updatedAt: '2026-02-08T10:00:00Z'
    }

    render(<TodoItem todo={todo} />)
    expect(screen.getByText('Test Todo')).toBeInTheDocument()
  })
})
```

### Test Coverage Goals

- **Overall Coverage**: > 80%
- **Critical Paths**: > 90% (auth, API client)
- **Components**: > 75%
- **Utilities**: > 85%

---

## Debugging

### Browser DevTools

1. **Open DevTools**: F12 or Right-click → Inspect
2. **Console Tab**: View console.log output and errors
3. **Network Tab**: Monitor API requests and responses
4. **React DevTools**: Install extension for component inspection

### Common Issues

**Issue**: "Module not found" error
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Issue**: Port 3000 already in use
```bash
# Solution: Use different port
PORT=3001 npm run dev
```

**Issue**: Environment variables not loading
```bash
# Solution: Restart dev server after changing .env.local
# Stop server (Ctrl+C) and restart
npm run dev
```

**Issue**: TypeScript errors
```bash
# Solution: Run type check to see all errors
npm run type-check
```

**Issue**: API requests failing with CORS errors
```bash
# Solution: Ensure backend has CORS configured for http://localhost:3000
# Check backend CORS settings
```

---

## Building for Production

### Create Production Build

```bash
# Build optimized production bundle
npm run build
```

**Build Output**:
```
Route (app)                              Size     First Load JS
┌ ○ /                                    1.2 kB         85.3 kB
├ ○ /login                               2.5 kB         87.6 kB
├ ○ /register                            2.5 kB         87.6 kB
└ ● /dashboard                           5.8 kB         91.9 kB

○  (Static)  automatically rendered as static HTML
●  (SSG)     automatically generated as static HTML + JSON
```

### Test Production Build Locally

```bash
# Build and start production server
npm run build
npm start

# Access at http://localhost:3000
```

### Production Checklist

- [ ] All tests passing (`npm test`)
- [ ] No TypeScript errors (`npm run type-check`)
- [ ] No ESLint errors (`npm run lint`)
- [ ] Environment variables configured for production
- [ ] HTTPS enabled
- [ ] Backend API URL updated to production
- [ ] Better Auth secret is production-specific
- [ ] Build completes successfully
- [ ] Production server starts without errors

---

## Deployment

### Vercel Deployment (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to Vercel
vercel

# Follow prompts to configure deployment
```

**Environment Variables in Vercel**:
1. Go to Project Settings → Environment Variables
2. Add all variables from `.env.local`
3. Set different values for Production/Preview/Development

### Alternative Deployment Options

**Netlify**:
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod
```

**Docker**:
```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## Troubleshooting

### Development Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Use `PORT=3001 npm run dev` |
| Module not found | Run `npm install` |
| TypeScript errors | Run `npm run type-check` |
| Build fails | Check for syntax errors, run `npm run lint` |
| Hot reload not working | Restart dev server |

### Authentication Issues

| Issue | Solution |
|-------|----------|
| Login fails | Check backend API is running, verify credentials |
| Token expired | Logout and login again |
| Redirect loop | Clear browser cookies and localStorage |
| CORS errors | Check backend CORS configuration |

### API Issues

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check JWT token is valid, re-login |
| 403 Forbidden | Verify user_id matches authenticated user |
| 404 Not Found | Check API endpoint URL is correct |
| Network error | Verify backend is running, check NEXT_PUBLIC_API_URL |

---

## Performance Optimization

### Development Performance

- Use `npm run dev -- --turbo` for faster builds (if available)
- Disable source maps in development if slow: `GENERATE_SOURCEMAP=false npm run dev`
- Close unused browser tabs to reduce memory usage

### Production Performance

- Enable Next.js image optimization
- Use dynamic imports for large components
- Implement code splitting for routes
- Enable compression in production server
- Use CDN for static assets

---

## Additional Resources

### Documentation

- **Next.js Docs**: https://nextjs.org/docs
- **React Docs**: https://react.dev
- **Better Auth Docs**: https://better-auth.com/docs
- **TypeScript Docs**: https://www.typescriptlang.org/docs

### Project Documentation

- **Specification**: `specs/002-nextjs-todo-frontend/spec.md`
- **Implementation Plan**: `specs/002-nextjs-todo-frontend/plan.md`
- **Research Findings**: `specs/002-nextjs-todo-frontend/research.md`
- **Data Models**: `specs/002-nextjs-todo-frontend/data-model.md`
- **API Contracts**: `specs/002-nextjs-todo-frontend/contracts/api-client.md`

### Getting Help

- Check project documentation in `specs/` directory
- Review error messages in browser console
- Check Network tab for API request/response details
- Run `npm run type-check` for TypeScript errors
- Run `npm run lint` for code quality issues

---

## Next Steps

After completing the quickstart setup:

1. **Familiarize with codebase**: Review project structure and key files
2. **Run tests**: Ensure all tests pass with `npm test`
3. **Review documentation**: Read spec.md and plan.md
4. **Start development**: Begin implementing tasks from tasks.md
5. **Test frequently**: Run tests after each significant change
6. **Commit regularly**: Commit working code with clear messages

---

**Status**: Quickstart guide complete, ready for development
