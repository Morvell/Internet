
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;


public class PropertiesHandler {

  private static Properties properties = null;
  private static File file;
  private static String filePath = "./application.properties";
  private static PropertiesHandler ourInstance = null;

  public static PropertiesHandler getInstance(boolean debug) throws IOException {

    if (ourInstance == null) {
      if (debug) {
        filePath = "src/test.properties";
      }
    }
    ourInstance = new PropertiesHandler();
    return ourInstance;
  }


  public static PropertiesHandler getInstance() throws IOException {

    if (ourInstance == null) {
      ourInstance = new PropertiesHandler();
    }
    return ourInstance;
  }

  private PropertiesHandler() throws IOException {
    properties = new Properties();
    file = new File(filePath).getAbsoluteFile();
    properties.load(getClass().getResourceAsStream("application.properties"));
  }

  public String getProperty(String var) {
    return properties.getProperty(var);
  }

  public String getProperty(String var, String def) {
    return properties.getProperty(var,def);
  }

  public void setProperty(String key, String var) throws IOException {
    properties.setProperty(key, var);
    properties.store(new FileOutputStream(file), null);

  }
}

