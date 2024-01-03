import java.nio.file.Path;

import com.sun.jna.Library;
import com.sun.jna.Native;

public interface LibSharedUtils extends Library {
    // LibSharedUtils INSTANCE = (LibSharedUtils) Native.loadLibrary("sharedUtils", LibSharedUtils.class); // Didn't work, don't know why
    LibSharedUtils INSTANCE = (LibSharedUtils) Native.load(Path.of("libsharedutils.so").toAbsolutePath().toString(), LibSharedUtils.class);

    int add(int a, int b);

    int multiply(int a, int b);
}
