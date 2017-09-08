package test.com.robot.tuling.aiuilibrary;

import android.media.MediaPlayer;
import android.util.Log;

/**
 * Created by yzf_f on 2017/9/8.
 */

public final class Mp3Player {
    private final String TAG = "tag";
    private static Mp3Player mp3Player;
    private MediaPlayer mediaPlayer;

    private Mp3Player() {
    }

    public static Mp3Player getInstance() {
        if (null == mp3Player) {
            synchronized (Mp3Player.class) {
                if (null == mp3Player) {
                    mp3Player = new Mp3Player();
                }
            }
        }
        return mp3Player;
    }

    public void play(String url) {
        try {
            if (mediaPlayer!=null){
                mediaPlayer.stop();
            }else {
                mediaPlayer = new MediaPlayer();
            }
            mediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                @Override
                public void onCompletion(MediaPlayer mp) {
                    if (mediaPlayer != null) {
                        mediaPlayer.release();
                        mediaPlayer = null;
                    }
                }
            });
            mediaPlayer.setDataSource(url);
            mediaPlayer.prepare();
            mediaPlayer.start();
        } catch (Exception e) {
            Log.e(TAG, "play:" + e.getMessage());
        }
    }

    public void replay() {
        mediaPlayer.reset();
        mediaPlayer.start();
    }

    public void stop() {
        mediaPlayer.stop();
        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }

    public void resume() {
        mediaPlayer.start();
    }

    public void pause(){
        mediaPlayer.pause();
    }

    public void destory(){
        if (mediaPlayer != null) {
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
    }
}
