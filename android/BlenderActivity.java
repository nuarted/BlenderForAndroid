package org.blender.android.experimental;

import android.app.AlertDialog;
import android.os.Bundle;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import org.libsdl.app.SDLActivity;

public class BlenderActivity extends SDLActivity {
    @Override protected String[] getLibraries() { return new String[] {"main"}; }

    @Override protected String[] getArguments() {
        return new String[] {"--factory-startup", "--gpu-backend", "vulkan"};
    }

    @Override public void onCreate(Bundle state) {
        // SDL starts its native thread after onCreate, when the surface is ready.
        try {
            copyAssets("blender", new File(getFilesDir(), "blender"));
        } catch (IOException error) {
            android.util.Log.e("Blender", "Unable to extract resources", error);
            super.onCreate(state);
            new AlertDialog.Builder(this).setTitle("Blender resources")
                .setMessage(error.getMessage()).setPositiveButton("Close", (d, w) -> finish()).show();
            return;
        }
        super.onCreate(state);
    }

    private void copyAssets(String source, File target) throws IOException {
        String[] children = getAssets().list(source);
        if (children != null && children.length > 0) {
            if (!target.isDirectory() && !target.mkdirs()) {
                throw new IOException("Cannot create " + target);
            }
            for (String child : children) copyAssets(source + "/" + child, new File(target, child));
            return;
        }
        try (InputStream input = getAssets().open(source);
             FileOutputStream output = new FileOutputStream(target)) {
            byte[] buffer = new byte[65536];
            int count;
            while ((count = input.read(buffer)) != -1) output.write(buffer, 0, count);
        }
    }
}
