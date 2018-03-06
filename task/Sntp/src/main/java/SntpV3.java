import fr.devnied.bitlib.BitUtils;
import java.net.DatagramPacket;

import lombok.Getter;
import lombok.Setter;
import org.apache.commons.net.ntp.TimeStamp;

@Setter
@Getter
public class SntpV3 {

  private int li = NtpV3Packet.LI_NO_WARNING;
  private int version = NtpV3Packet.VERSION_3;
  private int mode = NtpV3Packet.MODE_SERVER;
  private int stratum = 2;
  private int poll = NtpV3Packet.NTP_MINPOLL;
  private int precision;
  private int rootDelay;
  private int rootDispersion;
  private int referenceId;
  private long originateTimestamp;
  private long receiveTimestamp;
  private long transmitTimestamp;

  DatagramPacket datagramPacket;


  public SntpV3() {
  }

  public SntpV3(DatagramPacket datagramPacket) {
    this.datagramPacket = datagramPacket;
  }

  public DatagramPacket makeDatagramPacket() {
    byte[] buf = new byte[48];
    BitUtils bit = new BitUtils(buf);
    bit.setNextInteger(li, 2);
    bit.setNextInteger(version, 3);
    bit.setNextInteger(mode, 3);
    bit.setNextInteger(stratum, 8);
    bit.setNextInteger(poll, 8);
    bit.setNextInteger(precision, 8);
    bit.setNextInteger(rootDelay, 32);
    bit.setNextInteger(rootDispersion, 32);
    bit.setNextInteger(referenceId, 32);
    bit.setCurrentBitIndex(24*8);
    bit.setNextLong(originateTimestamp, 64);
    bit.setCurrentBitIndex(32*8);
    bit.setNextLong(receiveTimestamp, 64);
    bit.setNextLong(transmitTimestamp, 64);
    return new DatagramPacket(bit.getData(), 48);
  }

  public long NtpTime(long offsetMillis) {
    return TimeStamp.getNtpTime(System.currentTimeMillis() + offsetMillis).ntpValue();
  }

  public long getOriginateTimeFromRequest(byte[] bytes) {
    BitUtils bit = new BitUtils(bytes);
    bit.setCurrentBitIndex(40*8);
    return bit.getNextLong(64);
  }

  public int getVersionIndexFromRequest(byte[] bytes) {
    BitUtils bit = new BitUtils(bytes);
    bit.setCurrentBitIndex(2);
    return bit.getNextInteger(3);
  }
}
