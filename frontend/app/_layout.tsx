import { DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';

export default function RootLayout() {
  // Force light theme - no dark mode
  return (
    <ThemeProvider value={DefaultTheme}>
      <Stack screenOptions={{ headerShown: false }}>
        {/* Bootstrap decides whether to go to login or tabs based on stored token */}
        <Stack.Screen name="index" />
        {/* Auth flow */}
        <Stack.Screen name="login" />
        <Stack.Screen name="signup" />

        {/* Main app (dashboard, settings, player) */}
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="video/[id]" />
      </Stack>
      <StatusBar style="dark" />
    </ThemeProvider>
  );
}
