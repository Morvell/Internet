import java.io.IOException;

public class Main {

  public static void main(String[] args) {

    int port = 123;
    long millisOffset = 0;
    long minutesOffset = 0;
    long hoursOffset = 0;
    long dayOffset = 0;

    try {
      PropertiesHandler pr = PropertiesHandler.getInstance();

      port = Integer.valueOf(pr.getProperty("port", "123"));
      millisOffset = Long.valueOf(pr.getProperty("millisOffset", "0"));
      minutesOffset = Long.valueOf(pr.getProperty("minutesOffset", "0")) * 60 * 1000;
      hoursOffset = Long.valueOf(pr.getProperty("hoursOffset", "0")) * 60 * 60 * 1000;
      dayOffset = Long.valueOf(pr.getProperty("dayOffset", "0")) * 24 * 60 * 60 * 1000;

    } catch (IOException e) {
      e.printStackTrace();
    }

    SimpleNTPServer timeServer = new SimpleNTPServer(port, dayOffset + hoursOffset +
        minutesOffset + millisOffset);

    try {
      timeServer.start();
    } catch (IOException e) {
      e.printStackTrace();
    }

  }
}


