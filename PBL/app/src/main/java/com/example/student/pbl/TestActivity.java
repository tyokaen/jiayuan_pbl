package com.example.student.pbl;

import android.app.Activity;
import android.os.Bundle;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.hardware.usb.UsbManager;
import android.os.Handler;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.util.Arrays;
import java.util.Timer;
import java.util.TimerTask;
import android.graphics.Color;
import android.graphics.Paint.Align;
import android.view.ViewGroup.LayoutParams;
import org.achartengine.ChartFactory;
import org.achartengine.GraphicalView;
import org.achartengine.chart.PointStyle;
import org.achartengine.model.XYMultipleSeriesDataset;
import org.achartengine.model.XYSeries;
import org.achartengine.renderer.XYMultipleSeriesRenderer;
import org.achartengine.renderer.XYSeriesRenderer;
import java.io.BufferedWriter;
import jp.ksksue.driver.serial.FTDriver;

public class TestActivity extends Activity {

    TextView mX,mY0,mY, mY2, mY3;
    int i,d,j=0,flag=0,youso=0;
    FTDriver mSerial;
    Handler mHandler = new Handler();
    Handler sHandler = new Handler();
    Handler tHandler = new Handler();
//    Handler pHandler = new Handler();

    String str_alive="alive";
    String str_live="live";
    String str_1="1";
    String str1;

    private  Handler myHandler,myyHandler;
    public double currentTime=0.0,lastTime=0.0,xTime = 0.0;

    private String mText0, mText1, mText2, mText3;
    final int SERIAL_BAUDRATE = FTDriver.BAUD115200;
    private static final String ACTION_USB_PERMISSION =
            "jp.ksksue.tutorial.USB_PERMISSION";
    private boolean mRunningMainLoop;
    Button start, stop;
    double x,y,y2,y3;
    private boolean mStop = false;
 //   int pointview=0;
    //////////////////////////////

    private XYMultipleSeriesDataset mDataset = new XYMultipleSeriesDataset();
    private XYMultipleSeriesRenderer mRenderer = new XYMultipleSeriesRenderer();
    private XYSeries mCurrentSeries,mCurrentSeries2,mCurrentSeries3;
    private XYSeriesRenderer mCurrentRenderer;
    private GraphicalView mChartView;
    private XYSeriesRenderer renderer,renderer2,renderer3 ;

    private BufferedWriter bw;
    private  LinearLayout mainLayout;
    private Runnable pTask,myTask;
    ////////////////////////////////////////////////////

