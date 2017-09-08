package test.com.robot.tuling.aiuilibrary;

import android.app.Service;
import android.content.Intent;
import android.content.res.AssetManager;
import android.os.IBinder;
import android.util.Log;

import com.iflytek.aiui.AIUIAgent;
import com.iflytek.aiui.AIUIConstant;
import com.iflytek.aiui.AIUIEvent;
import com.iflytek.aiui.AIUIListener;
import com.iflytek.aiui.AIUIMessage;

import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AsrService extends Service {
    private final String TAG = "tag";
    private AIUIAgent mAIUIAgent = null;
    private int mAIUIState = AIUIConstant.STATE_IDLE;

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.e(TAG, "onStartCommand: ");
        startRecognize();
        updateLexicon();
        return super.onStartCommand(intent, flags, startId);
    }

    private void startRecognize() {
        if (checkAIUIAgent()) {
            startVoiceNlp();
        }
    }

    private boolean checkAIUIAgent() {
        if (null == mAIUIAgent) {
            Log.i(TAG, "create aiui agent");
            mAIUIAgent = AIUIAgent.createAgent(this, getAIUIParams(), mAIUIListener);
            AIUIMessage startMsg = new AIUIMessage(AIUIConstant.CMD_START, 0, 0, null, null);
            mAIUIAgent.sendMessage(startMsg);
        }

        if (null == mAIUIAgent) {
            final String strErrorTip = "创建 AIUI Agent 失败！";
            showTip(strErrorTip);
            Log.e(TAG, "checkAIUIAgent: " + strErrorTip);
        }

        return null != mAIUIAgent;
    }

    private void startVoiceNlp() {
        Log.i(TAG, "start voice nlp");
        //mNlpText.setText("");

        // 先发送唤醒消息，改变AIUI内部状态，只有唤醒状态才能接收语音输入
        if (AIUIConstant.STATE_WORKING != this.mAIUIState) {
            AIUIMessage wakeupMsg = new AIUIMessage(AIUIConstant.CMD_WAKEUP, 0, 0, "", null);
            mAIUIAgent.sendMessage(wakeupMsg);
        }

        // 打开AIUI内部录音机，开始录音
        String params = "sample_rate=16000,data_type=audio";
        AIUIMessage writeMsg = new AIUIMessage(AIUIConstant.CMD_START_RECORD, 0, 0, params, null);
        mAIUIAgent.sendMessage(writeMsg);
    }


    public void updateLexicon() {
        String params = null;
        String contents = FucUtil.readFile(this, "userwords", "utf-8");
        try {
            JSONObject joAiuiLexicon = new JSONObject();
            joAiuiLexicon.put("name", "userword");
            joAiuiLexicon.put("content", contents);
            params = joAiuiLexicon.toString();
        } catch (Throwable e) {
            e.printStackTrace();
            showTip(e.getLocalizedMessage());
        }//end of try-catch

        Log.e(TAG, "updateLexicon: " + contents);
        AIUIMessage msg = new AIUIMessage(AIUIConstant.CMD_UPLOAD_LEXICON, 0, 0, params, null);
        mAIUIAgent.sendMessage(msg);
    }

    private String getAIUIParams() {
        String params = "";

        AssetManager assetManager = getResources().getAssets();
        try {
            InputStream ins = assetManager.open("cfg/aiui_phone.cfg");
            byte[] buffer = new byte[ins.available()];

            ins.read(buffer);
            ins.close();

            params = new String(buffer);
        } catch (IOException e) {
            e.printStackTrace();
        }

        return params;
    }

    private AIUIListener mAIUIListener = new AIUIListener() {

        @Override
        public void onEvent(AIUIEvent event) {
            if (event.eventType == AIUIConstant.EVENT_WAKEUP) {
                Log.i(TAG, "on event: " + event.eventType);
                showTip("进入识别状态");

            } else if (event.eventType == AIUIConstant.EVENT_RESULT) {
                Log.i(TAG, "on event: " + event.eventType);
                try {
                    JSONObject bizParamJson = new JSONObject(event.info);
                    JSONObject data = bizParamJson.getJSONArray("data").getJSONObject(0);
                    JSONObject params = data.getJSONObject("params");
                    JSONObject content = data.getJSONArray("content").getJSONObject(0);

                    if (content.has("cnt_id")) {
                        String cnt_id = content.getString("cnt_id");
                        JSONObject cntJson = new JSONObject(new String(event.data.getByteArray(cnt_id), "utf-8"));
                        Log.e(TAG, "onEvent: " + cntJson.toString());
                        String sub = params.optString("sub");
                        if ("nlp".equals(sub)) {
                            // 解析得到语义结果
                            //String resultStr = cntJson.optString("intent");
                            handleResult(cntJson);
                            //Log.e(TAG,"result :"+ resultStr);
                        }
                    }
                } catch (Throwable e) {
                    e.printStackTrace();
                    Log.e(TAG, "onEvent: " + e.getLocalizedMessage());
                }

            } else if (event.eventType == AIUIConstant.EVENT_ERROR) {
                Log.i(TAG, "on event: " + event.eventType);
                Log.e(TAG, "错误: " + event.arg1 + "\n" + event.info);

            } else if (event.eventType == AIUIConstant.EVENT_VAD) {
                if (AIUIConstant.VAD_BOS == event.arg1) {
                    showTip("找到vad_bos");
                } else if (AIUIConstant.VAD_EOS == event.arg1) {
                    showTip("找到vad_eos");
                } else {
                    showTip("声音大小:" + event.arg2);
                }

            } else if (event.eventType == AIUIConstant.EVENT_START_RECORD) {
                Log.i(TAG, "on event: " + event.eventType);
                showTip("开始录音");

            } else if (event.eventType == AIUIConstant.EVENT_STOP_RECORD) {
                Log.i(TAG, "on event: " + event.eventType);
                showTip("停止录音");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                startRecognize();

            } else if (event.eventType == AIUIConstant.EVENT_STATE) {
                mAIUIState = event.arg1;
                if (AIUIConstant.STATE_IDLE == mAIUIState) {
                    // 闲置状态，AIUI未开启
                    showTip("STATE_IDLE");
                } else if (AIUIConstant.STATE_READY == mAIUIState) {
                    // AIUI已就绪，等待唤醒
                    showTip("STATE_READY");
                } else if (AIUIConstant.STATE_WORKING == mAIUIState) {
                    // AIUI工作中，可进行交互
                    showTip("STATE_WORKING");
                }
            } else if (event.eventType == AIUIConstant.EVENT_CMD_RETURN) {
                if (AIUIConstant.CMD_UPLOAD_LEXICON == event.arg1) {
                    showTip("上传" + (0 == event.arg2 ? "成功" : "失败"));
                }

            } else {
            }
        }

    };

    private void handleResult(JSONObject jsonObject) {
        try {
            JSONObject object = null;
            if (jsonObject != null) {
                if (jsonObject.has("intent")) {
                    object = jsonObject.getJSONObject("intent");
                    if (jsonObject.has("data")) {
                        if (jsonObject.has("result")) {
                            object = jsonObject.getJSONArray("result").getJSONObject(0);
                            String url = object.getString("url");
                            Log.e(TAG, "url: " + url);
                        }
                    }
                }

                String reg = "http://[audio|mp3][\\s]*[\\S]{1,188}.mp3";
                Pattern pattern = Pattern.compile(reg);
                String content = jsonObject.optString("intent").replace("\\", "");
                Matcher mat = pattern.matcher(content);
                boolean success = mat.find();
                List<String> mp3urls = new ArrayList<>();
                while(mat.find()){
                    String url = mat.group().replace("\\", "").replace("\"url\":\"", "");
                    mp3urls.add(url);
                }
                for (String mp3url : mp3urls) {
                    Log.e(TAG, "url : " + mp3url);
                }
                if (object != null) {
                    String text = object.getString("text");
                    JSONObject answerJson = object.getJSONObject("answer");
                    String answer = answerJson.getString("text");
                    Log.e(TAG, "query: " + text);
                    Log.e(TAG, "answer: " + answer);
//                    if (!TextUtils.isEmpty(mp3url)) {
//                        Mp3Player.getInstance().play(mp3url);
//                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "handleResult Exception: "+e.getMessage() );
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Mp3Player.getInstance().destory();
        if (null != this.mAIUIAgent) {
            AIUIMessage stopMsg = new AIUIMessage(AIUIConstant.CMD_STOP, 0, 0, null, null);
            mAIUIAgent.sendMessage(stopMsg);
            this.mAIUIAgent.destroy();
            this.mAIUIAgent = null;
        }
    }

    private void showTip(final String str) {
        Log.e(TAG, "showTip: " + str);
//        runOnUiThread(new Runnable() {
//
//            @Override
//            public void run() {
//                mToast.setText(str);
//                mToast.show();
//            }
//        });
    }

}