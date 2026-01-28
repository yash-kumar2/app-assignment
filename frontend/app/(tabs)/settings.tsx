import { useEffect, useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';

import { apiRequest, clearTokens } from '@/lib/api';

type Me = {
  name: string;
  email: string;
};

export default function SettingsScreen() {
  const [me, setMe] = useState<Me | null>(null);
  const [loadingMe, setLoadingMe] = useState(true);
  const [loggingOut, setLoggingOut] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await apiRequest('/auth/me', { method: 'GET', auth: true });
        if (!res.ok) {
          throw new Error('Failed to load profile');
        }
        const data = await res.json();
        setMe({ name: data.name, email: data.email });
      } catch {
        // If this fails, we simply show a generic state.
      } finally {
        setLoadingMe(false);
      }
    };
    load();
  }, []);

  const onLogout = async () => {
    if (loggingOut) return;
    setLoggingOut(true);
    try {
      try {
        await apiRequest('/auth/logout', { method: 'POST', auth: true });
      } catch {
        // ignore network errors for logout, we'll still clear tokens
      }
      await clearTokens();
      router.replace('/login');
    } finally {
      setLoggingOut(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Settings</Text>
        <Text style={styles.headerSubtitle}>Manage your account</Text>
      </View>

      <View style={styles.content}>
        {loadingMe ? (
          <View style={styles.center}>
            <ActivityIndicator size="large" color="#007AFF" />
            <Text style={styles.loadingText}>Loading profile...</Text>
          </View>
        ) : me ? (
          <View style={styles.profileCard}>
            <View style={styles.profileSection}>
              <Text style={styles.label}>Name</Text>
              <Text style={styles.value}>{me.name}</Text>
            </View>
            <View style={styles.divider} />
            <View style={styles.profileSection}>
              <Text style={styles.label}>Email</Text>
              <Text style={styles.value}>{me.email}</Text>
            </View>
          </View>
        ) : (
          <View style={styles.errorCard}>
            <Text style={styles.errorText}>Unable to load profile.</Text>
          </View>
        )}

        <TouchableOpacity
          style={[styles.logoutButton, loggingOut && styles.buttonDisabled]}
          onPress={onLogout}
          disabled={loggingOut}>
          {loggingOut ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.logoutButtonText}>Logout</Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    paddingTop: 60,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
  },
  profileCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  profileSection: {
    paddingVertical: 12,
  },
  label: {
    fontSize: 12,
    color: '#999',
    marginBottom: 4,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  value: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  divider: {
    height: 1,
    backgroundColor: '#e0e0e0',
    marginVertical: 8,
  },
  errorCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
  },
  errorText: {
    fontSize: 16,
    color: '#d32f2f',
    textAlign: 'center',
  },
  logoutButton: {
    backgroundColor: '#d32f2f',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 'auto',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  logoutButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

