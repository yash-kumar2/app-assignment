import { useEffect, useRef, useState } from 'react';
import { ActivityIndicator, Button, StyleSheet, Text, View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { Video, ResizeMode, VideoRef } from 'expo-av';

import { apiRequest, API_URL } from '@/lib/api';

type StreamResponse = {
  stream_url: string;
};

export default function VideoScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [streamUrl, setStreamUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isMuted, setIsMuted] = useState(false);
  const videoRef = useRef<VideoRef>(null);

  useEffect(() => {
    const load = async () => {
      if (!id) return;
      try {
        const playRes = await apiRequest(`/video/${id}/play`, {
          method: 'POST',
          auth: true,
        });
        if (!playRes.ok) {
          throw new Error('Unable to start playback');
        }
        const playData = await playRes.json();
        const token = playData.playback_token as string;

        const proxyUrl = `${API_URL}/video/${id}/stream?token=${encodeURIComponent(token)}`;

        setStreamUrl(proxyUrl);
      } catch (e: any) {
        setError(e.message ?? 'Failed to load video');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  const togglePlayPause = async () => {
    const video = videoRef.current;
    if (!video) return;
    const status = await video.getStatusAsync();
    if (!status.isLoaded) return;
    if (status.isPlaying) {
      await video.pauseAsync();
    } else {
      await video.playAsync();
    }
  };

  const toggleMute = async () => {
    const video = videoRef.current;
    if (!video) return;
    const next = !isMuted;
    setIsMuted(next);
    await video.setIsMutedAsync(next);
  };

  const seekForward = async () => {
    const video = videoRef.current;
    if (!video) return;
    const status = await video.getStatusAsync();
    if (!status.isLoaded || !status.positionMillis) return;
    await video.setPositionAsync(status.positionMillis + 10000);
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#fff" />
        <Text style={styles.loadingText}>Loading video...</Text>
      </View>
    );
  }

  if (error || !streamUrl) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>⚠️ {error ?? 'Unable to play video'}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Video
        ref={videoRef}
        source={{ uri: streamUrl }}
        style={styles.video}
        useNativeControls={false}
        resizeMode={ResizeMode.CONTAIN}
        shouldPlay
      />
      <View style={styles.controls}>
        <Button title="Play / Pause" onPress={togglePlayPause} />
        <Button title={isMuted ? 'Unmute' : 'Mute'} onPress={toggleMute} />
        <Button title="Seek +10s" onPress={seekForward} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#000',
  },
  loadingText: {
    marginTop: 12,
    color: '#fff',
    fontSize: 16,
  },
  errorText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    paddingHorizontal: 20,
  },
  video: {
    flex: 1,
  },
  controls: {
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#1a1a1a',
    borderTopWidth: 1,
    borderTopColor: '#333',
  },
});

