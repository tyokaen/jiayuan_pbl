package com.example.myapplication;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.media.MediaRecorder;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;

import com.google.android.gms.gcm.GoogleCloudMessaging;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;


public class MainActivity extends Activity {
	/**
	 * Google Cloud Messagingオブジェクト
	 */
	private GoogleCloudMessaging gcm;
	/**
	 * コンテキスト
	 */
	MediaRecorder mediaRecorder=new MediaRecorder();

	private Context context;
	TextView textView, textView1;
	Button b, btn_right, btn_False,btn_jump;
	String string = "";
	HttpClientTask clientTask = new HttpClientTask();
	AlertDialog alertDialog;
    ArrayAdapter<String> arrayAdapter;
	ArrayList<String> arrayList;
	File  sdCardDir= Environment.getExternalStorageDirectory();
	File saveFile=new File(sdCardDir,"List_info.csv");
	int i;
	String result;
	String string1="";
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		context = getApplicationContext();
		gcm = GoogleCloudMessaging.getInstance(this);
		Intent intent = this.getIntent();
			string = intent.getStringExtra("jiayuan");
			string1 = intent.getStringExtra("jiayuan1");
		textView = (TextView) findViewById(R.id.TextView);
		textView1 = (TextView) findViewById(R.id.Tx_result);
		textView1.setText(string);
		result=intent.getStringExtra("zhang");
		btn_right = (Button) findViewById(R.id.Right);
		btn_False = (Button) findViewById(R.id.False);
        btn_jump=(Button)findViewById(R.id.Button1);
		btn_jump.setOnClickListener(new View.OnClickListener() {
				 @Override
				 public void onClick(View view) {
					 Intent intent1=new Intent(MainActivity.this, VideoActivity.class);
					 startActivity(intent1);
				 }
			 });
		btn_right.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				ConfirmInfo();
			}
		});
		btn_False.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				Input();
			}
		});
		registerInBackground();
	}
	public void info() {
		AlertDialog.Builder builder = new AlertDialog.Builder(this);
		builder.setTitle("送信完了");
		builder.setMessage("ご協力ありがとうございます");
		AlertDialog dialog = builder.create();
		dialog.show();
	}
	public void Input() {
		final AlertDialog.Builder builder = new AlertDialog.Builder(this);
		builder.setTitle("分類結果確認");
		LayoutInflater layoutInflater = (LayoutInflater) this.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		final View layout = layoutInflater.inflate(R.layout.mylistview, (ViewGroup) this.findViewById(R.id.LinerLayout1));
		ListView listView = (ListView) layout.findViewById(R.id.ListView1);
		arrayList=new ArrayList<String>();
		try {
			InitData();
		} catch (IOException e) {
			e.printStackTrace();
		}
		ReadData(arrayList);
		arrayAdapter=new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,arrayList);
		listView.setAdapter(arrayAdapter);
		builder.setView(layout);
	    alertDialog = builder.create();
		alertDialog.show();
		WindowManager.LayoutParams params=alertDialog.getWindow().getAttributes();
		params.width=1200;
		params.height=1400;
		alertDialog.getWindow().setAttributes(params);
		listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
				if (i == 0) {
					AlertDialog.Builder builder1 = new AlertDialog.Builder(MainActivity.this);
					builder1.setTitle("正しい振動を入力してください");
					final EditText editText = new EditText(MainActivity.this);
					builder1.setView(editText);
					builder1.setCancelable(false);
					builder1.setNegativeButton("cancel", new DialogInterface.OnClickListener() {
						@Override
						public void onClick(DialogInterface dialogInterface, int i) {
						}
					});
					builder1.setPositiveButton("送信", new DialogInterface.OnClickListener() {
						@Override
						public void onClick(DialogInterface dialogInterface, int i) {
							ConfirmInfo2(editText.getText().toString());
							try {
								WriteData(editText.getText().toString());
							} catch (IOException e) {
								e.printStackTrace();
							}
						}
					});
					AlertDialog dialog = builder1.create();
					dialog.show();
					alertDialog.dismiss();
				} else {
						if(i==1) {
							ConfirmInfo1("door open",arrayList.get(i));
						}
					else if(i==2){
							ConfirmInfo1("wind",arrayList.get(i));
						}
						else if(i==3){
							ConfirmInfo1("mail box",arrayList.get(i));
						}
					else if(i==4){
							ConfirmInfo1("i do not know",arrayList.get(i));
						}
						else if(i==5){
							ConfirmInfo1("earthquake",arrayList.get(i));
						}
                   alertDialog.dismiss();
				}
			}
		});

	}
	public void saveToSDCard1(String filename, String ss) throws Exception {
		File file = new File(Environment.getExternalStorageDirectory(), filename);
		FileOutputStream out = new FileOutputStream(file, false);
		out.write(ss.getBytes());
		out.close();
	}
	private void registerInBackground() {
		new AsyncTask<Void, Void, String>() {
			@Override
			protected String doInBackground(Void... params) {
				String msg = "";
				try {
					if (gcm == null) {
						gcm = GoogleCloudMessaging.getInstance(context);
					}
					String project_number = "543507889670";
					String regid = gcm.register(project_number);
					msg = "Device registered, registration ID=" + regid;
				} catch (IOException ex) {
					msg = "Error :" + ex.getMessage();
				}
				Log.d("regiid", "regiid: " + msg);
				return msg;
			}

			@Override
			protected void onPostExecute(String msg) {
			}
		}.execute(null, null, null);
	}
   public void InitData() throws IOException {
	String filepath=saveFile.getAbsolutePath();
	   FileWriter fileWriter=new FileWriter(filepath,true);
	   if(saveFile.length()==0){
		   fileWriter.write("下記以外");
		   fileWriter.write("\r\n");
		  fileWriter.write("扉が開閉");
		   fileWriter.write("\r\n");
		   fileWriter.write("風");
		   fileWriter.write("\r\n");
		   fileWriter.write("ポスト投函");
		   fileWriter.write("\r\n");
		   fileWriter.write("わかりません");
		   fileWriter.write("\r\n");
		   fileWriter.flush();
		   fileWriter.close();
	   }
   }
	public void WriteData(String message)throws IOException{
	  String filepath=saveFile.getAbsolutePath();
		FileWriter fileWriter=new FileWriter(filepath,true);
		fileWriter.write(message);
		fileWriter.write("\r\n");
		fileWriter.flush();
		fileWriter.close();
	}
    public void ReadData( ArrayList<String> arrayList){
		BufferedReader bufferedReader=null;
		String filepath=saveFile.getAbsolutePath();
		try {
			 bufferedReader=new BufferedReader(new FileReader(filepath));
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		String string=null;
		try {
			while((string=bufferedReader.readLine())!=null){
                arrayList.add(string);
            }
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public void ConfirmInfo(){
		AlertDialog.Builder builder=new AlertDialog.Builder(this);
		builder.setTitle("確認");
		builder.setMessage("「"+ string+  "」"+"を送信しますか?");
		builder.setCancelable(false);
		builder.setNegativeButton("キャンセル", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialogInterface, int i) {
			}
		});
		builder.setPositiveButton("送信", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialogInterface, int i) {
				textView1.setText("無し");
				try {
					SimpleDateFormat df = new SimpleDateFormat("yyyy:MM:dd:HH:mm:ss");
					String date=df.format(new Date());
					saveToSDCard1("yuanyuan.csv", "True" + "//" + string1+"//"+result+"//"+date);
				} catch (Exception e) {
					e.printStackTrace();
				}
				new Thread(new Runnable() {
					@Override
					public void run() {
						clientTask.send();
					}
				}).start();
				info();
			}
		});
		   AlertDialog alertDialog=builder.create();
		   alertDialog.show();
	}
	public void ConfirmInfo1(final String info, final String ListInfo){
		AlertDialog.Builder builder=new AlertDialog.Builder(this);
		builder.setTitle("確認");
		builder.setMessage("「"+ ListInfo+  "」"+"を送信しますか?");
		builder.setNegativeButton("キャンセル", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialogInterface, int i) {
			}
		});
		builder.setPositiveButton("送信", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialogInterface, int i) {
				textView1.setText("無し");
				try {
					SimpleDateFormat df = new SimpleDateFormat("yyyy:MM:dd:HH:mm:ss");
					String date=df.format(new Date());
					saveToSDCard1("yuanyuan.csv", info + "//" + string1+"//"+result+"//"+date);
				} catch (Exception e) {
					e.printStackTrace();
				}
				new Thread(new Runnable() {
					@Override
					public void run() {
						clientTask.send();
					}
				}).start();
				info();
			}
		});
		AlertDialog alertDialog=builder.create();
		alertDialog.show();
	}
	public void ConfirmInfo2(final String info){
		AlertDialog.Builder builder=new AlertDialog.Builder(this);
		builder.setTitle("確認");
		builder.setMessage("「"+ info+  "」"+"を送信しますか?");
		builder.setNegativeButton("キャンセル", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialogInterface, int i) {
			}
		});
		builder.setPositiveButton("送信", new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialogInterface, int i) {
				textView1.setText("無し");
				try {
					SimpleDateFormat df = new SimpleDateFormat("yyyy:MM:dd:HH:mm:ss");
					String date=df.format(new Date());
					saveToSDCard1("yuanyuan.csv", info + "//" + string1+"//"+result+"//"+date);
				} catch (Exception e) {
					e.printStackTrace();
				}
				new Thread(new Runnable() {
					@Override
					public void run() {
						clientTask.send();
					}
				}).start();
				info();
			}
		});
		AlertDialog alertDialog=builder.create();
		alertDialog.show();
	}
}