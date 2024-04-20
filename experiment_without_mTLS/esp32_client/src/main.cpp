#include <Arduino.h>
#include <MQTTClient.h>
#include <WiFi.h>

const char ssid[] = "";
const char pass[] = "";

WiFiClient espClient;
MQTTClient client;

unsigned long lastMillis = 0;

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

  client.begin("labs.local", 1883, espClient);

  // Set the mqtt client message callback
  client.onMessage(messageReceived);

  // Connect to the mqtt broker
  while (!client.connect("myclient"))
  {
    Serial.print(",");
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
      Serial.print(".");
      delay(1000);
    }
    Serial.println("Reconnected to MQTT Broker!");
  }
}
