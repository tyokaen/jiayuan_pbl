package com.example.pzl.pblb_saisin;

import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.hardware.Camera;
import android.hardware.usb.UsbManager;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.PowerManager;
import android.support.v7.app.AppCompatActivity;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

import jp.ksksue.driver.serial.FTDriver;
public class MainActivity extends AppCompatActivity {
    TextView ck_text, ck11, ck22, ck33, ck44, t;
    private static String TAG = "com.example.pblb_saisin.MainActivity";
    public MediaRecorder mediaRecorder=null;
    private boolean isrunning=false;
     private File saveFile;
    MyWakefulReceiver mwr = new MyWakefulReceiver();
    private Context context;
    public Camera camera;
    String finame;
    private EditText FileName;
    double x, y, y2, y3;
    int count = 0;
    boolean flag = false;
    Switch Switch;
    CheckBox checkBox1, checkBox2, checkBox3, checkBox4;
    FTDriver mSerial;
    final int mOutputType = 0;
    int i = 0;
    Handler mHandler = new Handler();
    Handler videoHandler=new Handler();
    HttpVideoTask videoTask=new HttpVideoTask();
    Runnable runnable=null;
    String result;
    int convert;
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private String mText1, mText2, mText3, getcount, getmY, getmY2, getmY3, AmY, AmY2, AmY3;
    private boolean mStop = false;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";
    private boolean mRunningMainLoop;
    //public int currentTime;
    private Handler myHandler, pHandler, myHandler2;
    Button start, stop;
    SurfaceView surfaceView;

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
        Switch=(Switch)findViewById(R.id.camera_choice);
        Switch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                         if(b){
                              convert=1;
                         }
                else{
                             convert=0;
                         }
            }
        });
        surfaceView=(SurfaceView)findViewById(R.id.Surfaceview);
        surfaceView.getHolder().setFixedSize(140, 210);
        surfaceView.getHolder().setKeepScreenOn(true);
        surfaceView.getHolder().setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
        runnable=new Runnable() {

            public void run() {
                videoHandler.postDelayed(this,1000);
                if(i==11){
                    mediaRecorder.stop();
                    mediaRecorder.release();
                    mediaRecorder = null;
                    isrunning = false;
                    videoHandler.removeCallbacks(this);
                    i = 0;
                    camera.stopPreview();
                    camera.release();
                    camera = null;
                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            videoTask.send();
                        }
                    }).start();
                }
                i++;
            }
        };
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
                String str1 = new String(rbuf);
                if (len != -1) {
                    String[] new_str1 = str1.split(",", 0);
                    int youso = new_str1.length;
                    if (flag == false) {
                        if (youso >2) {
                            flag = true;
                            videoHandler.postDelayed(runnable,1000);
                            setViedo(convert);
                            startVideo();
                            try {
                                HttpClientTask task = new HttpClientTask();
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
                        } else {
                            try {
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    } else {
                        if(youso >2) {
                            try {
                                saveToSDCard2(finame, rbuf);
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
    public void saveToSDCard2(String filename, byte[] ss) throws Exception {
        File file = new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out = new FileOutputStream(file, true);
        out.write(ss);
        out.close();
    }
    public void saveToSDCard3(String filename, byte[] ss) throws Exception {
        File file = new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out = new FileOutputStream(file, true);
        out.write(ss);
        out.close();
    }
    public void setViedo(int j) {
        if (!isrunning) {
            mediaRecorder = new MediaRecorder();
            camera = Camera.open(j);
            camera.unlock();
            mediaRecorder.reset();
            mediaRecorder.setCamera(camera);
            mediaRecorder.setPreviewDisplay(surfaceView.getHolder().getSurface());
                    /*设置音频源·*/
            mediaRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                    /*设置视频源*/
            mediaRecorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);
                    /*设置输出格式*/
           mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
                    /*设置音频编码格式*/
            mediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);
            mediaRecorder.setVideoSize(640, 480);
            mediaRecorder.setAudioEncodingBitRate(5 * 200* 100);
            mediaRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);
            mediaRecorder.setAudioChannels(2);
            mediaRecorder.setMaxDuration(10000);
            if(j==1){
                mediaRecorder.setOrientationHint(270);
            }
            else if(j==0) {
                mediaRecorder.setOrientationHint(90);
            }
            mediaRecorder.setMaxFileSize(1024 * 1024);
            saveFile = new File(Environment.getExternalStorageDirectory(), "yuan.mp4");
            mediaRecorder.setOutputFile(saveFile.getAbsolutePath());
        }
    }
    public void startVideo(){
        if(!isrunning){
            try {
               mediaRecorder.prepare();
                mediaRecorder.start();
                isrunning=true;

           } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    public void saveToSDCard_list(String filename,ArrayList ss) throws Exception{
        File file=new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out=new FileOutputStream(file,true);//true ==> mode is APPEND; false ==> mode is PRIVATE;
        for(int m  =0; m < ss.size();m++)
        {
            out.write((byte[])ss.get(m));
        }
        out.close();
    }

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
