package com.example.myapplication;

import android.os.Environment;

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
 * Created by jiayuan on 2016/11/26.
 */
public class HttpClientTask {
    HttpClient httpClient;
    private String mUri_post = "http://130.158.80.39:8080/cgi-bin/form3.py";
    protected void send() {
        httpClient = new DefaultHttpClient();
        HttpPost post = new HttpPost(mUri_post);
        ResponseHandler<String> responseHandler = new BasicResponseHandler();
        MultipartEntity multipartEntity = new MultipartEntity(HttpMultipartMode.BROWSER_COMPATIBLE);
        File sdCardDir = Environment.getExternalStorageDirectory();
        File file = new File(sdCardDir, "yuanyuan.csv");
        FileBody body = new FileBody(file);
        //System.out.println(body.getFilename());
        multipartEntity.addPart("jiayuan", body);
        post.setEntity(multipartEntity);
        try {
            httpClient.execute(post, responseHandler);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
