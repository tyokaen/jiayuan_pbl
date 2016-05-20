package com.example.pzl.musenn;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import jp.ksksue.driver.serial.FTDriver;

public class TestActivity extends Activity {
    TextView mY, mY2, mY3;
    private EditText FileName;
    FTDriver mSerial;
    Handler mHandler = new Handler();
    private String mText1, mText2, mText3;
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";
    private boolean mRunningMainLoop;
    Button start, stop;
    private Runnable run;
    private boolean mStop = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_test);
        mSerial = new FTDriver((UsbManager) getSystemService(Context.USB_SERVICE));

        PendingIntent permissionIntent = PendingIntent.getBroadcast(this, 0, new Intent(ACTION_USB_PERMISSION), 0);
        mSerial.setPermissionIntent(permissionIntent);

        mY = (TextView) findViewById(R.id.xValue);
        mY2 = (TextView) findViewById(R.id.yValue);
        mY3 = (TextView) findViewById(R.id.zValue);

        start = (Button) findViewById(R.id.button1);
        stop = (Button) findViewById(R.id.button2);

        start.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                if (mSerial.begin(SERIAL_BAUDRATE)) {
                    mainloop();
                    mStop = false;
                    start.setEnabled(false);
                    stop.setEnabled(true);
                }
            }
        });

        stop.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mStop = true;
                stop.setEnabled(false);
                start.setEnabled(true);
            }
        });
    }

    private void mainloop() {
        mRunningMainLoop = true;
        new Thread(mLoop).start();
    }

    private Runnable mLoop = new Runnable() {
        @Override
        public void run() {

            int i, len;

            // [FTDriver] Create Read Buffer
            byte[] rbuf = new byte[4096]; // 1byte <--slow-- [Transfer Speed] --fast--> 4096 byte
            while (true) {
                for (; ; ) {
                    // [FTDriver] Read from USB serial
                    len = mSerial.read(rbuf);
                    rbuf[len] = 0;
                    String str1 = new String(rbuf);

                    if (len > 72) {

                        String[] new_str1 = str1.split(";", 0);
                        int youso = new_str1.length;
                        if (youso == 16) {
                            String new_str1a = new_str1[12];
                            int a = Integer.parseInt(new_str1a);
                            double g_str1 = 0, doublecount = a;
                            g_str1 = doublecount / 100;

                            String new_str2a = new_str1[13];
                            int b = Integer.parseInt(new_str2a);
                            double g_str2 = 0, doublecount2 = b;
                            g_str2 = doublecount2 / 100;


                            String new_str3a = new_str1[14];
                            int c = Integer.parseInt(new_str3a);
                            double g_str3 = 0, doublecount3 = c;
                            g_str3 = doublecount3 / 100;

                            for (i = 0; i < len; ++i) {
                                if (rbuf[i] == 0x0A) {
                                    if (a > -10000 && a < 10000) {
                                        mText1 = String.format("%.2f", g_str1);
                                    }
                                    if (b > -10000 && b < 10000) {
                                        mText2 = String.format("%.2f", g_str2);
                                    }
                                    if (c > -10000 && c < 10000) {
                                        mText3 = String.format("%.2f", g_str3);
                                    }

                                }
                            }

                        }



                        mHandler.post(new Runnable() {
                            public void run() {
                                mY.setText(mText1);
                                mY2.setText(mText2);
                                mY3.setText(mText3);
                            }


                        });
                        if (mStop) {
                            mRunningMainLoop = false;
                            return;
                        }

                    }

                }

            }
        }
    };
}


