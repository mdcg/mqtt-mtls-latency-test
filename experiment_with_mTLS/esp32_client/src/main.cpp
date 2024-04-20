#include <Arduino.h>
#include <MQTTClient.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>

const char ssid[] = "<rede-wifi>";
const char pass[] = "<senha>";

const char *serverCA = R"EOF(-----BEGIN CERTIFICATE-----
<CA - Certificate>
-----END CERTIFICATE-----)EOF";

const char *clientCert = R"KEY(-----BEGIN CERTIFICATE-----
<ESP32 - Certificate>
-----END CERTIFICATE-----)KEY";

const char *clientKey = R"KEY(-----BEGIN PRIVATE KEY-----
<ESP32 - KEY>
-----END PRIVATE KEY-----)KEY";

WiFiClientSecure net;
MQTTClient client;

void messageReceived(String &topic, String &payload)
{
  Serial.println("Incoming: " + topic + " - " + payload);
  client.publish("mTLS/end", payload);
}

void setup()
{
  Serial.begin(115200);

  // Connect to the WiFi
  WiFi.begin(ssid, pass);
  Serial.print("Checking wifi...");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("WiFi connected!");
  // Configure WiFiClientSecure with the required certs
  net.setCACert(serverCA);
  net.setCertificate(clientCert);
  net.setPrivateKey(clientKey);

  // Set a timeout for our WiFiClient so it doesn't hang on disconnect
  net.setTimeout(5);

  client.begin("labs.local", 8883, net);

  // Set the mqtt client message callback
  client.onMessage(messageReceived);

  // Connect to the mqtt broker
  while (!client.connect("myclient"))
  {
    Serial.print("m");
    delay(1000);
  }
  Serial.println("Connected!");
  client.subscribe("mTLS/start");
}

void loop()
{
  // Run the mqtt client loop (handles recived messages - runs keep alive)
  client.loop();

  // Check that client is still connected - if not reconnect
  if (!client.connected())
  {
    while (!client.connect("myclient"))
    {
      Serial.print("r");
      delay(1000);
    }
    Serial.println("Reconnected to MQTT Broker!");
  }
}
