package com.example.pzl.pblb;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;

import jp.ksksue.driver.serial.FTDriver;


public class MainActivity extends Activity {
    TextView ck_text, ck11, ck22, ck33, ck44,t;


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
    private Runnable myTask, pTask, myTask2;
    Button start, stop,btn_right,btn_false;
    private BufferedWriter bw;
    private LinearLayout mainLayout;
    private  TextView tx_rec;
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
        btn_right=(Button)findViewById(R.id.Right);
        btn_false=(Button)findViewById(R.id.False);
        tx_rec=(TextView)findViewById(R.id.Tx_Receive);

       btn_right.setOnClickListener(new View.OnClickListener() {
           @Override
           public void onClick(View view) {
               try {
                   saveToSDCard1("zhang.csv","True"+result);
               } catch (Exception e) {
                   e.printStackTrace();
               }
               new Thread(new Runnable() {
                   @Override
                   public void run() {
                       HttpClientTask_result task=new HttpClientTask_result();
                       task.send();
                   }
               }).start();

           }
       });

        btn_false.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Input();
            }
        });






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
/*
        fff.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                task.execute();
            }
        });
*/
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

    public void Input() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("正しい振動入力");
        final EditText editText = new EditText(this);
        builder.setView(editText);
        builder.setPositiveButton("送信", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialogInterface, int i) {
                try {
                    saveToSDCard1("zhang.csv",editText.getText().toString()+result);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        HttpClientTask_result task=new HttpClientTask_result();
                        task.send();
                    }
                }).start();
            }
        });
        builder.setCancelable(false);
        builder.setNegativeButton("キャンセル", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialogInterface, int i) {
            }
        });
        AlertDialog alertDialog = builder.create();
        alertDialog.show();
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
                            try {
                                saveToSDCard("pbl_orange.csv", rbuf);
                                HttpClientTask task=new HttpClientTask(tx_rec);
                                task.execute();
                            } catch (Exception e) {
                                e.printStackTrace();
                            }


                            mHandler.postDelayed(new Runnable() {
                                @Override
                                public void run() {
                                    flag = false;
                                }
                            }, 5000);
                        }else{
                            try {
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }

                    } else {
                        try {
                            saveToSDCard2("pbl_orange.csv", rbuf);
                        } catch (Exception e) {
                            e.printStackTrace();
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

    public void saveToSDCard(String filename,byte[] ss) throws Exception{
        File file=new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out=new FileOutputStream(file,false);//true ==> mode is APPEND; false ==> mode is PRIVATE;
        out.write(ss);
        out.close();
    }

    public void saveToSDCard2(String filename,byte[] ss) throws Exception{
        File file=new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out=new FileOutputStream(file,true);
        out.write(ss);
        out.close();
    }

    public void saveToSDCard1(String filename,String ss) throws Exception{
        File file=new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out=new FileOutputStream(file,false);
        out.write(ss.getBytes());
        out.close();
    }

}
