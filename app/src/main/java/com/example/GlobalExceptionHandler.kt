package com.example

import android.content.Context
import android.content.Intent
import java.io.PrintWriter
import java.io.StringWriter
import kotlin.system.exitProcess

class GlobalExceptionHandler(
    private val context: Context,
    private val defaultHandler: Thread.UncaughtExceptionHandler?
) : Thread.UncaughtExceptionHandler {
    override fun uncaughtException(thread: Thread, exception: Throwable) {
        val stringWriter = StringWriter()
        exception.printStackTrace(PrintWriter(stringWriter))
        val stackTrace = stringWriter.toString()

        val intent = Intent(context, ErrorActivity::class.java).apply {
            putExtra("EXTRA_ERROR_DETAILS", stackTrace)
            putExtra("EXTRA_ERROR_MESSAGE", exception.message)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        }

        context.startActivity(intent)
        
        android.os.Process.killProcess(android.os.Process.myPid())
        exitProcess(1)
    }
}
