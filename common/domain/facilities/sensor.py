# SensorResource is a Resource that gathers data.
# Examples: temperature sensor, motion detector.

from .resource import Resource


class SensorResource(Resource):
    def __init__(self, name: str, sensor_type: str, **kwargs):
        super().__init__(name, **kwargs)
        self.sensor_type = sensor_type
        self.last_reading = None

    def update_reading(self, value):
        self.last_reading = value
        self.update_version()

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "sensor_type": self.sensor_type,
            "last_reading": self.last_reading
        })
        return base
