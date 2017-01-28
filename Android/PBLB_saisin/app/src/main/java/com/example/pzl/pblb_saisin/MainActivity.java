package com.example.pzl.pblb_saisin;

import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.PowerManager;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;

import java.io.File;
import java.io.FileOutputStream;

import jp.ksksue.driver.serial.FTDriver;

public class MainActivity extends AppCompatActivity {
    TextView ck_text, ck11, ck22, ck33, ck44,t;
    private static String TAG = "com.example.pblb_saisin.MainActivity";

    MyWakefulReceiver mwr = new MyWakefulReceiver();
    private Context context;

    String finame;
    private EditText FileName;
    double x, y, y2, y3;
    int count = 0;
    boolean flag = false;
    CheckBox checkBox1, checkBox2, checkBox3, checkBox4;
    FTDriver mSerial;
    final int mOutputType = 0;
    int i = 0;
    Handler mHandler = new Handler();
    String result;
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private String mText1, mText2, mText3, getcount, getmY, getmY2, getmY3, AmY, AmY2, AmY3;
    private boolean mStop = false;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";
    private boolean mRunningMainLoop;
    //public int currentTime;
    private Handler myHandler, pHandler, myHandler2;
    Button start, stop;


    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
    }

    @Override
    protected void onRestoreInstanceState(Bundle savedState) {
        super.onRestoreInstanceState(savedState);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        PowerManager powerManager = (PowerManager) getSystemService(POWER_SERVICE);
        final PowerManager.WakeLock wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,
                "MyWakelockTag");
        wakeLock.acquire();


        //currentTime = 0;
        mSerial = new FTDriver((UsbManager) getSystemService(Context.USB_SERVICE));

        // [FTDriver] setPermissionIntent() before begin()
        PendingIntent permissionIntent = PendingIntent.getBroadcast(this, 0, new Intent(
                ACTION_USB_PERMISSION), 0);
        mSerial.setPermissionIntent(permissionIntent);

        //myTask = new MyTimerTask();
        myHandler = new Handler();

        myHandler2 = new Handler();
        start = (Button) findViewById(R.id.button1);
        stop = (Button) findViewById(R.id.button2);


        //測定開始ボタンの処理
        start.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                //Intent intent = new Intent("com.example.pblb_saisin.RECEIVE");
                //sendBroadcast(intent);
                //startService(new Intent(MainActivity.this,MyService.class));
                mStop = false;
                if (mSerial.begin(SERIAL_BAUDRATE)) {
                    mainloop();
                    start.setEnabled(false);
                    stop.setEnabled(true);
                }
            }
        });
        //測定開始ボタンの処理
        stop.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                //stopService(new Intent(MainActivity.this,MyService.class));
                wakeLock.release();
                mStop = true;
                stop.setEnabled(false);
                start.setEnabled(true);
            }
        });
    }

    private void mainloop() {
        mRunningMainLoop = true;
        new Thread(mLoop1).start();
    }

    private Runnable mLoop = new Runnable() {
        @Override
        public void run() {
            int len = 0;
            while (true) {
                // [FTDriver] Create Read Buffer
                byte[] rbuf = new byte[128];

                len = mSerial.read(rbuf);
                //String str1=new String(rbuf);

                if(len!=0) {
                    //String[] new_str1 = str1.split(",", 0);
                    //int youso = new_str1.length;
                    if (flag == false) {
                        if ((rbuf[0]&0xFF)!=0x00) {
                            flag = true;
                            try {
                                HttpClientTask task=new HttpClientTask();
                                finame = task.saveToSDCard(rbuf);
                                task.execute();

                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                            mHandler.postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    flag = false;
                                    try {
                                    } catch (Exception e) {
                                        e.printStackTrace();
                                    }
                                }
                            }, 5000);
                        }else{
                            try {
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    } else {
                            //if(youso>2){
                                try{
                                    saveToSDCard2(finame,rbuf);
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                            }

                    }
                    if (mStop) {
                        mRunningMainLoop = false;
                        return;
                    }
                }
            }

    };

    private Runnable mLoop1 = new Runnable() {
        @Override
        public void run() {
            int len = 0;
            while (true) {
                // [FTDriver] Create Read Buffer
                byte[] rbuf = new byte[128];

                len = mSerial.read(rbuf);
                String str1=new String(rbuf);

                if(len!=0) {
                    String[] new_str1 = str1.split(",", 0);
                    int youso = new_str1.length;
                    if (flag == false) {
                        if (youso != 2) {
                            flag = true;
                            try {
                                HttpClientTask task=new HttpClientTask();
                                finame = task.saveToSDCard(rbuf);
                                task.execute();

                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                            mHandler.postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    flag = false;
                                    try {
                                    } catch (Exception e) {
                                        e.printStackTrace();
                                    }
                                }
                            }, 5000);
                        }else{
                            try {
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    } else {
                        if(youso!=2){
                            try{
                                saveToSDCard2(finame,rbuf);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }

                    }
                    if (mStop) {
                        mRunningMainLoop = false;
                        return;
                    }
                }
            }
        }
    };

    public void saveToSDCard2(String filename,byte[] ss) throws Exception{
        File file=new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out=new FileOutputStream(file,true);

        out.write(ss);
        out.close();
    }

    public void saveToSDCard3(String filename,byte[] ss) throws Exception{
        File file=new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out=new FileOutputStream(file,true);

        out.write(ss);
        out.close();
    }

/*
    public void saveToSDCard_list(String filename,ArrayList ss) throws Exception{
        File file=new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out=new FileOutputStream(file,true);//true ==> mode is APPEND; false ==> mode is PRIVATE;
        for(int m  =0; m < ss.size();m++)
        {
            out.write((byte[])ss.get(m));
        }
        out.close();
    }
*/
/*
    int j=0;
    byte[] rb = new byte[rbuf.length];
    for(int i=0;i<rbuf.length;i++) {
        if(rbuf[i] != 0x00){
            rb[j] = rbuf[i];
            j=j+1;
        }
    }
*/
}
