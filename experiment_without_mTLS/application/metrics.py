from influxdb_client import InfluxDBClient, Point


class InfluxDB:
    def __init__(self):
        client = InfluxDBClient(url="localhost:8086", token="SUPERTOKEN!", org="isd")
        self.write_api = client.write_api()

    def collect(self, elapsed_time):
        point = Point("experiment").tag("service", "without_mTLS").field("elapsed_time", elapsed_time)
        self.write_api.write(bucket="metrics", record=point)
