package example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.time.Instant;
import java.util.Map;

public class HelloHandler implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    @Override
    public Map<String, Object> handleRequest(
            Map<String, Object> event,
            Context context) {

        context.getLogger().log(
                "HelloHandler received event: " + event
        );

        return Map.of(
                "success", true,
                "message", "Hello from Java Lambda",
                "receivedEvent", event,
                "timestamp", Instant.now().toString()
        );
    }
}