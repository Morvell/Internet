import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class Main {
  public static void main(String[] args) {


    int port = 123;
    long offsetMillis = 0;

    try {
      PropertiesHandler pr = PropertiesHandler.getInstance();

      port = Integer.valueOf(pr.getProperty("port","123"));
      offsetMillis = Long.valueOf(pr.getProperty("offset","0"));

    } catch (IOException e) {
      e.printStackTrace();
    }

    SimpleNTPServer timeServer = new SimpleNTPServer(port, offsetMillis);

    try {
      timeServer.start();
    } catch (IOException e) {
      e.printStackTrace();
    }

  }
  }


