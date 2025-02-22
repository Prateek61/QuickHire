# 🎨 QuickHire Frontend

A modern, responsive SvelteKit application with TailwindCSS and Skeleton UI for the QuickHire platform.

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── app.html          # Base HTML template
│   ├── hooks.server.js   # Server-side hooks
│   ├── lib/             # Shared utilities
│   │   ├── auth_store.js  # Authentication state
│   │   ├── components/    # Reusable components
│   │   └── config.js      # App configuration 
│   └── routes/          # Application routes
│       ├── +layout.svelte   # Root layout
│       ├── auth/           # Authentication routes
│       │   ├── login/      # Login page
│       │   └── register/   # Registration page
│       └── (protected)/   # Protected routes
└── static/           # Static assets
```

## ⚙️ Setup and Installation

### Prerequisites

- Node.js 16+
- npm or yarn
- Backend API running

### Installation Steps

```bash
# Install dependencies
npm install

# Start development server
npm run dev -- --open

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔐 Authentication

Authentication is handled through the `auth_store.js` module:

```javascript
// lib/auth_store.js
import { writable } from 'svelte/store';

// Auth store for managing user state
export const authStore = writable({
    user: null,
    token: null,
    isAuthenticated: false,
    isAuthenticating: false
});

// Auth utilities with token management
export function createAuth(customFetch = fetch) {
    return {
        async login(username, password) {
            // Implementation
        },
        async register(userData) {
            // Implementation
        },
        async fetchUser() {
            // Implementation
        },
        // ... other auth methods
    };
}
```

### Using Auth Store

```svelte
<script>
    import { authStore } from '$lib/auth_store';
    
    // Subscribe to auth state
    $: user = $authStore.user;
    $: isAuthenticated = $authStore.isAuthenticated;
</script>
```

## 🎯 Components

### Login Form

```svelte
<!-- routes/auth/login/+page.svelte -->
<script>
    import { getToastStore } from '@skeletonlabs/skeleton';
    import IconUser from '~icons/mdi/account';
    import IconLock from '~icons/mdi/lock';

    let loading = false;
    let errorMessage = '';
    const toastStore = getToastStore();

    async function handleSubmit(event) {
        // Form submission logic
    }
</script>

<form on:submit={handleSubmit} class="space-y-6">
    <!-- Username input -->
    <div class="relative">
        <IconUser class="absolute left-3 top-3 text-blue-300" />
        <input 
            type="text"
            name="username"
            class="pl-10 w-full rounded-lg"
            required
        />
    </div>

    <!-- Password input -->
    <div class="relative">
        <IconLock class="absolute left-3 top-3 text-blue-300" />
        <input 
            type="password"
            name="password"
            class="pl-10 w-full rounded-lg"
            required
        />
    </div>

    <button 
        type="submit"
        class="w-full btn variant-filled"
        disabled={loading}
    >
        {loading ? 'Signing in...' : 'Sign in'}
    </button>
</form>
```

### Layout Structure

```svelte
<!-- +layout.svelte -->
<script>
    import { AppShell, Toast } from '@skeletonlabs/skeleton';
    import '../app.postcss';
</script>

<Toast />
<AppShell>
    <slot />
</AppShell>
```

## 🎨 Styling with TailwindCSS

### Custom Classes

```css
/* app.postcss */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
    .btn-primary {
        @apply bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2;
    }
}
```

### Using Tailwind

```svelte
<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900">
    <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
        <!-- Content -->
    </div>
</div>
```

## 🚀 API Integration

### Environment Configuration

```env
# .env
PUBLIC_API_URL=http://localhost:8000
PUBLIC_CLOUDINARY_CLOUD_NAME=your-cloud-name
PUBLIC_CLOUDINARY_UPLOAD_PRESET=your-preset
```

### API Client Example

```javascript
import { PUBLIC_API_URL } from '$env/static/public';

async function fetchProfessionals() {
    const response = await fetch(`${PUBLIC_API_URL}/professionals`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.json();
}
```

## 🔒 Protected Routes

### Route Protection

```javascript
// hooks.server.js
export const handle = async ({ event, resolve }) => {
    // Check authentication status
    const session = event.cookies.get('session');
    
    if (!session && event.url.pathname.startsWith('/protected')) {
        return new Response('Redirect', {
            status: 303,
            headers: { Location: '/auth/login' }
        });
    }
    
    return resolve(event);
};
```

### Protected Layout

```svelte
<!-- routes/(protected)/+layout.svelte -->
<script>
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { authStore } from '$lib/auth_store';

    // Redirect if not authenticated
    $: if (browser && !$authStore.isAuthenticated) {
        goto('/auth/login');
    }
</script>
```

## 🎭 UI Components

### Toast Notifications

```javascript
import { getToastStore } from '@skeletonlabs/skeleton';

const toastStore = getToastStore();

// Show success toast
toastStore.trigger({
    message: 'Logged in successfully',
    background: 'variant-filled-success'
});

// Show error toast
toastStore.trigger({
    message: 'An error occurred',
    background: 'variant-filled-error'
});
```

### Loading States

```svelte
{#if loading}
    <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
        <circle 
            class="opacity-25" 
            cx="12" cy="12" r="10" 
            stroke="currentColor" 
            stroke-width="4"
        />
        <path 
            class="opacity-75" 
            fill="currentColor" 
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
    </svg>
{/if}
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 📦 Dependencies

Key dependencies include:
- SvelteKit: Application framework
- TailwindCSS: Utility-first CSS
- Skeleton UI: UI component library
- PostCSS: CSS processing
- Vite: Build tool

## 📱 Responsive Design

The application uses Tailwind's responsive classes:
- Mobile first approach
- Breakpoints: sm, md, lg, xl, 2xl
- Fluid typography and spacing

## 🚀 Performance Optimization

1. Code splitting by route
2. Image optimization
3. Lazy loading components
4. Service worker for caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
