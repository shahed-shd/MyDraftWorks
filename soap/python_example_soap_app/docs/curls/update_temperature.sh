curl -X POST http://127.0.0.1:8000/ \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: http://example.com/weather/update_temperature" \
  -d @update_temperature.xml