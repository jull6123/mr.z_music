
<template>
  <el-container>
    <el-header>
      <el-row class="grid-content bg-purple-light" :gutter="20">
        <el-col :span="3"></el-col>
        <el-col :span="2" style="text-align: center" class="grid-content bg-purple-dark"><div style="margin-top: 12px">音你心动</div></el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='songMusic' && 'grid-content bg-purple']">
          <div  type="text" @click="songMusicB" style="margin-top: 12px">正在播放</div>
        </el-col>
        <el-col :span="1" style="text-align: center"
                :class="[getType==='recommend' && 'grid-content bg-purple']">
          <div type="text" @click="recommendB" style="margin-top: 12px"> 推 荐 </div>
        </el-col>
        <el-col :span="1" style="text-align: center"
                :class="[getType==='search' && 'grid-content bg-purple']">
          <div type="text" @click="searchB" style="margin-top: 12px">搜 索</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='songList' && 'grid-content bg-purple']">
          <div type="text" @click="songListB" style="margin-top: 12px">我的歌单</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='listened' && 'grid-content bg-purple']">
          <div type="text" @click="listenedB" style="margin-top: 12px">我听过的</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='ai' && 'grid-content bg-purple']">
          <div type="text" @click="aiB" style="margin-top: 12px">AI生成</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='upload' && 'grid-content bg-purple']">
          <div type="text" @click="$router.push({path: '/uploadPost', query: {uploadMold: 'music'}})" style="margin-top: 12px">上传歌曲</div>
        </el-col>
        <el-col :span="3"></el-col>
        <el-col :span="1" style="text-align: center">
          <el-dropdown trigger="click">
            <h3 class="el-dropdown-link mx-1" size="large" type="text" style="margin-top: 12px">{{ user.username }}</h3>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push({path: '/person', query: {uid: user.id}})" >个人信息</el-dropdown-item>
                <el-dropdown-item @click="$router.push('/')"> 退 出 </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-col>
        <el-col :span="3"></el-col>
      </el-row>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="3"></el-col>
        <el-col :span="18" class="grid-contents bg-purple-light">
          <div>
            <div style="margin: 10px 0" v-if="getType==='home'">
              <!--              搜索框-->
              <el-card class="box-card" :style="{ height: '600px' }">
                <h1>home 介绍</h1>
              </el-card>
            </div>

            <!--        搜索        -->
            <div style="margin: 10px 0" v-if="getType==='search'">
<!--              搜索框-->
              <el-card class="box-card" :style="{ height: '80px' }">
                <span >热门歌曲：</span>
                <span style="margin-left: 5px" v-for="(value, key) in hotMusic" :key="key" class="text item">
                  <span style="margin-left: 5px" v-for="(val, keys) in value" :key="keys" class="text item">
                    <template v-if="keys === 'name'" @click="handleMusicNameClick(value.id)">
                      {{ val }}
                    </template>
                </span>
                </span>

                <el-input style="width: 200px" placeholder="请输入" suffix-icon="el-icon-message" class="ml-5"
                          v-model="searchData.serName" input-style="margin-left: 5px"></el-input>
                <el-button class="ml-5" type="primary" @click="search">搜索</el-button>
                <el-button type="warning" @click="reset">重置</el-button>
              </el-card>
<!--              已上传的全部音乐-->
              <el-table :data="musicListAll" border stripe :header-cell-class-name="'headerBg'"
                  style="margin-top: 30px">
                <el-table-column prop="name" label="歌曲名" width="140"></el-table-column>
                <el-table-column prop="singer" label="歌手"></el-table-column>
                <el-table-column prop="support" label="点赞数"></el-table-column>
                <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                <el-table-column label="操作" width="500" align="center">
                  <template #default="scope">
                    <el-button type="primary" @click="display(scope.row)"> 播 放 </el-button>
                    <el-button type="primary" @click="like(scope.row,'music')"> 点 赞 </el-button>
                    <el-button type="success" @click="comment(scope.row)"> 评 论 </el-button>
                    <el-button type="success" @click="add(scope.row)"> 添加至 我的歌单 </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>

