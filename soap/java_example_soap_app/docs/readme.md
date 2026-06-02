# Java Example SOAP Application

## Environment
- Java 21

## To Run Server
- Navigate to project root directory.
- Generate JAXB classes in server by running:
  </br>
  `./gradlew :soap-server:generateJaxb`
- Run application:
  </br>
  `/gradlew :soap-server:bootRun`

### Why `@Endpoint` instead of `@RestController`?
| Feature        | `@Endpoint` (Spring-WS)               | `@RestController` (Spring MVC) |
| -------------- | ------------------------------------- | ------------------------------ |
| Purpose        | SOAP Web Services                     | REST APIs (JSON/XML over HTTP) |
| Message Format | SOAP XML Envelope                     | JSON / Plain XML               |
| Contract       | WSDL + XSD (Contract-First)           | OpenAPI / No strict contract   |
| Routing        | Based on XML payload (`@PayloadRoot`) | Based on URL + HTTP Method     |
| Use Case       | Enterprise, Banking, Legacy Systems   | Modern web/mobile APIs         |

#### Key Reason:
`@RestController` is designed for **REST** and does not understand SOAP envelopes, WSDL generation, or XML payload routing. If `@RestController` is used for SOAP, manual handling is needed for the entire SOAP XML parsing, envelope wrapping, etc., which defeats the purpose of using Spring-WS.

`@Endpoint` + `@PayloadRoot` is the correct and standard way to handle SOAP in Spring.

## Run Client
### Using `curl`
To invoke APIs by `curl`, check `docs/curls` directory.
  </br>
  Can be piped for formatting, like:
  </br>
  `bash update_temperature.sh | xmlstarlet format`
  </br>
  Or,
  </br>
  `bash update_temperature.sh | xmllint --format - `

### Using `soap-client` module
To run `soap-client` mdoule:
  - `./gradlew :soap-client:clean`
  - `./gradlew soap-client:generateJaxb`
  - `/gradlew :soap-client:build`
  - `./gradlew soap-client:bootRun`
