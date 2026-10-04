package example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.time.Instant;
import java.util.Map;

public class WorkerHandler implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    @Override
    public Map<String, Object> handleRequest(
            Map<String, Object> event,
            Context context) {

        context.getLogger().log(
                "Worker started. event=" + event
        );

        try {
            // Simulate background work
            Thread.sleep(5_000);

            context.getLogger().log(
                    "Background work completed"
            );

            return Map.of(
                    "success", true,
                    "message", "Background task completed",
                    "completedAt", Instant.now().toString()
            );

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();

            context.getLogger().log(
                    "Worker interrupted: " + e.getMessage()
            );

            throw new RuntimeException(e);
        }
    }
}