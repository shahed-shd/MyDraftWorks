# `SOAPAction` header is optional, depends on your SOAP service configuration

curl -X POST http://localhost:8080/ws \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: https://example.com/weather/updateTemperatureRequest" \
  -d '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                     xmlns:tns="https://example.com/weather">
         <soap:Body>
             <tns:updateTemperatureRequest>
                 <tns:city>Dhaka</tns:city>
                 <tns:newTemp>35</tns:newTemp>
             </tns:updateTemperatureRequest>
         </soap:Body>
       </soap:Envelope>'