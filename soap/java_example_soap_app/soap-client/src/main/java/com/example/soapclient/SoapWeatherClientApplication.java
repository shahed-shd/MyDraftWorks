package com.example.soapclient;

import com.example.soapweather.model.GetWeatherRequest;
import com.example.soapweather.model.GetWeatherResponse;
import com.example.soapweather.model.UpdateTemperatureRequest;
import com.example.soapweather.model.UpdateTemperatureResponse;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.ws.client.core.WebServiceTemplate;

@SpringBootApplication
public class SoapWeatherClientApplication {

    public static void main(String[] args) {
        SpringApplication.run(SoapWeatherClientApplication.class, args);
    }

    @Bean
    CommandLineRunner run(WebServiceTemplate webServiceTemplate) {
        return args -> {
            System.out.println("=== SOAP Client Started ===\n");

            // Test 1: getWeather
            GetWeatherRequest getRequest = new GetWeatherRequest();
            getRequest.setCity("Dhaka");

            System.out.println("Calling getWeather(Dhaka)...");
            GetWeatherResponse weatherResponse = (GetWeatherResponse) webServiceTemplate
                    .marshalSendAndReceive("http://localhost:8080/ws", getRequest);

            System.out.println("City: " + weatherResponse.getWeatherInfo().getCity());
            System.out.println("Temperature: " + weatherResponse.getWeatherInfo().getTemperature() + "°C");
            System.out.println("Condition: " + weatherResponse.getWeatherInfo().getCondition());
            System.out.println("Humidity: " + weatherResponse.getWeatherInfo().getHumidity() + "%\n");

            // Test 2: updateTemperature
            UpdateTemperatureRequest updateRequest = new UpdateTemperatureRequest();
            updateRequest.setCity("London");
            updateRequest.setNewTemp(22);

            System.out.println("Calling updateTemperature(London, 22)...");
            UpdateTemperatureResponse updateResponse = (UpdateTemperatureResponse) webServiceTemplate
                    .marshalSendAndReceive("http://localhost:8080/ws", updateRequest);

            System.out.println("Response: " + updateResponse.getMessage());
        };
    }
}