        //データを格納しておく
    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putSerializable("dataset", mDataset);
        outState.putSerializable("renderer", mRenderer);
        outState.putSerializable("current_series", mCurrentSeries);
        outState.putSerializable("current_renderer", mCurrentRenderer);
    }

        //再描画が行われるときに、onSaceInstanceStateに保存しておいたデータをonCreateにデータを投げる
    @Override
    protected void onRestoreInstanceState(Bundle savedState) {
        super.onRestoreInstanceState(savedState);
        mDataset = (XYMultipleSeriesDataset) savedState.getSerializable("dataset");
        mRenderer = (XYMultipleSeriesRenderer) savedState.getSerializable("renderer");
        mCurrentSeries = (XYSeries) savedState.getSerializable("current_series");
        mCurrentRenderer = (XYSeriesRenderer) savedState.getSerializable("current_renderer");
    }

        //表示画面生成
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);////////////////////////
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
///////////////////////////////////////////////////////////////////////////////////////
        myHandler = new Handler();
        myyHandler = new Handler();

        final Timer mTimer = new Timer();
        final Timer xTimer = new Timer();
        final CountUpTimerTask timerTask = new CountUpTimerTask();
        final XTimerTask xtimertask = new XTimerTask();

        mainLayout = (LinearLayout)findViewById(R.id.mainLayout);///////////////////////

        // 新しいデータ系列の作成(個々のグラフ作成)
        XYSeries series = new XYSeries("X軸");
        XYSeries series2 = new XYSeries("Y軸");
        XYSeries series3 = new XYSeries("Z軸");

        mDataset.addSeries(series);
        mDataset.addSeries(series2);
        mDataset.addSeries(series3);

        mCurrentSeries = series;
        mCurrentSeries2 = series2;
        mCurrentSeries3 = series3;

        // 新しいデータ系列の新規レンダラー作成(グラフ全体)
        renderer = new XYSeriesRenderer();
        renderer2 = new XYSeriesRenderer();
        renderer3 = new XYSeriesRenderer();

        // 各種設定をレンダラーに設定する
        //X軸の値
        renderer.setColor(Color.GREEN);
        renderer.setPointStyle(PointStyle.X);
        renderer.setLineWidth(3);
        renderer.setFillPoints(true);

        //Y軸の値
        renderer2.setColor(Color.YELLOW);
        renderer2.setPointStyle(PointStyle.CIRCLE);
        renderer2.setLineWidth(3);
        renderer2.setFillPoints(true);

        //Z軸の値
        renderer3.setColor(Color.RED);
        renderer3.setPointStyle(PointStyle.TRIANGLE);
        renderer3.setLineWidth(3);
        renderer3.setFillPoints(true);

        //value
        //if(pointview ==1) {
      //  renderer.setDisplayChartValues(true);
      //  renderer.setChartValuesTextSize(25);
        //  renderer.setChartValuesSpacing(20);
        //   renderer.setChartValuesTextAlign(Align.CENTER);
      //  renderer2.setDisplayChartValues(true);
     //   renderer2.setChartValuesTextSize(25);
        //  renderer2.setChartValuesSpacing(20);
        //  renderer2.setChartValuesTextAlign(Align.CENTER);
      //  renderer3.setDisplayChartValues(true);
      //  renderer3.setChartValuesTextSize(25);
        //  renderer3.setChartValuesSpacing(20);
        //  renderer3.setChartValuesTextAlign(Align.CENTER);
        // }
        mRenderer.addSeriesRenderer(renderer);
        mRenderer.addSeriesRenderer(renderer2);
        mRenderer.addSeriesRenderer(renderer3);
       // renderer.setDisplayChartValuesDistance(10);
        mRenderer.setChartTitle("加速度変位");
        mRenderer.setXTitle("秒数");
        mRenderer.setYTitle("加速度[G]");
        mRenderer.setAxisTitleTextSize(16);
        mRenderer.setChartTitleTextSize(20);
        mRenderer.setXLabels(100); // グリット間隔X
        mRenderer.setYLabels(100); // グリット間隔Y
        mRenderer.setLabelsTextSize(15);
        mRenderer.setLegendTextSize(15);

        mRenderer.setXLabelsAlign(Align.CENTER);
        mRenderer.setYLabelsAlign(Align.RIGHT);

        mRenderer.setAxesColor(Color.LTGRAY);
        mRenderer.setLabelsColor(Color.YELLOW);
        mRenderer.setBackgroundColor(Color.BLACK);

        //グリット設定
        mRenderer.setShowGrid(true);
        mRenderer.setGridColor(Color.parseColor("#00FFFF"));
        mRenderer.setXAxisMin(0);//x軸最小値
        mRenderer.setXAxisMax(5); //X最大値
        mRenderer.setYAxisMin(-3);//Y軸最小値
        mRenderer.setYAxisMax(3); //Ｙ最大値
        //凡例表示
        mRenderer.setShowLegend(true);
        //背景
        mRenderer.setMargins(new int[]{30, 30, 15, 40});
         //mRenderer.setPointSize(0);

        mCurrentRenderer = renderer;
        mCurrentRenderer = renderer2;
        mCurrentRenderer = renderer3;