<!--            推荐界面-->
            <div style="margin: 10px 0" v-if="getType==='recommend'">
              <!--              歌曲榜单推荐-->
              <el-card class="box-card" :style="{ height: '200px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">歌曲榜单</h1>
                </div>
                <div class="photo-container">
                  <el-card class="photo-card" v-for="(photo, index) in photos" :key="index">
                    <img :src="photo.url" alt="photo" @click="goToDetail(photo.id)" class="photo-img">
                  </el-card>
                </div>
              </el-card>
              <!--              歌单榜单-->
              <el-card class="box-card" style="height:600px;">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">歌单榜单</h1>
                </div>
                <el-table :data="songListHot" border stripe :header-cell-class-name="'headerBg'">
                  <el-table-column prop="name" label="名称" width="140"></el-table-column>
                  <el-table-column prop="userName" label="所属者"></el-table-column>
                  <el-table-column prop="number" label="歌曲数量"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button type="primary" @click="getSongMusic(scope.row)"> 播放并查看 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </div>

            <!--        正在播放        -->
            <div style="margin: 10px 0" v-if="getType==='songMusic'">
<!--              歌单信息-->
              <el-card class="box-card" >
                <div slot="header" class="clearfix">
                  <h3 style="text-align: center">{{ songListNow.name }}</h3>
                </div>
                <div v-for="(value, key) in songListNow" :key="key" class="text item">
                  <template v-if="key !== 'id' && key !== 'avatar' && key !== 'uid'">
                    {{ customKeys[key] }}:{{ value }}
                  </template>
                </div>
                <div style="padding-top: 30px;">
                  <el-button type="primary" @click="like(songListNow,'songList')"> 点 赞 </el-button>
                  <el-button type="primary" @click="collect(songListNow)"> 收 藏 </el-button>
                </div>
              </el-card>
<!--              歌单的歌曲列表-->
              <el-table :data="songMusicList" border stripe :header-cell-class-name="'headerBg'"
                        style="margin-top: 30px">
                <el-table-column prop="name" label="歌曲名" width="140"></el-table-column>
                <el-table-column prop="si nger" label="歌手"></el-table-column>
                <el-table-column prop="support" label="点赞数"></el-table-column>
                <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                <el-table-column label="操作" width="500" align="center">
                  <template #default="scope">
                    <el-button type="primary" @click="display(scope.row)"> 播 放 </el-button>
                    <el-button type="primary" @click="like(scope.row, 'music')"> 点 赞 </el-button>
                    <el-button type="success" @click="comment(scope.row)"> 评 论 </el-button>
                    <el-button type="success" @click="add(scope.row)"> 添加至 我的歌单 </el-button>
                    <el-button type="success" v-if="user.id === songListNow.uid && songListNow.is_upload === 0" @click="delMusic(scope.row)"> 删 除 </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>

<!--            我的歌单-->
            <div style="margin: 10px 0" v-if="getType==='songList'">
              <el-card class="box-card" :style="{ height: '80px' }">
                <el-input style="width: 200px" placeholder="请输入歌单名" suffix-icon="el-icon-message" class="ml-5"
                          v-model="searchData.serSName" input-style="margin-left: 5px"></el-input>
                <el-button class="ml-5" type="primary" @click="search">搜索</el-button>
                <el-button type="warning" @click="reset">重置</el-button>
              </el-card>
              <!--              我的歌单-->
              <el-card class="box-card" :style="{ height: '400px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">我的歌单</h1>
                </div>
                <el-table :data="songListMine" border stripe :header-cell-class-name="'headerBg'">
                  <el-table-column prop="name" label="名称" width="140"></el-table-column>
                  <el-table-column prop="number" label="歌曲数量"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="is_upload_msg" label="上传阶段"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button type="primary" @click="getSongMusic(scope.row)"> 播放并查看 </el-button>
                      <el-button type="primary" @click="updateSongList(scope.row)"> 修 改 </el-button>
                      <el-button type="primary" v-if="scope.row.is_upload === 0" @click="uploadSongList(scope.row)"> 上 传 </el-button>
                      <el-button type="primary" @click="delSongList(scope.row)"> 删 除 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
              <!--              收藏歌单-->
              <el-card class="box-card" :style="{ height: '400px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">收藏歌单</h1>
                </div>
                <el-table :data="songListCollect" border stripe :header-cell-class-name="'headerBg'">
                  <el-table-column prop="name" label="名称" width="140"></el-table-column>
                  <el-table-column prop="userName" label="所属者"></el-table-column>
                  <el-table-column prop="number" label="歌曲数量"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button type="primary" @click="getSongMusic(scope.row)"> 播放并查看 </el-button>
                      <el-button type="primary" @click="delcollect(scope.row)"> 取消收藏 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </div>

