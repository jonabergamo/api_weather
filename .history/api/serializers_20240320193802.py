

class WeatherSerializer:
    fields = "__all__"

    def __init__(self, data=None, many=False):
        self.data = data
        self.many = many

    def serialize(self):
        if self.many:
            return [self._serialize_single(weather_entity) for weather_entity in self.data]
        else:
            return self._serialize_single(self.data)

    def _serialize_single(self, weather_entity):
        serialized_data = {}
        if self.fields == "__all__":
            self.fields = weather_entity.keys()  # Usar todos os campos se "__all__" for especificado

        for field in self.fields:
            if field in weather_entity:
                serialized_data[field] = weather_entity[field]

        return serialized_data