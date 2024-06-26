from influxdb_client import InfluxDBClient, Point


class InfluxDB:
    def __init__(self):
        client = InfluxDBClient(url="labs.local:8086", token="SUPERTOKEN!", org="isd", retries=True)
        self.write_api = client.write_api()

    def collect(self, elapsed_time):
        point = Point("experiment").tag("service", "with_mTLS").field("elapsed_time", elapsed_time)
        self.write_api.write(bucket="metrics", record=point)
