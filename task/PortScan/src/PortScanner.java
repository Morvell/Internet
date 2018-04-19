import java.io.FileWriter;
import java.io.IOException;
import java.net.DatagramSocket;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

class PortScanner {

  public static void main(final String... args)
      throws InterruptedException, ExecutionException, IOException {
    final ExecutorService es = Executors.newFixedThreadPool(50);
    final String ip = "87.240.188.250";
    final int timeout = 1;
    final List<Future<ScanResult>> futures = new ArrayList<>();
    for (int port = 1; port <= 65535; port++) {
      futures.add(tcpPortIsOpen(es, ip, port, timeout));
      futures.add(udpPortIsOpen(es, ip, port, timeout));
    }
    es.awaitTermination(10, TimeUnit.MILLISECONDS);
    int openPorts = 0;
    FileWriter writer = new FileWriter("./result.txt");
    for (final Future<ScanResult> f : futures) {

      if (f.get().isOpen()) {
        openPorts++;
        writer.write(String.valueOf(f.get()));
      }

    }
    writer.flush();
    writer.close();
    System.out.println(
        "There are " + openPorts + " open ports on host " + ip + " (probed with a timeout of "
            + timeout + "ms)");
  }

  public static Future<ScanResult> tcpPortIsOpen(final ExecutorService es, final String ip,
      final int port,
      final int timeout) {
    return es.submit(() -> {
      try {
        Socket socket = new Socket();
        socket.connect(new InetSocketAddress(ip, port), timeout);
        socket.close();
        return new ScanResult(port, true, "TCP");
      } catch (Exception ex) {
        return new ScanResult(port, false, "TCP");
      }
    });
  }

  public static Future<ScanResult> udpPortIsOpen(final ExecutorService es, final String ip,
      final int port,
      final int timeout) {
    return es.submit(() -> {
      try {
        DatagramSocket socket = new DatagramSocket(port);
        socket.setSoTimeout(timeout);
        socket.connect(new InetSocketAddress(ip, port));
        if(!socket.isConnected()) {
          socket.close();
          return new ScanResult(port, false, "UDP");
        }
        return new ScanResult(port, true,"UDP");
      } catch (Exception ex) {
        return new ScanResult(port, false, "UDP");
      }
    });
  }

  public static class ScanResult {

    private int port;

    private boolean isOpen;

    private String type;

    public ScanResult(int port, boolean isOpen, String type) {
      super();
      this.port = port;
      this.isOpen = isOpen;
      this.type = type;
    }

    public int getPort() {
      return port;
    }

    public void setPort(int port) {
      this.port = port;
    }

    public boolean isOpen() {
      return isOpen;
    }

    public void setOpen(boolean isOpen) {
      this.isOpen = isOpen;
    }

    @Override
    public String toString() {
      return
          "port=" + port +
          ", isOpen=" + isOpen +
          ", type='" + type + '\'' +
          '}' + "\n";
    }
  }
}