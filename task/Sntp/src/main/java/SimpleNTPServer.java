import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SimpleNTPServer implements Runnable {

  private int port;

  private volatile boolean running;

  private boolean started;

  private DatagramSocket socket;

  long offsetMillis;

  public SimpleNTPServer() {
    port = 123;
  }

  public SimpleNTPServer(int port, long offsetMillis) {
    this.port = port;
    this.offsetMillis = offsetMillis;
  }


  private void connect() throws IOException {
    if (socket == null) {
      socket = new DatagramSocket(port);

      System.out.println("Running NTP service on port " + port + "/UDP");
    }
  }

  public void start() throws IOException {
    if (socket == null) {
      connect();
    }
    if (!started) {
      started = true;
      new Thread(this).start();
    }
  }

  @Override
  public void run() {
    running = true;
    byte buffer[] = new byte[48];
    final DatagramPacket request = new DatagramPacket(buffer, buffer.length);
    do {
      try {
        socket.receive(request);
        handlePacket(request, offsetMillis);
      } catch (IOException e) {
        if (running) {
          e.printStackTrace();
        }
      }
    } while (running);
  }

  private void handlePacket(DatagramPacket req, long offsetMillis) throws IOException {

    System.out.println("NTP packet from " + req.getAddress().getHostAddress());
    SntpV3 response = new SntpV3();

    response.setMode(NtpV3Packet.MODE_SERVER);
    response.setVersion(response.getVersionIndexFromRequest(req.getData()));

    response.setOriginateTimestamp(response.getOriginateTimeFromRequest(req.getData()));
    response.setReceiveTimestamp(response.NtpTime(offsetMillis));
    response.setTransmitTimestamp(response.NtpTime(offsetMillis));

    DatagramPacket dp = response.makeDatagramPacket();
    dp.setPort(req.getPort());
    dp.setAddress(req.getAddress());
    socket.send(dp);
  }
}