<!--            我听过的-->
            <div style="margin: 10px 0" v-if="getType==='listened'">
              <div>
                <el-button type="primary" style="margin-bottom: 10px" @click="emptyListened"> 清空历史 </el-button>
              </div>
              <el-table :data="musicListened" border stripe :header-cell-class-name="'headerBg'">
                <el-table-column prop="name" label="歌曲名" width="140"></el-table-column>
                <el-table-column prop="singer" label="歌手"></el-table-column>
                <el-table-column prop="listened_time" label="听歌时间"></el-table-column>
                <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                <el-table-column label="操作" width="500" align="center">
                  <template #default="scope">
                    <el-button type="primary" @click="display(scope.row)"> 播 放 </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>

<!--            ai-->
            <div style="margin: 10px 0" v-if="getType==='ai'">
              <el-card class="box-card" :style="{ height: '400px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">歌曲榜单</h1>
                </div>
                <div class="photo-container">
                  <el-card class="photo-card">
                    <div slot="header" class="clearfix">
                      <h1 style="text-align: center">ai生成</h1>
                    </div>
                  </el-card>
                  <el-card class="photo-card">
                    <div slot="header" class="clearfix">
                      <h1 style="text-align: center">ai生成</h1>
                    </div>
                  </el-card>
                </div>
              </el-card>
            </div>


<!--            榜单的弹窗-->
            <el-dialog
                v-model="dialogFormVisibleBD"
                width="1000"
                align-center
            >
              <el-card class="box-card" :style="{ height: '400px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">{{ nameBD }}</h1>
                </div>
                <el-table :data="selectedData" border stripe :header-cell-class-name="'headerBg'"
                          style="margin-top: 30px">
                  <el-table-column prop="name" label="歌曲名" width="140"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button type="primary" @click="display(scope.row)"> 播 放 </el-button>
                      <el-button type="primary" @click="like(scope.row,'music')"> 点 赞 </el-button>
                      <el-button type="success" @click="comment(scope.row)"> 评 论 </el-button>
                      <el-button type="success" @click="add(scope.row)"> 添加至 我的歌单 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-dialog>

            <el-dialog
                v-model="dialogFormVisibleC"
                width="1500"
                align-center
            >
              <el-card class="box-card" :style="{ height: '1000px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center"><< {{ musicCom.name }} >>评论区</h1>
                </div>
                <div>
                  <!--              热门评论-->
                  <el-card class="box-card" :style="{ height: '400px' }" style="margin-top: 30px">
                    <div slot="header" class="clearfix">
                      <h1 style="text-align: center">热门评论</h1>
                    </div>
                    <el-table :data="commentHot" border stripe :header-cell-class-name="'headerBg'">
                      <el-table-column prop="username" label="评论者" width="140"></el-table-column>
                      <el-table-column prop="content" label="评论内容"></el-table-column>
                      <el-table-column prop="support" label="点赞数"></el-table-column>
                      <el-table-column prop="create_time" label="评论时间"></el-table-column>
                      <el-table-column label="操作" width="500" align="center">
                        <template #default="scope">
                          <el-button type="primary" @click="opencomment(scope.row.id)"> 评论 </el-button>
                          <el-button type="primary" @click="like(scope.row,'comment')"> 点赞 </el-button>
                          <el-button type="primary" v-if="scope.row.user_id === user.id" @click="delComment(scope.row, 'comment')"> 删除 </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-card>
                  <!--              最新评论-->
                  <el-card class="box-card" :style="{ height: '400px' }">
                    <div slot="header" class="clearfix">
                      <h1 style="text-align: center">最新评论</h1>
                    </div>
                    <el-table :data="commentHot" border stripe :header-cell-class-name="'headerBg'">
                      <el-table-column prop="username" label="评论者" width="140"></el-table-column>
                      <el-table-column prop="content" label="评论内容"></el-table-column>
                      <el-table-column prop="support" label="点赞数"></el-table-column>
                      <el-table-column prop="create_time" label="评论时间"></el-table-column>
                      <el-table-column label="操作" width="500" align="center">
                        <template #default="scope">
                          <el-button type="primary" @click="opencomment(scope.row.id)"> 评论 </el-button>
                          <el-button type="primary" @click="like(scope.row,'comment')"> 点赞 </el-button>
                          <el-button type="primary" v-if="scope.row.user_id === user.id" @click="delComment(scope.row, 'comment')"> 删除 </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-card>
                </div>
              </el-card>
              <template #footer>
                <div class="dialog-footer">
                  <el-button type="primary" @click="opencomment(0)"> 评 论 </el-button>
                  <el-button type="success" @click="dialogFormVisibleC = false"> back </el-button>
                </div>
              </template>
            </el-dialog>


