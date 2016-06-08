package com.example.student.pbl;

import android.app.Activity;
import android.os.Bundle;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbManager;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Timer;
import java.util.TimerTask;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Paint.Align;
import android.hardware.usb.UsbManager;
import android.os.Bundle;
import android.os.Handler;
import android.text.format.Time;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import android.view.Window;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.CheckBox;
import android.view.View.OnClickListener;

import org.achartengine.ChartFactory;
import org.achartengine.GraphicalView;
import org.achartengine.chart.PointStyle;
import org.achartengine.model.SeriesSelection;
import org.achartengine.model.XYMultipleSeriesDataset;
import org.achartengine.model.XYSeries;
import org.achartengine.renderer.XYMultipleSeriesRenderer;
import org.achartengine.renderer.XYSeriesRenderer;

import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;

import jp.ksksue.driver.serial.FTDriver;

import jp.ksksue.driver.serial.FTDriver;

public class TestActivity extends Activity {

    TextView mY0,mY, mY2, mY3;
    int d;
    private EditText FileName;
    FTDriver mSerial;
    Handler mHandler = new Handler();
    Handler sHandler = new Handler();
    Handler tHandler = new Handler();
    private String mText0, mText1, mText2, mText3;
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";
    private boolean mRunningMainLoop;
    Button start, stop;


    private boolean mStop = false;

   // private int cnt =0;
    //////////////////////////////
/*    String mDataset;
    String mRenderer;
    String mCurrentSeries;
    String mCurrentRenderer;
    */
/*
    private XYMultipleSeriesDataset mDataset = new XYMultipleSeriesDataset();
    private XYMultipleSeriesRenderer mRenderer = new XYMultipleSeriesRenderer();
    private XYSeries mCurrentSeries,mCurrentSeries2,mCurrentSeries3;
    private XYSeriesRenderer mCurrentRenderer;
    private GraphicalView mChartView;
    */
    ////////////////////////////////////////////////////
//    Timer timer;
    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        // save the current data, for instance when changing screen orientation
 /*         outState.putString("dataset", "不明");
        outState.putString("renderer", "不明");
        outState.putString("current_series", "不明");
        outState.putString("current_renderer", "不明");
*/
    }

    @Override
    protected void onRestoreInstanceState(Bundle savedState) {
        super.onRestoreInstanceState(savedState);
        // restore the current data, for instance when changing the screen
        // orientation


/*        mY0=(TextView)findViewById(R.id.dValue);
        mY = (TextView) findViewById(R.id.xValue);
        mY2 = (TextView) findViewById(R.id.yValue);
        mY3 = (TextView) findViewById(R.id.zValue);
*/
 /*        mDataset = (String) savedState.getSerializable("dataset");
         mRenderer = (String) savedState.getSerializable("renderer");
         mCurrentSeries = (String) savedState.getSerializable("current_series");
       mCurrentRenderer = (String) savedState.getSerializable("current_renderer");
*/


/*
            mY0.setText("省電力モードではありません");
            mY.setText(0);
            mY2.setText(0);
            mY3.setText(0);
*/

    }

    @Override
    protected void onResume() {
        super.onResume();
 /*      if(cnt > 1) {
           mRunningMainLoop = false;
            mainloop();
         mSerial = new FTDriver((UsbManager) getSystemService(Context.USB_SERVICE));
          PendingIntent permissionIntent = PendingIntent.getBroadcast(this, 0, new Intent(ACTION_USB_PERMISSION), 0);
           mSerial.setPermissionIntent(permissionIntent);


       }
       */
/*
        LinearLayout layout = (LinearLayout) findViewById(R.id.chart);
        mChartView = ChartFactory.getLineChartView(this, mDataset, mRenderer);
        // enable the chart click events
        mRenderer.setClickEnabled(true);
        mRenderer.setSelectableBuffer(10);
        mChartView.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // handle the click event on the chart
                SeriesSelection seriesSelection = mChartView.getCurrentSeriesAndPoint();
                if (seriesSelection == null) {

                }
            }
        });
        layout.addView(mChartView, new LayoutParams(LayoutParams.FILL_PARENT,
                LayoutParams.FILL_PARENT));
        boolean enabled = mDataset.getSeriesCount() > 0;
        setSeriesWidgetsEnabled(enabled);
    } else {
        mChartView.repaint();
    }
*/
    }

    ////////////////////////////////////////////////////

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_test);
        mSerial = new FTDriver((UsbManager) getSystemService(Context.USB_SERVICE));

        PendingIntent permissionIntent = PendingIntent.getBroadcast(this, 0, new Intent(ACTION_USB_PERMISSION), 0);
        mSerial.setPermissionIntent(permissionIntent);

       mY0=(TextView)findViewById(R.id.dValue);
        mY = (TextView) findViewById(R.id.xValue);
        mY2 = (TextView) findViewById(R.id.yValue);
        mY3 = (TextView) findViewById(R.id.zValue);

        start = (Button) findViewById(R.id.button1);
        stop = (Button) findViewById(R.id.button2);
 /*       if(cnt > 1) {
            mainloop();
            mY0.setText("未取得中");
        }

        cnt++;
        */

        mY0.setText("未取得中");
        mY.setText("未取得中");
        mY2.setText("未取得中");
        mY3.setText("未取得中");


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


            byte[] rbuf = new byte[4096]; // 1byte <--slow-- [Transfer Speed] --fast--> 4096 byte
            while (true) {
                len = 0;//
                for (;;) {

                    // [FTDriver] Read from USB serial
                    len = mSerial.read(rbuf);
                    rbuf[len] = 0;
                    String str1 = new String(rbuf);
                    d=0;

                    if(len < 8 && len > 0 ) {
                        tHandler.post(new Runnable() {
                            public void run() {

                                mY0.setText("生存信号");
                                //mY.setText(mText1);
                                //mY2.setText(mText2);
                                //mY3.setText(mText3);
                                // mLoop = false;
                                // mHandler.postDelayed(this, 100);

                            }

                        });
                        try {
                            Thread.sleep(500);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }

                    }else

                    if (len > 72) {

                        String[] new_str1 = str1.split(";", 0);
                        int youso = new_str1.length;

                        if (youso >= 16) {

                            String new_str0a = new_str1[11];
                            d = Integer.parseInt(new_str0a);
                            //if(d != 1){d=0;}
                            double g_str0 = 0, doublecount0 = d;
                            g_str0 = doublecount0 / 100;

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
                                     if (d > -10000 && d < 10000) {
                                        mText0 = String.format("%.2f", g_str0);
                                    }
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
                       // d=0;

                        if(d == 1) {
                            mHandler.post(new Runnable() {
                                public void run() {

                                    mY0.setText("通常モード");
                                    mY.setText(mText1);
                                    mY2.setText(mText2);
                                    mY3.setText(mText3);
                                   // mLoop = false;
                                   // mHandler.postDelayed(this, 100);

                                }

                            });
                            try {
                                Thread.sleep(500);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }

                        }






                        if (mStop) {
                            mRunningMainLoop = false;
                            return;
                        }

                    }else {
                        if(d != 1) {
                          try {
                                Thread.sleep(100);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }

                            sHandler.post(new Runnable() {
                               public void run() {
                                  mY0.setText("省電力モード");
                                    mY.setText("省電力中");
                                    mY2.setText("省電力中");
                                    mY3.setText("省電力中");
                                   //mHandler.postDelayed(this, 500);

                                }


                            });


                        }


                    }
                   // d=0;//ポイントはここ

                }
               // d=0;

            }

           // d=0;
        }
       // d=0;
    };


}
