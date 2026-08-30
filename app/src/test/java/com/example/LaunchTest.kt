package com.example

import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.Robolectric
import org.robolectric.annotation.Config
import android.os.Build

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [Build.VERSION_CODES.O_MR1])
class LaunchTest {
    @Test
    fun testActivityLaunch() {
        Robolectric.buildActivity(MainActivity::class.java).create().start().resume().visible()
    }
}
