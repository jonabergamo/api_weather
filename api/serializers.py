from .repositories import WeatherRepository


class WeatherSerializer:
    def __init__(self, data, many=False):
        # data pode ser um único objeto ou uma lista de objetos
        self.data = data
        self.many = many

    def serialize(self):
        if self.many:
            return [self._serialize_single(weather_entity) for weather_entity in self.data]
        else:
            return self._serialize_single(self.data)

    @staticmethod
    def _serialize_single(weather_entity):
        # Isso é um exemplo. Adapte os campos conforme necessário.
        return {
            "temperature": weather_entity.get("temperature"),
            "date": weather_entity.get("date"),
            "atmosphericPressure": weather_entity.get("atmosphericPressure"),
            "humidity": weather_entity.get("humidity"),
            "city": weather_entity.get("city"),
            "weather": weather_entity.get("weather")
        }