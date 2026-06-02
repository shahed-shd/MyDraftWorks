package com.example.soapweather.endpoint;

import com.example.soapweather.model.*;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

@Endpoint
public class WeatherEndpoint {

    private static final String NAMESPACE_URI = "https://example.com/weather";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "getWeatherRequest")
    @ResponsePayload
    public GetWeatherResponse getWeather(@RequestPayload GetWeatherRequest request) {
        GetWeatherResponse response = new GetWeatherResponse();
        
        WeatherInfo info = new WeatherInfo();
        String city = request.getCity().toLowerCase();

        if ("london".equals(city)) {
            info.setCity("London");
            info.setTemperature(18);
            info.setCondition("Cloudy");
            info.setHumidity(75);
        } else if ("dhaka".equals(city)) {
            info.setCity("Dhaka");
            info.setTemperature(32);
            info.setCondition("Sunny");
            info.setHumidity(60);
        } else {
            info.setCity(request.getCity());
            info.setTemperature(25);
            info.setCondition("Unknown");
            info.setHumidity(50);
        }

        response.setWeatherInfo(info);
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "updateTemperatureRequest")
    @ResponsePayload
    public UpdateTemperatureResponse updateTemperature(@RequestPayload UpdateTemperatureRequest request) {
        UpdateTemperatureResponse response = new UpdateTemperatureResponse();
        response.setMessage("Temperature for " + request.getCity() 
                + " updated to " + request.getNewTemp() + "°C");
        return response;
    }
}