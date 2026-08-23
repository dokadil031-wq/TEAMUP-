with open("app/src/main/java/com/example/AppScreens.kt", "r") as f:
    content = f.read()

target_imports = """import androidx.lifecycle.compose.collectAsStateWithLifecycle"""
replacement_imports = """import androidx.lifecycle.compose.collectAsStateWithLifecycle
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.util.Base64
import java.io.ByteArrayOutputStream
import java.io.InputStream
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.foundation.Image
import androidx.compose.ui.layout.ContentScale"""

content = content.replace(target_imports, replacement_imports)
with open("app/src/main/java/com/example/AppScreens.kt", "w") as f:
    f.write(content)
