// import 'global.css';

// ----------------------------------------------------------------------

import { Router } from './routes/sections';

// import { useScrollToTop } from 'src/hooks/use-scroll-to-top';

import { CONFIG } from './config-global';
import { LocalizationProvider } from './locales';
import { I18nProvider } from './locales/i18n-provider';
import { ThemeProvider } from './theme/theme-provider';

// import { Snackbar } from './components/snackbar';
// import { ProgressBar } from './components/progress-bar';
// import { MotionLazy } from './components/animate/motion-lazy';
// import { SettingsDrawer, defaultSettings, SettingsProvider } from './components/settings';

// import { CheckoutProvider } from 'src/sections/checkout/context';

// import { AuthProvider as JwtAuthProvider } from 'src/auth/context/jwt';
// import { AuthProvider as Auth0AuthProvider } from 'src/auth/context/auth0';
// import { AuthProvider as AmplifyAuthProvider } from 'src/auth/context/amplify';
// import { AuthProvider as SupabaseAuthProvider } from 'src/auth/context/supabase';
// import { AuthProvider as FirebaseAuthProvider } from 'src/auth/context/firebase';

// ----------------------------------------------------------------------

const AuthProvider =
  (CONFIG.auth.method === 'amplify' && AmplifyAuthProvider) ||
  (CONFIG.auth.method === 'firebase' && FirebaseAuthProvider) ||
  (CONFIG.auth.method === 'supabase' && SupabaseAuthProvider) ||
  (CONFIG.auth.method === 'auth0' && Auth0AuthProvider) ||
  JwtAuthProvider;

export default function App() {
  useScrollToTop();

  return (
    <I18nProvider>
      <LocalizationProvider>
        {/* <AuthProvider> */}
        <SettingsProvider settings={defaultSettings}>
          <ThemeProvider>
            {/* <MotionLazy> */}
            {/* <CheckoutProvider> */}
            {/* <Snackbar />
                  <ProgressBar />
                  <SettingsDrawer /> */}
            <Router />
            {/* </CheckoutProvider> */}
            {/* </MotionLazy> */}
          </ThemeProvider>
        </SettingsProvider>
        {/* </AuthProvider> */}
      </LocalizationProvider>
    </I18nProvider>
  );
}
