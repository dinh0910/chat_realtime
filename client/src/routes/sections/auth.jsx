import { lazy, Suspense } from 'react';
import { Outlet } from 'react-router-dom';

import { AuthCenteredLayout } from '../../layouts/auth-centered';

import { SplashScreen } from '../../components/loading-screen';

/** **************************************
 * Centered layout
 *************************************** */
const CenteredLayout = {
  SignInPage: lazy(() => import('../../pages/auth/sign-in')),
  // SignUpPage: lazy(() => import('src/pages/auth/centered/sign-up')),
  // VerifyPage: lazy(() => import('src/pages/auth/centered/verify')),
  // ResetPasswordPage: lazy(() => import('src/pages/auth/centered/reset-password')),
  // UpdatePasswordPage: lazy(() => import('src/pages/auth/centered/update-password')),
};

const authCentered = {
  path: 'centered',
  element: (
    <AuthCenteredLayout>
      <Outlet />
    </AuthCenteredLayout>
  ),
  children: [
    { path: 'sign-in', element: <CenteredLayout.SignInPage /> },
    // { path: 'sign-up', element: <CenteredLayout.SignUpPage /> },
    // { path: 'verify', element: <CenteredLayout.VerifyPage /> },
    // { path: 'reset-password', element: <CenteredLayout.ResetPasswordPage /> },
    // { path: 'update-password', element: <CenteredLayout.UpdatePasswordPage /> },
  ],
};

// ----------------------------------------------------------------------

export const authRoutes = [
  {
    path: 'auth-demo',
    element: (
      <Suspense fallback={<SplashScreen />}>
        <Outlet />
      </Suspense>
    ),
    children: [authSplit, authCentered],
  },
];