//////////////////////////////////////////////////////////////////////////
        mY0.setText("未取得中");
        mY.setText("未取得中");
        mY2.setText("未取得中");
        mY3.setText("未取得中");


        start.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                currentTime = 0;
                if (mSerial.begin(SERIAL_BAUDRATE)) {
                    mTimer.schedule(timerTask,100,1000);
                    xTimer.schedule(xtimertask, 100, 1000);
                    mainloop();
                    mStop = false;
                    start.setEnabled(false);
                    stop.setEnabled(true);
                }
            }
        });

        stop.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                myHandler.removeCallbacks(timerTask);
                myyHandler.removeCallbacks(xtimertask);
                mStop = true;
                stop.setEnabled(false);
                start.setEnabled(true);
                if( mDataset.getSeries().length > 0) {
                    mDataset.getSeriesAt(0).clear();
                    mDataset.getSeriesAt(1).clear();
                    mDataset.getSeriesAt(2).clear();
                }
            }

        });
    }//onCreate
    //////////////////////////////////////////////////////////////////////////////////////
    //時刻計測
    class CountUpTimerTask extends TimerTask {
        @Override
        public void run() {
            // handlerを使って処理をキューイングする
            myHandler.post(new Runnable() {
                public void run() {
                    currentTime++;
                    //xTime++;
                }
            });
        }
    }

    //時刻計測
    class XTimerTask extends TimerTask {
        @Override
        public void run() {
            // handlerを使って処理をキューイングする
            myyHandler.post(new Runnable() {
                public void run() {
                    xTime++;
                }
            });
        }
    }






    //表示するグラフの設定
        @Override
    protected void onResume() {
        super.onResume();
        if (mChartView == null) {
            LinearLayout layout = (LinearLayout) findViewById(R.id.chart);
            mChartView = ChartFactory.getLineChartView(this, mDataset, mRenderer);
            mRenderer.setClickEnabled(true);
            mRenderer.setSelectableBuffer(10);
            // スクロール
             mRenderer.setPanEnabled(true);
            //  mRenderer.setPanLimits(new double[]{0, 5000, -20, 20});

            //凡例表示
            mRenderer.setShowLegend(true);

            //ズーム許可
            mRenderer.setZoomEnabled(true);
            // mRenderer.setZoomRate(1000);
            // mRenderer.setZoomLimits(new double[]{0, 5000, -20, 20});
            layout.addView(mChartView, new LayoutParams(LayoutParams.FILL_PARENT,
                    LayoutParams.FILL_PARENT));
            boolean enabled = mDataset.getSeriesCount() > 0;
        } else {
            mChartView.repaint();
        }
    }

    ////////////////////////////////////////////////////

    private void mainloop() {
        mRunningMainLoop = true;
        new Thread(mLoop).start();
    }

    private Runnable mLoop = new Runnable() {
        @Override
        public void run() {
            int i, len;

            while (true) {


                for (;;) {
                    byte[] rbuf = new byte[4096]; // 1byte <--slow-- [Transfer Speed] --fast--> 4096 byte
                    len = mSerial.read(rbuf);
                    rbuf[len] = 0;
                    str1 = new String(rbuf);
                    d=0;

                mText1 = str1;

      /*         if(len < 8 && len > 0 ) {
                        lastTime=currentTime;

                        tHandler.post(new Runnable() {
                            public void run() {
                                mY0.setText("生存信号");
                            }

                        });
                        try {
                            Thread.sleep(500);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }else*/

                   // if (len > 72) {
                       if(len > 0){
                        String[] new_str1 = str1.split(";", 0);
                        youso = new_str1.length;


                        //通信中の処理
                       // if (youso >= 16) {
                         if(youso >=1) {
                            flag=0;
                             for (i = 0; i < youso; i++) {
                                 if (str_alive.equals(new_str1[i]) || str_live.equals(new_str1[i])) {
                                     lastTime = currentTime;
                                     flag++;


                                     tHandler.post(new Runnable() {
                                         public void run() {
                                             mY0.setText("生存信号を受信しました");
                                         }

                                     });
                                     try {
                                         Thread.sleep(500);
                                     } catch (Exception e) {
                                         e.printStackTrace();
                                     }

                                 }
                             }
                             if(flag == 1){continue;}
                             do {
                                 for (i = j; i < youso; i++) {
                                     if (str_1.equals(new_str1[i])) {
                                         j =i;
                                         break;
                                     }
                                 }

                                 if ((i + 4) > youso) {
                                     continue;
                                 }
                                 String new_str0a = new_str1[i];
                                 String new_str1a = new_str1[i + 1];
                                 String new_str2a = new_str1[i + 2];
                                 String new_str3a = new_str1[i + 3];
                                 //  String new_str0a = new_str1[11];

                                 //  String new_str0a = new_str1[0];
                                 d = Integer.parseInt(new_str0a);
                                 if (d != 1) { d = 0;}

                                 //  String new_str1a = new_str1[12];
                                 // String new_str1a = new_str1[1];
                                 int a = Integer.parseInt(new_str1a);
                                 double g_str1 = 0, doublecount = a;
                                 g_str1 = doublecount / 100;

                                 // String new_str2a = new_str1[13];
                                 //  String new_str2a = new_str1[2];
                                 int b = Integer.parseInt(new_str2a);
                                 double g_str2 = 0, doublecount2 = b;
                                 g_str2 = doublecount2 / 100;


                                 // String new_str3a = new_str1[14];
                                 // String new_str3a = new_str1[3];
                                 int c = Integer.parseInt(new_str3a);
                                 double g_str3 = 0, doublecount3 = c;
                                 g_str3 = doublecount3 / 100;

                                 for (i = 0; i < len; ++i) {
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
                          //   }while(i+4 <= youso);
                              //      j=0;
                     //    }

                     //   }

                        if(d == 1) {
                            lastTime=currentTime;

                            mHandler.post(new Runnable() {
                                public void run() {

                                     mY0.setText("通常モード");
                                    mY.setText(String.valueOf(youso));
                                     //mY.setText(mText1);
                                     mY2.setText(mText2);
                                     mY3.setText(mText3);

                                    //表示するデータを取得
                                    try {
                                        x = xTime;
                                       // xTime += 0.1;
                                    }catch(NumberFormatException e){
                                        mX.requestFocus();
                                        return;
                                    }
                                    try {
                                        y = Double.parseDouble(mY.getText().toString());
                                        y2 = Double.parseDouble(mY2.getText().toString());
                                        y3 = Double.parseDouble(mY3.getText().toString());
                                    } catch (NumberFormatException e) {
                                        mY.requestFocus();
                                        mY2.requestFocus();
                                        mY3.requestFocus();
                                        return;
                                    }

                                    //表示するデータ
                                    mCurrentSeries.add(x, y);
                                    mCurrentSeries2.add(x, y2);
                                    mCurrentSeries3.add(x, y3);
                                       //グラフを表示
                                   mChartView.repaint();
                                }

                            });

                        }
                                 }while(i+4 <= youso);
                                 j=0;
                            }

                           try {
                               Thread.sleep(150);
                           } catch (Exception e) {
                               e.printStackTrace();
                           }

                  }


                                 //終了処理
                        if (mStop) {
                            mRunningMainLoop = false;
                           finish();

                    }else {//通信してないときの処理
                        if(d != 1) {

                        /*  try {
                                Thread.sleep(100);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }*/

                           if(xTime > 5.0) xTime=0;

                            sHandler.post(new Runnable() {
                               public void run() {
                                 //  pointview=0;
                                  if((currentTime -lastTime) > 30){
                                       mY0.setText("電池が切れた可能性があります");
                                       mY0.setTextColor(Color.RED);
                                       mY.setText("");
                                       mY2.setText("");
                                       mY3.setText("");
                                       try {
                                           Thread.sleep(1000);
                                       } catch (Exception e) {
                                           e.printStackTrace();
                                       }

                                   }

                                   if(xTime == 0.0) {
                                       //mY0.setText("省電力モード");
                                       mY0.setText(String.valueOf(currentTime - lastTime));
                                       // mY.setText("省電力中");
                                       mY.setText(mText1);
                                       mY2.setText("省電力中");
                                       mY3.setText("省電力中");
                                       // mY.setText(mText1);


                                       if (mDataset.getSeries().length > 0) {
                                           mDataset.getSeriesAt(0).clear();
                                           mDataset.getSeriesAt(1).clear();
                                           mDataset.getSeriesAt(2).clear();
                                       }

                                       //表示するデータ
                                       mCurrentSeries.add(0, 0);
                                       mCurrentSeries2.add(0, 0);
                                       mCurrentSeries3.add(0, 0);
                                       //グラフを表示
                                       mChartView.repaint();
                                   }
                                }
                            });
                        }

                    }
                    //終了処理
                    if (mStop) {
                        mRunningMainLoop = false;
                        break;

                    }
                }
                //終了処理
               finish();
            }
        }
    };
}
