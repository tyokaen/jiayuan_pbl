package com.example.pzl.pblb;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.view.View;
import android.view.Window;
import android.widget.Button;

import java.io.File;
import java.io.FileOutputStream;
import java.util.ArrayList;

import jp.ksksue.driver.serial.FTDriver;


public class MainActivity extends Activity {
    boolean flag = false;
    HttpClientTask task = new HttpClientTask();
    FTDriver mSerial;
    Handler mHandler = new Handler();
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private boolean mStop = false;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";
    private boolean mRunningMainLoop;
    Button start, stop;
    int mn = 0;



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

        start = (Button) findViewById(R.id.button1);
        stop = (Button) findViewById(R.id.button2);

        //測定開始ボタンの処理
        start.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
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
            int len = 0;
            ArrayList<byte[]> p = new ArrayList<>();
            while (true) {
                // [FTDriver] Create Read Buffer
                byte[] rbuf = new byte[128];
                len = mSerial.read(rbuf);
                if (len != 0) {
                    if((rbuf[0]&0xFF)==0x81){
                        p.add(rbuf);
                    }

                    /*
                    try{
                        for(int n=0;n<rbuf.length;n++){
                            //String a = "";
                            String s = String.format("%8s", Integer.toBinaryString(rbuf[n] & 0xFF)).replace(' ', '0');
                            String hex = Long.toHexString(Long.parseLong(s, 2));
                            String ss = String.format("%" + (int) (Math.ceil(s.length() / 4.0)) + "s", hex).replace(' ', '0');
                            if((rbuf[n]&0xFF)==0x81){
                                saveToSDCard1("pbl_seebinary.txt","■ID："+ss + " ");
                            }else {
                                saveToSDCard1("pbl_seebinary.txt", ss + " ");
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    */


                    //for (int m = 0; m < rbuf.length; m++) {

                    //if(((rbuf[m] & 0xFF) == 0x81)&&(m<12)){

                    // }
                    //count0结束 开始suck count1！！！！！！！！


/*
                    String[] new_str1 = str1.split(",", 0);
                    int youso = new_str1.length;
                    if (youso != 2) {
                        try {
                            //String printMe = new String(encoded, "US-ASCII");
                            //saveToSDCard1("pbl_orange.txt", printMe);
                            String a="";
                            for(int i=0;i<4;i++) {
                                if(rbuf[i] != 0x00) {
                                    String s = String.format("%8s", Integer.toBinaryString(rbuf[i] & 0xFF)).replace(' ', '0');
                                    String hex = Long.toHexString(Long.parseLong(s, 2));
                                    String ss = String.format("%" + (int)(Math.ceil(s.length() / 4.0)) + "s", hex).replace(' ', '0');
                                    //saveToSDCard1("pbl_orange_bs_true.txt", s);
                                    a=a+ss;
                                }
                            }
                            //int ab = Integer.parseInt(a, 2);

                            saveToSDCard1("pbl_seebinary.txt","■ID:"+a+",");

                            String a1 = String.format("%8s", Integer.toBinaryString(rbuf[4] & 0xFF)).replace(' ', '0');
                            int ab1 = Integer.parseInt(a1, 2);
                            saveToSDCard1("pbl_seebinary.txt","Mode:"+ab1+",");


                            if((rbuf[5] & 0xFF)==0xFF){
                                String a22 = String.format("%8s", Integer.toBinaryString(rbuf[6] & 0xFF)).replace(' ', '0');
                                String a23 = String.format("%8s", Integer.toBinaryString(rbuf[7] & 0xFF)).replace(' ', '0');

                                int ab2 = Integer.parseInt(a22+a23, 2);
                                saveToSDCard1("pbl_seebinary.txt","Time:"+ab2+"　");
                            }else {
                                String a21 = String.format("%8s", Integer.toBinaryString(rbuf[5] & 0xFF)).replace(' ', '0');
                                String a22 = String.format("%8s", Integer.toBinaryString(rbuf[6] & 0xFF)).replace(' ', '0');
                                String a23 = String.format("%8s", Integer.toBinaryString(rbuf[7] & 0xFF)).replace(' ', '0');

                                int ab2 = Integer.parseInt(a21+a22+a23, 2);
                                saveToSDCard1("pbl_seebinary.txt","Time:"+ab2+"　");
                            }


                            for(int i=8;i<rbuf.length;i=i+2){
                                if((rbuf[i] & 0xFF)==0x07){
                                    String bb2 = String.format("%8s", Integer.toBinaryString(rbuf[i+1] & 0xFF)).replace(' ', '0');
                                    int bb22 = Integer.parseInt(bb2, 2);
                                    saveToSDCard1("pbl_seebinary.txt",","+bb22);
                                }else{
                                    if((rbuf[i] & 0xFF)>0x80){
                                        //String bbb=String.format("%8s", Integer.toBinaryString((rbuf[i] & 0xFF)-0x80)).replace(' ', '0');
                                        //String bb2 = String.format("%8s", Integer.toBinaryString(rbuf[i+1] & 0xFF)).replace(' ', '0');
                                        //int bb22 = Integer.parseInt(bbb+bb2, 2);
                                        //bb22 = 0-bb22;
                                        saveToSDCard1("pbl_seebinary.txt","xxxxxx");
                                    }else {
                                        String bb = String.format("%8s", Integer.toBinaryString(rbuf[i] & 0xFF)).replace(' ', '0');
                                        String bb2 = String.format("%8s", Integer.toBinaryString(rbuf[i+1] & 0xFF)).replace(' ', '0');
                                        int bb22 = Integer.parseInt(bb+bb2, 2);
                                        saveToSDCard1("pbl_seebinary.txt",","+bb22);
                                    }
                                }
                            }

                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
*/
                }
                if (mStop) {
                    mRunningMainLoop = false;

                    try {
                        for (int nn = 0; nn < p.size(); nn++) {
                            String a = "";
                            String onerow="";
                            for (int i = 0; i < 4; i++) {
                                String s = String.format("%8s", Integer.toBinaryString(p.get(nn)[i] & 0xFF)).replace(' ', '0');
                                String hex = Long.toHexString(Long.parseLong(s, 2));
                                String ss = String.format("%" + (int) (Math.ceil(s.length() / 4.0)) + "s", hex).replace(' ', '0');
                                a = a + ss;
                            }
                            //int ab = Integer.parseInt(a, 2);
                            onerow="■ID:" + a + ",";
                            //saveToSDCard1("pbl_seebinary.txt", "■ID:" + a + ",");

                            String a1 = String.format("%8s", Integer.toBinaryString(p.get(nn)[4] & 0xFF)).replace(' ', '0');
                            int ab1 = Integer.parseInt(a1, 2);
                            onerow=onerow+"Mode:" + ab1 + ",";
                            //saveToSDCard1("pbl_seebinary.txt", "Mode:" + ab1 + ",");

                            if ((p.get(nn)[5] & 0xFF) == 0xFF) {
                                String a22 = String.format("%8s", Integer.toBinaryString(p.get(nn)[6] & 0xFF)).replace(' ', '0');
                                String a23 = String.format("%8s", Integer.toBinaryString(p.get(nn)[7] & 0xFF)).replace(' ', '0');
                                int ab2 = Integer.parseInt(a22 + a23, 2);
                                onerow=onerow+"Time:" + ab2 + "　";
                                //saveToSDCard1("pbl_seebinary.txt", "Time:" + ab2 + "　");
                            } else {
                                String a21 = String.format("%8s", Integer.toBinaryString(p.get(nn)[5] & 0xFF)).replace(' ', '0');
                                String a22 = String.format("%8s", Integer.toBinaryString(p.get(nn)[6] & 0xFF)).replace(' ', '0');
                                String a23 = String.format("%8s", Integer.toBinaryString(p.get(nn)[7] & 0xFF)).replace(' ', '0');

                                int ab2 = Integer.parseInt(a21 + a22 + a23, 2);
                                onerow=onerow+"Time:" + ab2 + "　";
                                //saveToSDCard1("pbl_seebinary.txt", "Time:" + ab2 + "　");
                            }

                            for (int i = 8; i < 68; i = i + 2) {
                                if ((p.get(nn)[i] & 0xFF) == 0x07) {
                                    String bb2 = String.format("%8s", Integer.toBinaryString(p.get(nn)[i+1] & 0xFF)).replace(' ', '0');
                                    int bb22 = Integer.parseInt(bb2, 2);
                                    if (bb22 > 127) {
                                        bb22 = bb22 - 256;
                                    }
                                    onerow=onerow+"," + bb22;
                                    //saveToSDCard1("pbl_seebinary.txt", "," + bb22);
                                } else {
                                    String bbb = String.format("%8s", Integer.toBinaryString(p.get(nn)[i] & 0xFF)).replace(' ', '0');
                                    String bb2 = String.format("%8s", Integer.toBinaryString(p.get(nn)[i+1] & 0xFF)).replace(' ', '0');
                                    int bb22 = Integer.parseInt(bbb + bb2, 2);
                                    if (bb22 > 32767) {
                                        bb22 = bb22 - 65536;
                                    }
                                    if (bb22 == 1700) {
                                        bb22 = 0;
                                    }
                                    onerow=onerow+"," + bb22;
                                    //saveToSDCard1("pbl_seebinary.txt", "," + bb22);
                                }
                            }
                            saveToSDCard1("pbl_seebinary.txt", onerow);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    return;
                }
            }
        }
        // }
    };

    private Runnable mLoop1 = new Runnable() {
        @Override
        public void run() {
            int len = 0;
            while (true) {
                // [FTDriver] Create Read Buffer
                byte[] rbuf = new byte[128];
                len = mSerial.read(rbuf);
                String str1 = new String(rbuf);
                if (len != -1) {
                    String[] new_str1 = str1.split(",", 0);
                    int youso = new_str1.length;
                    if (youso == 33) {
                        try {
                            saveToSDCard("pbl_orange.txt", rbuf);
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


    public void saveToSDCard(String filename, byte[] ss) throws Exception {
        File file = new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out = new FileOutputStream(file, true);//true ==> mode is APPEND; false ==> mode is PRIVATE;
        out.write(ss);
        out.close();
    }

    public void saveToSDCard2(String filename, byte[] ss) throws Exception {
        File file = new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out = new FileOutputStream(file, true);
        out.write(ss);
        out.close();
    }

    public void saveToSDCard1(String filename, String ss) throws Exception {
        File file = new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out = new FileOutputStream(file, true);
        out.write(ss.getBytes());
        out.close();
    }


}
