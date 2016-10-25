package com.example.pzl.pblb;

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
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import jp.ksksue.driver.serial.FTDriver;


public class MainActivity extends Activity {
    TextView ck_text, ck11, ck22, ck33, ck44;
    private EditText FileName;
    double x, y, y2, y3;
    int count = 0;
    boolean flag = false;
    CheckBox checkBox1, checkBox2, checkBox3, checkBox4;
    FTDriver mSerial;
    final int mOutputType = 0;
    int i = 0;
    Handler mHandler = new Handler();
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private String mText1, mText2, mText3, getcount, getmY, getmY2, getmY3, AmY, AmY2, AmY3;
    private boolean mStop = false;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";
    private boolean mRunningMainLoop;
    //public int currentTime;
    private Handler myHandler, pHandler, myHandler2;
    private Runnable myTask, pTask, myTask2;
    Button start, stop, check;
    private BufferedWriter bw;
    private LinearLayout mainLayout;

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        // save the current data, for instance when changing screen orientation
    }

    @Override
    protected void onRestoreInstanceState(Bundle savedState) {
        super.onRestoreInstanceState(savedState);
        // restore the current data, for instance when changing the screen
        // orientation
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // タイトルを非表示にします。
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);

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
        check = (Button) findViewById(R.id.button3);

        ck_text = (TextView) findViewById(R.id.checktext);
        ck11 = (TextView) findViewById(R.id.ck1);
        ck22 = (TextView) findViewById(R.id.ck2);

        //測定開始ボタンの処理
        start.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                //myHandler.postDelayed(myTask, 100);
                //myHandler3.postDelayed(myTask3, 100);
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
                //cancelTimer();
                mStop = true;
                stop.setEnabled(false);
                start.setEnabled(true);

            }
        });

        check.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                readFileData("data");
            }
        });
    }
/*
    private void cancelTimer() {
        if (myHandler != null) {
            myHandler.removeCallbacks(myTask);
        }
    }
*/

    private void mainloop() {
        mRunningMainLoop = true;
        new Thread(mLoop).start();
    }

    private Runnable mLoop = new Runnable() {
        @Override
        public void run() {
            int len = 0;
            while (true) {
                // [FTDriver] Create Read Buffer
                byte[] rbuf = new byte[256];
                len = mSerial.read(rbuf);
                String str1=new String(rbuf);
                if (len != -1) {
                    String[] new_str1 = str1.split(",", 0);
                    int youso = new_str1.length;
                    if (flag == false) {

                        if (youso > 2) {
                            flag = true;
                            save3("data", rbuf);
                            mHandler.postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    flag = false;
                                }
                            }, 5000);
                        }else{
                            save("data", "生存信号");
                        }

                    } else {
                        save2("data", rbuf);
                    }

                    if (mStop) {
                        mRunningMainLoop = false;
                        return;

                    }
                }
            }
            //}
        }

        ;

    };

    /*
        public Runnable runnable=new Runnable() {
            public void run() {
                mHandler.postDelayed(runnable,1000);
                if(i==4){
                    flag=false;
                    i=0;
                    mHandler.removeCallbacks(runnable);

                }
                i++;

            }
        };
*/
    public void save(String filename, String message) {
        try {
            //ck33.setText("3 is done");
            FileOutputStream outStream = openFileOutput(filename, MODE_PRIVATE);
            byte[] b = message.getBytes();
            outStream.write(b);
            outStream.close();
            //Toast.makeText(MainActivity.this,"Saved", Toast.LENGTH_LONG).show();
        } catch (FileNotFoundException e) {
            return;
        } catch (IOException e) {
            return;
        }
    }

    public void save3(String filename, byte[] z) {
        try {
            //ck33.setText("3 is done");
            FileOutputStream outStream = openFileOutput(filename, MODE_PRIVATE);
            outStream.write(z);
            outStream.close();
            //Toast.makeText(MainActivity.this,"Saved", Toast.LENGTH_LONG).show();
        } catch (FileNotFoundException e) {
            return;
        } catch (IOException e) {
            return;
        }
    }

    public void save2(String filename, byte[] z) {
        try {
            //ck33.setText("3 is done");
            FileOutputStream outStream = openFileOutput(filename, MODE_APPEND);
            outStream.write(z);
            outStream.close();
            //Toast.makeText(MainActivity.this,"Saved", Toast.LENGTH_LONG).show();
        } catch (FileNotFoundException e) {
            return;
        } catch (IOException e) {
            return;
        }
    }

    public void readFileData(String fileName) {
        try {
            //ck44.setText("4 is done");
            FileInputStream fin = openFileInput(fileName);
            StringBuffer fileContent = new StringBuffer("");
            byte[] buffer = new byte[4096];
            int n;
            while((n = fin.read(buffer)) != -1)
            {
                fileContent.append(new String(buffer, "UTF-8"));
            }

            /*for (int i = 0; i < length; i++){
                res.concat(String.format("%8s", Integer.toBinaryString(buffer[i] & 0xFF).replace(' ', '0')));
            }*/

            //res = new String(buffer);
            ck_text.setText(fileContent);
            fin.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
