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
public class HttpClientTask extends AsyncTask<Void,Void,String> {
    private TextView mTextView;
    private Activity mParentActivity;
    private ProgressDialog mDialog = null;
    HttpClient httpClient;
    private String mUri = "http://130.158.80.39:8080/cgi-bin/form.py";
/*
    public HttpClientTask( TextView textView){
        this.mTextView = textView;
    }
*/
    protected void onPreExecute(){}
    protected String doInBackground(Void...arg0){
        try {
            Thread.sleep(5000);
            send();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        return null;
    }
    @Override
    protected void onPostExecute(String string){
        //this.mTextView.setText(string);
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
        File file=new File(sdCardDir,"pbl_orange.csv");
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
    /*
    private String exec_get() {
        BufferedReader in=null;
        String src ="";
        try {
            HttpGet get=new HttpGet();
            get.setURI(new URI(mUri));
            HttpResponse response = httpClient.execute(get);
            in=new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
            StringBuffer stringBuffer=new StringBuffer();
            String line="";
            while((line=in.readLine())!=null){
                stringBuffer.append(line);
            }
            src=stringBuffer.toString();
        }catch(Exception e){
            e.printStackTrace();
        }finally {
            try{
                if (in!=null){
                    in.close();
                }
            }catch (Exception ignored){
            }
        }
        return src;
    }*/
}
