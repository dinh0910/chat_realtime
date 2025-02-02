import { lazy, Suspense } from 'react';
import { Navigate, useRoutes } from 'react-router-dom';

import { AuthCenteredLayout } from '../../layouts/auth-centered';

import { SplashScreen } from '../../components/loading-screen';

import { authRoutes } from './auth';
// import { mainRoutes } from './main';
// import { authDemoRoutes } from './auth-demo';
// import { dashboardRoutes } from './dashboard';
// import { componentsRoutes } from './components';

// ----------------------------------------------------------------------

const HomePage = lazy(() => import('../../pages/auth/sign-in'));

export function Router() {
  return useRoutes([
    {
      path: '/',
      /**
       * Skip home page
       * element: <Navigate to={CONFIG.auth.redirectPath} replace />,
       */
      element: (
        <Suspense fallback={<SplashScreen />}>
          <AuthCenteredLayout>
            <HomePage />
          </AuthCenteredLayout>
        </Suspense>
      ),
    },

    // Auth
    ...authRoutes,
    // ...authDemoRoutes,

    // Dashboard
    // ...dashboardRoutes,

    // Main
    // ...mainRoutes,

    // Components
    // ...componentsRoutes,

    // No match
    { path: '*', element: <Navigate to="/404" replace /> },
  ]);
}