<!--            新增评论弹窗-->
            <el-dialog
                v-model="contentDialogVisible"
                title="新增评论"
                width="1000"
                align-center
            >
              <el-form>
                <el-form-item label="评论">
                  <el-input type="textarea" v-model="content" autocomplete="off"></el-input>
                </el-form-item>
              </el-form>
              <template #footer>
                <div class="dialog-footer">
                  <el-button type="primary" @click="addcomment(content)">发 布</el-button>
                  <el-button @click="contentDialogVisible = false">返 回</el-button>
                </div>
              </template>
            </el-dialog>

<!--            添加歌曲至我的歌单-->
            <el-dialog
                v-model="dialogVisibleToList"
                width="1500"
                align-center
            >
              <el-card class="box-card" :style="{ height: '600px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center"> 我 的 歌 单 </h1>
                </div>
                <div>
                  <el-card class="box-card" :style="{ height: '400px' }" style="margin-top: 30px">
                    <el-table :data="songListMine" border stripe :header-cell-class-name="'headerBg'">
                      <el-table-column prop="name" label="名称" width="140"></el-table-column>
                      <el-table-column prop="number" label="歌曲数量"></el-table-column>
                      <el-table-column prop="support" label="点赞数"></el-table-column>
                      <el-table-column prop="is_upload_msg" label="上传阶段"></el-table-column>
                      <el-table-column label="操作" width="500" align="center">
                        <template #default="scope">
                          <el-button type="primary" v-if="scope.row.is_upload === 0 " @click="addTo(scope.row.id)"> 添 加 </el-button>
                          <el-button type="primary" @click="updateSongList(scope.row)"> 查看 </el-button>
                          <el-button type="primary" v-if="scope.row.user_id === 0 " @click="uploadSongList(scope.row)"> 上 传 </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-card>
                </div>
              </el-card>
              <template #footer>
                <div class="dialog-footer">
                  <el-button type="primary" @click="openAddSongList()"> 新 增 歌 单 </el-button>
                  <el-button type="success" @click="dialogVisibleToList = false"> back </el-button>
                </div>
              </template>
            </el-dialog>



          </div>
        </el-col>
        <el-col :span="3"></el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import { mapMutations } from 'vuex';
