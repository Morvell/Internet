
public interface NtpV3Packet {

  int NTP_PORT = 123;
  int LI_NO_WARNING = 0;
  int LI_LAST_MINUTE_HAS_61_SECONDS = 1;
  int LI_LAST_MINUTE_HAS_59_SECONDS = 2;
  int LI_ALARM_CONDITION = 3;
  int MODE_RESERVED = 0;
  int MODE_SYMMETRIC_ACTIVE = 1;
  int MODE_SYMMETRIC_PASSIVE = 2;
  int MODE_CLIENT = 3;
  int MODE_SERVER = 4;
  int MODE_BROADCAST = 5;
  int MODE_CONTROL_MESSAGE = 6;
  int MODE_PRIVATE = 7;
  int NTP_MINPOLL = 4;
  int NTP_MAXPOLL = 14;
  int NTP_MINCLOCK = 1;
  int NTP_MAXCLOCK = 10;
  int VERSION_3 = 3;
  int VERSION_4 = 4;

}
