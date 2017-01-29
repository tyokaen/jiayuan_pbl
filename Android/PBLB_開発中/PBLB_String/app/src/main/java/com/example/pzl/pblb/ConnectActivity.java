package com.example.pzl.pblb;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.TextView;

import jp.ksksue.driver.serial.FTDriver;

public class ConnectActivity extends Activity {

    Button mRC,btnBegin,btnEnd,btn_app;
    FTDriver mSerial;
    private TextView mText;

    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_connect);


        btnBegin = (Button) findViewById(R.id.btnBegin);
        btnEnd = (Button) findViewById(R.id.btnEnd);
        mRC = (Button) findViewById(R.id.RC);

        mText = (TextView) findViewById(R.id.textView1);

        mRC.setEnabled(false);
        btnEnd.setEnabled(false);
        mSerial = new FTDriver((UsbManager)getSystemService(Context.USB_SERVICE));

        PendingIntent permissionIntent = PendingIntent.getBroadcast(this, 0, new Intent(
                ACTION_USB_PERMISSION), 0);
        mSerial.setPermissionIntent(permissionIntent);

        mRC.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent=new Intent(ConnectActivity.this,MainActivity.class);
                startActivity(intent);
            }});
    }

    public void onBeginClick(View view) {
        // [FTDriver] Open USB Serial
        if(mSerial.begin(FTDriver.BAUD115200)) {


            mRC.setEnabled(true);
            btnEnd.setEnabled(true);
            btnBegin.setEnabled(false);


            mText.setText("接続中");
            mText.setTextColor(Color.BLUE);
        } else {
            mText.setText("未接続");
            mText.setTextColor(Color.RED);
        }
    }

    public void onEndClick(View view) {

        mRC.setEnabled(false);

        btnEnd.setEnabled(false);
        btnBegin.setEnabled(true);
        mSerial.end();
        mText.setText("未接続");
        mText.setTextColor(Color.RED);

    }

}
