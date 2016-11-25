package com.example.myapplication;

import android.app.IntentService;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.NotificationCompat;
import android.util.Log;
import com.google.android.gms.gcm.GoogleCloudMessaging;

public class GcmIntentService extends IntentService {
	public static final int NOTIFICATION_ID = 1;
	private static final String TAG = "GcmIntentService";
	public GcmIntentService() {
		super("GcmIntentService");
	}
	@Override
	protected void onHandleIntent(Intent intent) {
		Bundle extras = intent.getExtras();
		GoogleCloudMessaging gcm = GoogleCloudMessaging.getInstance(this);
		String messageType = gcm.getMessageType(intent);

		if (!extras.isEmpty()) {
			if (GoogleCloudMessaging.MESSAGE_TYPE_SEND_ERROR.equals(messageType)) {
				Log.d(TAG, "messageType: " + messageType + ",body:" + extras.toString());
			} else if (GoogleCloudMessaging.MESSAGE_TYPE_DELETED.equals(messageType)) {
				Log.d(TAG,"messageType: " + messageType + ",body:" + extras.toString());
			} else if (GoogleCloudMessaging.MESSAGE_TYPE_MESSAGE.equals(messageType)) {
				Log.d(TAG,"messageType: " + messageType + ",body:" + extras.toString());
				final String message = extras.getString("message");
				sendNotification(message);
			}
		}
		GcmBroadcastReceiver.completeWakefulIntent(intent);
	}

	private void sendNotification(String msg) {
		final NotificationManager notificationManager = (NotificationManager)
				this.getSystemService(Context.NOTIFICATION_SERVICE);

		final PendingIntent contentIntent = PendingIntent.getActivity(this, 0,
				new Intent(this, MainActivity.class), 0);

		final Uri uri= RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

		final NotificationCompat.Builder builder = new NotificationCompat.Builder(this);
		builder.setContentTitle(getString(R.string.app_name));
		builder.setSmallIcon(R.mipmap.ic_launcher);
		builder.setStyle(new NotificationCompat.BigTextStyle().bigText(msg));
		builder.setContentText(msg);
		builder.setWhen(System.currentTimeMillis());
		builder.setSound(uri);

		// タップで通知領域から削除する
		builder.setAutoCancel(true);

		builder.setContentIntent(contentIntent);
		notificationManager.notify(NOTIFICATION_ID, builder.build());
	}
}