import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react';
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native';
import { LinkExit, LinkSuccess } from 'react-native-plaid-link-sdk';

import { FinClient } from './clients/FinClient';
import logger from './logger';


const serviceHost: string = 'fin-serving-layer';
const servicePort: string = process.env.FIN_SERVING_LAYER_PORT || "9999";
const finClient: FinClient = new FinClient(`http://${serviceHost}:${servicePort}`)


const App: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState("failed");

  useEffect(() => {
    let attempts = 0;
    const maxAttempts = 30;

    const checkHealth = async () => {
      try {
        // const response = await axios.get('http://fin-serving-layer:8000/health');
        const status = await finClient.getHealthStatus();
        if (status === 'healthy') {
          setHealthStatus("healthy");
          setLoading(false);
        } else {
          attempts++;
          if (attempts < maxAttempts) {
            setTimeout(checkHealth, 1000);
          } else {
            setLoading(false);
          }
        }
      } catch (error) {
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(checkHealth, 1000);
        } else {
          setLoading(false);
        }
      }
    };

    checkHealth();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.text}>
        {healthStatus === "healthy" ? 'Service is Healthy' : 'Service is Unhealthy'}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  text: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
});

export default App;
