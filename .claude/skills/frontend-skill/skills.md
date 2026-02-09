---
name: frontend-skill
description: Build responsive frontend interfaces including pages, reusable components, layouts, and modern styling.
---

# Frontend Skill

## Instructions

1. **Page structure**
   - Create clear page hierarchy and routing
   - Separate pages by feature or view
   - Ensure semantic HTML structure
   - Support responsive behavior across devices

2. **Component design**
   - Build reusable and modular UI components
   - Manage props, state, and events properly
   - Keep components small and focused
   - Organize components into logical folders

3. **Layout & styling**
   - Use modern CSS approaches (Flexbox, Grid, Tailwind, or CSS Modules)
   - Maintain consistent spacing, typography, and colors
   - Implement responsive breakpoints for mobile-first design
   - Support dark/light themes if required

4. **Interactivity & data handling**
   - Handle user input and form validation
   - Fetch and display API data asynchronously
   - Show loading, empty, and error states
   - Optimize rendering and performance

## Best Practices
- Follow consistent naming conventions
- Avoid deeply nested components
- Reuse styles and UI patterns
- Keep accessibility (ARIA, contrast, keyboard nav) in mind
- Minimize unnecessary re-renders
- Structure project for scalability and maintenance

## Example Structure

```tsx
// reusable component
function Button({ children, onClick }) {
  return (
    <button className="px-4 py-2 rounded bg-blue-600 text-white" onClick={onClick}>
      {children}
    </button>
  );
}

// page layout
export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold">Welcome</h1>
        <Button>Get Started</Button>
      </div>
    </main>
  );
}
