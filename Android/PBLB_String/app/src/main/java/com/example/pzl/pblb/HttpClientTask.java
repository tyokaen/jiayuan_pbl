package com.example.pzl.pblb;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Environment;
import android.widget.TextView;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by jiayuan on 2016/10/26.
 */
public class HttpClientTask extends AsyncTask<Void,Void,String> {
    private TextView mTextView;
    private Activity mParentActivity;
    private ProgressDialog mDialog = null;
    HttpClient httpClient;
    private String mUri = "http://130.158.80.39:8080/cgi-bin/form2.py";

    public HttpClientTask( TextView textView){
        this.mTextView = textView;
    }

    protected void onPreExecute(){}
    protected String doInBackground(Void...arg0){
        String a = "";
        try {
            Thread.sleep(5000);
            send();
            a = exec_get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        return a;
    }
    @Override
    protected void onPostExecute(String a){
        this.mTextView.setText(a);
    }
    protected void send(){
        httpClient=new DefaultHttpClient();
        HttpPost post=new HttpPost(mUri);
        SimpleDateFormat df = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss");
        String namenew = df.format(new Date())+".csv";
        // try {
        //  post.setURI(new URI(mUri));
        // } catch (URISyntaxException e) {
        //    e.printStackTrace();
        // }
        ResponseHandler<String> responseHandler=new BasicResponseHandler();
        MultipartEntity multipartEntity=new MultipartEntity(HttpMultipartMode.BROWSER_COMPATIBLE);
        File sdCardDir = Environment.getExternalStorageDirectory();
        File file=new File(sdCardDir,"pbl_orange.csv");
        File file1 = new File(sdCardDir,namenew);
        file.renameTo(file1);
        FileBody body=new FileBody(file1);
        //System.out.println(body.getFilename());
        multipartEntity.addPart("jiayuan", body);
        post.setEntity(multipartEntity);
        try {
            httpClient.execute(post,responseHandler);
        } catch (IOException e) {
            e.printStackTrace();
        }
        if (file.exists()){
            if(file.isFile()){
                file.delete();
            }
        }
        if (file1.exists()){
            if(file1.isFile()){
                file1.delete();
            }
        }

    }
    protected void send1(){
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
    }
}
