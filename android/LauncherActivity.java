package org.blender.android.experimental;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import java.io.File;

/** Keep a way to retrieve logs even when the separate native process exits. */
public class LauncherActivity extends Activity {
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        int padding = (int) (24 * getResources().getDisplayMetrics().density);
        layout.setPadding(padding, padding, padding, padding);
        TextView heading = new TextView(this);
        heading.setText("Blender — тестовая сборка");
        heading.setTextSize(24);
        layout.addView(heading);
        TextView help = new TextView(this);
        help.setText("Если Blender закроется или не покажет интерфейс, вернитесь сюда и отправьте журнал ошибки.");
        layout.addView(help);
        Button launch = new Button(this);
        launch.setText("Открыть Blender");
        launch.setOnClickListener(v -> startActivity(new Intent(this, BlenderActivity.class)));
        layout.addView(launch);
        Button share = new Button(this);
        share.setText("Поделиться журналом");
        share.setOnClickListener(v -> {
            if (!new File(getFilesDir(), "blender.log").isFile()) {
                Toast.makeText(this, "Журнала пока нет. Сначала запустите Blender.", Toast.LENGTH_LONG).show();
                return;
            }
            Uri uri = Uri.parse("content://org.blender.android.experimental.logs/blender.log");
            Intent intent = new Intent(Intent.ACTION_SEND).setType("text/plain")
                .putExtra(Intent.EXTRA_STREAM, uri)
                .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            intent.setClipData(android.content.ClipData.newRawUri("Blender log", uri));
            startActivity(Intent.createChooser(intent, "Отправить журнал Blender"));
        });
        layout.addView(share);
        setContentView(layout);
    }
}
