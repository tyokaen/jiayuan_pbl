package com.example.myapplication;

import android.app.Activity;
import android.content.Context;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import com.google.android.gms.gcm.GoogleCloudMessaging;

import java.io.IOException;


public class MainActivity extends Activity {
	/** Google Cloud Messagingオブジェクト */
	private GoogleCloudMessaging gcm;
	/** コンテキスト */
	private Context context;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		context = getApplicationContext();

		gcm = GoogleCloudMessaging.getInstance(this);
		//registerInBackground();
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
}