from spyne import Application, rpc, ServiceBase, Unicode, Integer, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import logging

# Optional: Define a Complex Type (like a data class)
class WeatherInfo(ComplexModel):
    __namespace__ = 'http://example.com/weather'
    city = Unicode
    temperature = Integer
    condition = Unicode
    humidity = Integer

class WeatherService(ServiceBase):
    __service_url_path__ = '/weather'
    __namespace__ = 'http://example.com/weather'

    @rpc(Unicode, _returns=WeatherInfo)
    def get_weather(ctx, city):
        """Get weather information for a city"""
        # In real app, fetch from DB/API
        if city.lower() == "london":
            return WeatherInfo(city="London", temperature=18, condition="Cloudy", humidity=75)
        elif city.lower() == "dhaka":
            return WeatherInfo(city="Dhaka", temperature=32, condition="Sunny", humidity=60)
        else:
            return WeatherInfo(city=city, temperature=25, condition="Unknown", humidity=50)

    @rpc(Unicode, Integer, _returns=Unicode)
    def update_temperature(ctx, city, new_temp):
        """Simulate updating temperature"""
        raise NotImplementedError("This method is not implemented yet")
        return f"Temperature for {city} updated to {new_temp}°C"

# Create the application
application = Application(
    [WeatherService],
    tns='http://example.com/weather',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# WSGI wrapper
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    server = make_server('0.0.0.0', 8000, wsgi_application)
    
    print("SOAP Service running at http://127.0.0.1:8000")
    print("WSDL available at: http://127.0.0.1:8000/?wsdl")
    print("Try it with tools like SoapUI, Postman, or Zeep client")
    
    server.serve_forever()