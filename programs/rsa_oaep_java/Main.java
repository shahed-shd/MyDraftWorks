import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.MGF1ParameterSpec;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.spec.OAEPParameterSpec;
import javax.crypto.spec.PSource;

/*
 * Language: Java 21
 */

public class Main {
    private static final String UTF8 = "UTF-8";
    private static final String RSA = "RSA";
    private static final String SHA_256 = "SHA-256";
    private static final String MGF1 = "MGF1";
    private static final String RSA_ECB_OAEP_WITH_SHA_256_AND_MGF1_PADDING = "RSA/ECB/OAEPWithSHA-256AndMGF1Padding";

    public static void main(String[] args) throws Exception {
        // Generate RSA key pair
        // KeyPair keyPair = generateKeyPair();
        // PublicKey publicKey = keyPair.getPublic();
        // PrivateKey privateKey = keyPair.getPrivate();

        // Load RSA key pair
        PrivateKey privateKey = loadPrivateKey("private.pem");
        PublicKey publicKey = loadPublicKey("public.pem");

        // Prepare message
        String plainText = "Hello, World! This is a secret message.";
        byte[] plainTextInBytes = plainText.getBytes(UTF8);

        // Encrypt
        byte[] cipherTextInBytes = encrypt(plainTextInBytes, publicKey);
        System.out.println("Cipher text base-64 encoded:\n" + Base64.getEncoder().encodeToString(cipherTextInBytes));

        // Decrypt
        byte[] decryptedTextInBytes = decrypt(cipherTextInBytes, privateKey);
        String decryptedText = new String(decryptedTextInBytes, UTF8);
        System.out.println("\nDecrypted text:\n" + decryptedText);
    }

    private static KeyPair generateKeyPair() throws Exception {
        KeyPairGenerator generator = KeyPairGenerator.getInstance(RSA);
        generator.initialize(2048); // 2048-bit key
        return generator.generateKeyPair();
    }

    private static byte[] encrypt(byte[] plaintext, PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance(RSA_ECB_OAEP_WITH_SHA_256_AND_MGF1_PADDING);
        OAEPParameterSpec oaepParameterSpec = getOaepParameterSpec();
        cipher.init(Cipher.ENCRYPT_MODE, publicKey, oaepParameterSpec);
        return cipher.doFinal(plaintext);
    }

    private static byte[] decrypt(byte[] ciphertext, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance(RSA_ECB_OAEP_WITH_SHA_256_AND_MGF1_PADDING);
        OAEPParameterSpec oaepParameterSpec = getOaepParameterSpec();
        cipher.init(Cipher.DECRYPT_MODE, privateKey, oaepParameterSpec);
        return cipher.doFinal(ciphertext);
    }

    private static OAEPParameterSpec getOaepParameterSpec() {
        return new OAEPParameterSpec(
                SHA_256,
                MGF1,
                MGF1ParameterSpec.SHA256,
                PSource.PSpecified.DEFAULT);
    }

    public static PrivateKey loadPrivateKey(String filePath) throws Exception {
        String key = new String(Files.readAllBytes(Paths.get(filePath)));

        key = key.replace("-----BEGIN PRIVATE KEY-----", "")
                .replace("-----END PRIVATE KEY-----", "")
                .replaceAll("\\s+", ""); // Remove any whitespace or newlines

        byte[] keyBytes = Base64.getDecoder().decode(key);

        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance(RSA);

        return keyFactory.generatePrivate(keySpec);
    }

    public static PublicKey loadPublicKey(String filePath) throws Exception {
        String key = new String(Files.readAllBytes(Paths.get(filePath)));

        key = key.replace("-----BEGIN PUBLIC KEY-----", "")
                .replace("-----END PUBLIC KEY-----", "")
                .replaceAll("\\s+", ""); // Remove any whitespace or newlines

        byte[] keyBytes = Base64.getDecoder().decode(key);

        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance(RSA);

        return keyFactory.generatePublic(keySpec);
    }

}
