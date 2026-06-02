# `SOAPAction` header is optional, depends on your SOAP service configuration

curl -X POST http://localhost:8080/ws \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: https://example.com/weather/getWeatherRequest" \
  -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                     xmlns:tns="https://example.com/weather">
         <soap:Body>
             <tns:getWeatherRequest>
                 <tns:city>Dhaka</tns:city>
             </tns:getWeatherRequest>
         </soap:Body>
       </soap:Envelope>'