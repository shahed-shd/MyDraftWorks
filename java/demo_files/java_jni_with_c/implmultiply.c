#include <jni.h>

JNIEXPORT jint JNICALL Java_Main_multiply(JNIEnv *env, jobject obj, jint a, jint b) {
   return a * b;
}
