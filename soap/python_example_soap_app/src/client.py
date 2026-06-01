from zeep import Client
# import zeep

wsdl_url = "http://127.0.0.1:8000/?wsdl"

client = Client(wsdl_url)

# Call get_weather
result = client.service.get_weather("London")
print("Weather in London:", result)

# Call update_temperature
msg = client.service.update_temperature("Dhaka", 35)
print(msg)
