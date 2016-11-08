package com.example.jiayuan.test_http1;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
Button b;
TextView t;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        b=(Button)findViewById(R.id.Button1);
        t=(TextView)findViewById(R.id.TextView1);
        b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                HttpClientTask task=new HttpClientTask(t);
                task.execute();
            }
        });
    }
}