import photo1 from '@/assets/image/hotsongBD.png';
import photo2 from '@/assets/image/newsongBD.png';
import photo3 from '@/assets/image/aisongBD.png';
export default {
  name: "adminHomeView",
  data() {
    return {
      user:localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      getType: 'home',
      // 推荐
      nameBD:'',
      photos: [
        { id: 1, url: photo1 },
        { id: 2, url: photo2 },
        { id: 3, url: photo3 }
      ],
      hotMusic:[],
      dialogFormVisibleBD:false,
      newMusic:[],
      aiMusic:[],
      songListHot:[],
      // 搜索
      searchData:{
        type:'search',
        serName:'',
        serSName:'',
      },
      musicListAll:[],
      //正在播放的歌单
      songListNow:[],
      // key的修改
      customKeys:{
        name: '名称',
        description: '描述',
        owner: '所属者',
        singer: '歌手',
        mold: '类型',
        nameParent: '源音乐',
        userName: '上传者',
        username: '姓名',
        email: '邮箱',
        create_time: '创建时间',
        content: '审核结果',
      },
      // 正在播放的歌单的歌曲列表
      songMusicList:[],
      // 我的歌单+收藏歌单
      songListMine:[],
      songListCollect:[],
      // 我听过的歌曲列表
      musicListened:[],
      // 评论 热门+最新
      dialogFormVisibleC:false,
      musicCom:[],
      commentHot:[],
      commentNew:[],
      contentDialogVisible:false,
      commentId:0,
      content:'',
      musicToList:'',
      dialogVisibleToList:false,
    }
  },
  computed: {
    selectedData() {
      return this.nameBD === "热歌榜" ? this.hotMusic : (this.nameBD === "新歌榜" ? this.newMusic : this.aiMusic);
    }
  },
  created() {
    this.load()
  },
  methods: {
    goToDetail(id) {
      this.nameBD=id===1 ? "热歌榜": (id===2 ? "新歌榜" : "AI榜")
      const data = {
        type: this.nameBD === "热歌榜" ? 'hot' : (this.nameBD === "新歌榜" ? 'new' : 'ai'),
        serName:'',
      }
      fetch('http://127.0.0.1:9001/serMusic/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.hotMusic  = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })
      this.dialogFormVisibleBD = true
    },
    songMusicB(){
      this.getType = 'songMusic'
    },
    recommendB(){
      this.getType = 'recommend'
      const data = {
        type:'hot',
        serSName:'',
      }
      fetch('http://127.0.0.1:9001/serSongList/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.songListHot  = data.listHot
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    searchB(){
      this.getType = 'search'
      fetch('http://127.0.0.1:9001/serMusic/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.searchData),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.musicListAll  = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    songListB(){
      this.getType = 'songList'
    },
    listenedB(){
      this.getType = 'listened'
    },
    aiB(){
      this.getType = 'ai'
    },
    load(){
    //   数据初始化
    //   搜索的热门歌单名
      const data = {
        type:'hot',
        serName:'',
      }
      fetch('http://127.0.0.1:9001/serMusic/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.hotMusic  = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })

      // 添加至 我的歌单 弹窗
      const data2 = {
        type:'get',
        serSName:this.searchData.serSName,
      }
      fetch('http://127.0.0.1:9001/serSongList/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data2),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.songListMine  = data.listMine
              this.songListCollect = data.listCollect
            }
            this.$notify({
              title: data.msg
            });
          })

    },
    handleMusicNameClick(id){
    //   点击歌曲name 播放歌曲
    },
    search(){
    //   根据serName搜索歌曲
      if (this.getType === 'search') this.searchB()
      else if (this.type === 'songList') this.songListB()
    },
    reset(){
    //   搜索重置
      this.searchData.serName = ''
      this.searchData.serSName = ''
      this.search()
    },
    display(row){
    //   播放歌曲
    },
    comment(row){
    //   评论歌曲
      this.musicCom = row
      const data={
        musicId:row.id,
      }
      fetch('http://127.0.0.1:9001/getComments/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.commentHot = data.commentListHot
              this.commentNew = data.commentListNew
              this.dialogFormVisibleC = true
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    getSongMusic(row){
    //   歌单的点击播放并查看
    },
    collect(row){
    //   收藏歌单
    },
    delcollect(row){
    //   取消收藏
    },
    emptyListened(){
    //   清空我听过的历史
    },
    add(row){
    //   添加至我的歌单  弹框
      this.musicToList = row
      this.dialogVisibleToList = true
    },
    delMusic(row){
    //   从未上传的歌单中删除歌曲
    },
    updateSongList(row){
    //   更新歌单的post信息
    },
    uploadSongList(row){
    //   直接上传歌单
    },
    delSongList(row){
    //   删除我的歌单  上传+未上传
    },
    opencomment(cid){
      this.contentDialogVisible = true
      this.commentId = cid
    },
    addcomment(content){
    //   新增评论
      const data={
        mid:this.musicCom.id,
        userId:this.user.id,
        content:content,
        pid:this.commentId,
      }
      fetch('http://127.0.0.1:9001/comment/addComment/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.contentDialogVisible = false
              this.comment(this.musicCom)
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    delComment(row, type){
    //   删除评论
      const data = {
        getType: type,
        id:row.id,
      }
      fetch('http://127.0.0.1:9001/delById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              this.comment(this.musicCom)
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    like(row,type){
      //   点赞歌曲
      const data = {
        type: type,
        id:row.id,
      }
      fetch('http://127.0.0.1:9001/supportById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200){
              if (type === 'search')  this.searchB()
              else if (type === 'comment') this.comment(this.musicCom)
            }
            this.$notify({
              title: data.msg
            });
          })
    },
  }
}
</script>


<style scoped>
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 6px;
  min-height: 50px;
}
.grid-contents {
  border-radius: 6px;
  min-height: 2500px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.headerBg {
  background: #eee !important;
}
.photo-container {
  display: flex;
  justify-content: space-around;
}

.photo-card {
  width: 30%;
  text-align: center;
}
.photo-img {
  width: 120px; /* 设置图片宽度 */
  height: 120px; /* 设置图片高度 */
}
</style>
