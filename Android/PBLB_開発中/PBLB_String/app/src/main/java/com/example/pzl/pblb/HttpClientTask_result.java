package com.example.pzl.pblb;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Environment;
import android.widget.TextView;

import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.File;
import java.io.IOException;

/**
 * Created by jiayuan on 2016/10/26.
 */
public class HttpClientTask_result extends AsyncTask<Void,Void,String> {
    private TextView mTextView;
    private Activity mParentActivity;
    private ProgressDialog mDialog = null;
    HttpClient httpClient;
    private String mUri = "http://130.158.80.39:8080/cgi-bin/form2.py";

    protected void onPreExecute(){}
    protected String doInBackground(Void...arg0){
        send();
        return null;
    }
    @Override
    protected void onPostExecute(String a){
        //this.mTextView.setText(a);
    }

    protected void send(){
        httpClient=new DefaultHttpClient();
        HttpPost post=new HttpPost(mUri);

        // try {
        //  post.setURI(new URI(mUri));
        // } catch (URISyntaxException e) {
        //    e.printStackTrace();
        // }
        ResponseHandler<String> responseHandler=new BasicResponseHandler();
        MultipartEntity multipartEntity=new MultipartEntity(HttpMultipartMode.BROWSER_COMPATIBLE);
        File sdCardDir = Environment.getExternalStorageDirectory();
        File file=new File(sdCardDir,"zhang.csv");
        FileBody body=new FileBody(file);
        //System.out.println(body.getFilename());
        multipartEntity.addPart("jiayuan", body);
        post.setEntity(multipartEntity);
        try {
            httpClient.execute(post,responseHandler);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
