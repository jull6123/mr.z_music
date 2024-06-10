<template>
  <div>
    <el-row style="margin-top: 10px; font-size: 18px; color:black;">
      <span style="margin-left: 80px;">歌曲</span>
      <span style="margin-left: 950px;">歌手</span>
      <span style="margin-left: 180px;">时长</span>
    </el-row>
        <li class="musiclist" style="margin-top: 10px;"></li>
        <li v-for="obj in Music" :key="obj.Id" class="musiclist">
          <el-button style="width: 1300px;background: rgba(0,0,0,0);height: 60px;cursor: default;" text @dblclick="PlayMusic(obj.Id)">
           <span style="left:90px;position:fixed;color:black;font-size: 16px; opacity: 100%;">{{ obj.MusicName }}</span>
           <span style="left: 1070px;position:fixed; color:black;font-size: 16px;opacity: 100%;">{{ obj.Singer }}</span>
           <span style="left: 1290px;position:fixed; color:black;font-size: 16px;opacity: 100%;">{{ obj.Time }}</span>
          </el-button>
        </li>
  </div>
  <div>
    <el-button text style="position: fixed;left: 150px; bottom: 40px;width: 50px;background: rgba(0,0,0,0);" size="default" @click="NextMusic">
      <el-icon style="width: 100px;font-size: 30px;"><ArrowRight /></el-icon>
    </el-button>
    <el-button text style="position: fixed;left: 80px; bottom: 40px;width: 50px;background: rgba(0,0,0,0);" size="default" @click="PreviousMusic">
      <el-icon style="width: 100px;font-size: 30px;"><ArrowLeft /></el-icon>
    </el-button>
    <el-button text style="position: fixed;left: 10px;bottom: 40px;width: 50px;background: rgba(0,0,0,0);" @click="ChangeMode">
      <span v-if="this.isRepeat">单曲循环</span>
      <span v-else>顺序播放</span>
    </el-button>
  </div>
  <div class="audiocontrol" style="position: fixed;">
   <audio controls :src="MusicUrl" autoplay="true" style="width: 1100px;" ref="audioPlayer" @ended="PlayModel">
   </audio>
  </div>
</template> 


<script>

  export default{
     data(){
      return{
        currentSrc:'',
        MusicUrl:'',
        Playmode:'repeat',
        isRepeat:true,
        Musiclength:3,
        Music:[
          {
            Id:0,
            MusicName:"谁",
            Singer:"廖俊涛",
            Time:"4:14",
            src:'/public/music/shei_liaojt_414.mp3'
          },
          {
            Id:1,
            MusicName:"消愁",
            Singer:"毛不易",
            Time:"4:21",
            src:"/public/music/xiaochou_maoby_421.mp3"
          },
          {
            Id:2,
            MusicName:"保留",
            Singer:"郭顶",
            Time:"4:30",
            src:"/public/music/baoliu_guod_430.mp3"
          },
          {
            Id:3,
            MusicName:"像我这样的人",
            Singer:"毛不易",
            Time:"3:27",
            src:"/public/music/xwzydr_maoby_327.mp3"
          }
        ]
      }
     },
     methods:{
      PlayMusic(id){
        console.log('id:' + id);
        this.$currentIndex = id;
        this.MusicUrl = this.Music[this.$currentIndex].src;
        this.$setMusicUrl(this.MusicUrl);
        this.$refs.audioPlayer.play();
      },
      ChangeMode()
      {
        if(this.Playmode=='repeat')
        {
        this.Playmode = 'loop'
        this.isRepeat=false
        }
        else
        {
        this.Playmode = 'repeat'
        this.isRepeat=true
        }
      },
      PlayModel(){
       if(this.Playmode=='repeat')
       {
       this.$refs.audioPlayer.currentTime = 0; // 将播放位置重置为0  
       this.$refs.audioPlayer.play(); // 重新播放歌曲
       }
       if(this.Playmode=='loop')
       {
        this.NextMusic();
       }
      },
      NextMusic(){
        if(this.$currentIndex<=this.Musiclength){
        this.$currentIndex++;
        }
        if(this.$currentIndex==this.Musiclength+1)
        {
          this.$currentIndex=0;
        }
        this.MusicUrl = this.Music[this.$currentIndex].src;
        this.$refs.audioPlayer.play();
      },
      PreviousMusic(){
        if(this.$currentIndex==0)
        this.$currentIndex=2;
        else
        this.$currentIndex--;

        this.MusicUrl = this.Music[this.$currentIndex].src;
        this.$refs.audioPlayer.play();
      }
  }
}
</script>

<style>

.line {
  width: 70%;
}
.line div {
  width: 100%;
  height: 0;
  border-top: 1px solid var(--el-border-color);
}
.musiclist{
  margin-bottom: 0px;
  margin-top: 0px;
  border-bottom: 1px solid #0f1e40;
  margin-left: 70px;
  width: 1250px;
  list-style: none;
  opacity: 70%;
}
.audiocontrol{
  bottom: 30px;
  left: 230px;
}
</style>
