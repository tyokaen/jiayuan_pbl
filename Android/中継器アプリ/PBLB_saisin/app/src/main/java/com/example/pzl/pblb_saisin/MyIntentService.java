package com.example.pzl.pblb_saisin;

import android.app.IntentService;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.support.v4.app.NotificationCompat;

import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import jp.ksksue.driver.serial.FTDriver;

/**
 * An {@link IntentService} subclass for handling asynchronous task requests in
 * a service on a separate handler thread.
 * <p>
 * TODO: Customize class - update intent actions, extra parameters and static
 * helper methods.
 */
public class MyIntentService extends IntentService {
    public static final int NOTIFICATION_ID = 1;
    private NotificationManager mNotificationManager;
    NotificationCompat.Builder builder;
    private static final String ACTION_FOO = "com.example.pzl.pblb_saisin.action.FOO";
    private static final String ACTION_BAZ = "com.example.pzl.pblb_saisin.action.BAZ";
    private static final String EXTRA_PARAM1 = "com.example.pzl.pblb_saisin.extra.PARAM1";
    private static final String EXTRA_PARAM2 = "com.example.pzl.pblb_saisin.extra.PARAM2";
    FTDriver mSerial;
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";

    HttpClient httpClient;
    private String mUri = "http://130.158.80.39:8080/cgi-bin/form3.py";
    boolean flag = false;
    String finame;
    private Handler mHandler = new Handler();
    String fim="";
    String fim1="";
    public MyIntentService() {
        super("MyIntentService");
    }
    @Override
    protected void onHandleIntent(Intent intent) {
        Bundle extras = intent.getExtras();

        mSerial = new FTDriver((UsbManager) getSystemService(Context.USB_SERVICE));
        //[FTDriver] setPermissionIntent() before begin()
        PendingIntent permissionIntent = PendingIntent.getBroadcast(this, 0, new Intent(
                ACTION_USB_PERMISSION), 0);
        mSerial.setPermissionIntent(permissionIntent);

        if(mSerial.begin(SERIAL_BAUDRATE)){
            new Thread() {
                @Override
                public void run() {
                    super.run();
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
                                if (youso > 2) {
                                    flag = true;
                                    try {
                                        finame = saveToSDCard(rbuf);
                                        MyTask myTask = new MyTask();
                                        myTask.execute();
                                    } catch (Exception e) {
                                        e.printStackTrace();
                                    }
                                    mHandler.postDelayed(new Runnable() {
                                        @Override
                                        public void run() {
                                            flag = false;
                                        }
                                    }, 5000);
                                } else {
                                    try {
                                    } catch (Exception e) {
                                        e.printStackTrace();
                                    }
                                }
                            } else {
                                try {
                                    saveToSDCard2(finame, rbuf);
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                            }
                        }
                    }
                }
            }.start();
        }
        // Do the work that requires your app to keep the CPU running.
        // ...
        // Release the wake lock provided by the WakefulBroadcastReceiver.
        MyWakefulReceiver.completeWakefulIntent(intent);
    }

    public void saveToSDCard2(String filename, byte[] ss) throws Exception {
        File file = new File(Environment.getExternalStorageDirectory(), filename);
        FileOutputStream out = new FileOutputStream(file, true);
        out.write(ss);
        out.close();
    }

    public String saveToSDCard(byte[] ss) throws Exception {
        SimpleDateFormat df = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss_SSS");
        fim = "pbl_" + df.format(new Date()) + ".csv";
        fim1 = fim;
        File file = new File(Environment.getExternalStorageDirectory(), fim1);
        FileOutputStream out = new FileOutputStream(file, false);//true ==> mode is APPEND; false ==> mode is PRIVATE;

        out.write(ss);
        out.close();
        return fim1;
    }

    protected void send(String fm){
        httpClient=new DefaultHttpClient();
        HttpPost post=new HttpPost(mUri);

        ResponseHandler<String> responseHandler=new BasicResponseHandler();
        MultipartEntity multipartEntity=new MultipartEntity(HttpMultipartMode.BROWSER_COMPATIBLE);
        File sdCardDir = Environment.getExternalStorageDirectory();
        File file=new File(sdCardDir,fm);
        FileBody body=new FileBody(file);

        multipartEntity.addPart("jiayuan", body);
        post.setEntity(multipartEntity);
        try {
            httpClient.execute(post);
        } catch (IOException e) {
            e.printStackTrace();
        }

        if (file.exists()){
            if(file.isFile()){
                file.delete();
            }
        }

    }

    private class MyTask extends AsyncTask<String, Integer, String> {
        @Override
        protected void onPreExecute() {
        }

        //doInBackground方法内部执行后台任务,不可在此方法内修改UI
        @Override
        protected String doInBackground(String... params) {
            try {
                Thread.sleep(5000);
                send(finame);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            return null;
        }

        //onProgressUpdate方法用于更新进度信息
        @Override
        protected void onProgressUpdate(Integer... progresses) {
        }

        //onPostExecute方法用于在执行完后台任务后更新UI,显示结果
        @Override
        protected void onPostExecute(String result) {

        }

        //onCancelled方法用于在取消执行中的任务时更改UI
        @Override
        protected void onCancelled() {

        }
    }
}
