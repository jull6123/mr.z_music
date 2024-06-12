<template>
  <el-container>
    <el-header>
      <template #default="scope">
        <el-row class="grid-content bg-black-light audio"></el-row>
        <div class="audio audioControler">
          <audio  ref="audioplayer"  controls :src="MusicUrl" style="width: 1150px" autoplay></audio>
        </div>
        <div style="left: 50px" class="audio audioButton">
          <el-button style="width: 60px;height: 40px;" @click="previousMusic">
          <el-icon><ArrowLeftBold /></el-icon>
        </el-button>
        </div>
        <div class="audio audioButton" style="left: 150px;">
          <el-button style="width: 60px;height: 40px;">
            <el-icon size="large" @click="nextMusic"><ArrowRightBold /></el-icon>
          </el-button>
        </div>
      <el-row class="grid-content bg-black-light head-button" :gutter="16">
        <el-col :span="3"></el-col>
        <el-col :span="3" style="text-align: center" class="grid-content"><div style="margin-top: 16px;font-size: 28px">音你心动</div></el-col>
        <el-col :span="2" style="text-align: center;height: 70px"
                :class="[getType==='songMusic' && 'grid-content bg-black-dark']">
          <div  type="text" @click="songMusicB" style="margin-top: 20px">正在播放</div>
        </el-col>
        <el-col :span="1" style="text-align: center"
                :class="[getType==='recommend' && 'grid-content bg-black-dark']">
          <div type="text" @click="recommendB" style="margin-top: 20px"> 推 荐 </div>
        </el-col>
        <el-col :span="1" style="text-align: center"
                :class="[getType==='search' && 'grid-content bg-black-dark']">
          <div type="text" @click="searchB" style="margin-top: 20px">搜 索</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='songList' && 'grid-content bg-black-dark']">
          <div type="text" @click="songListB" style="margin-top: 20px">我的歌单</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='listened' && 'grid-content bg-black-dark']">
          <div type="text" @click="listenedB" style="margin-top: 20px">我听过的</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='ai' && 'grid-content bg-black-dark']">
          <div type="text" @click="aiB" style="margin-top: 20px">AI生成</div>
        </el-col>
        <el-col :span="2" style="text-align: center"
                :class="[getType==='upload' && 'grid-content bg-black-dark']">
          <div type="text" @click="$router.push({path: '/uploadPost', query: {uploadMold: 'music'}})" style="margin-top: 20px">上传歌曲</div>
        </el-col>
        <el-col :span="1"></el-col>
        <el-icon style="margin-top: 24px"><User /></el-icon>
        <el-col :span="1" style="text-align: center">
          <el-dropdown trigger="click">
            <h3 class="el-dropdown-link mx-1" size="large" type="text" style="margin-top: 24px;font-size: 18px;color: #ffffff">{{ user.username }}</h3>
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
      </template>
    </el-header>
    <el-main style="z-index: 1">
      <el-row :gutter="20">
        <el-col :span="3"></el-col>
        <el-col :span="18" class="grid-contents bg-purple-light">
          <div>
            <div style="margin: 10px 0" v-if="getType==='home'">
              <!--              搜索框-->
              <el-card class="box-card" style="height: 600px;font-size: 20px">
                <h1>欢迎使用音你心动</h1>
                 <h2>本网站提供音乐播放和AI录歌</h2>
                <p>{{this.MusicUrls[0]}}</p>
                 <p>{{this.MusicNumber}}</p>
              </el-card>
            </div>

            <!--        搜索        -->
            <div style="margin: 10px 0" v-if="getType==='search'">
<!--              搜索框-->
              <el-card class="box-card" :style="{ height: '80px' }">
                <span >热门歌曲：</span>
                <span style="margin-left: 5px" v-for="(value, key) in hotMusic" :key="key" class="text item">
                  <span style="margin-left: 5px" v-for="(val, keys) in value" :key="keys" class="text item">
                    <template v-if="keys === 'name'">
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
              <el-card class="box-card" :style="{ height: '600px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">音乐列表</h1>
                </div>
                <el-table :data="musicListAll" border stripe :header-cell-class-name="'headerBg'"
                          style="margin-top: 30px">
                  <el-table-column prop="name" label="歌曲名" width="250"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <p>{{this.currentIndex}}</p>
                      <el-button style="border: none" @click="display(scope.row);display2(scope.row.id)"><el-icon style="font-size: 28px"><VideoPlay /></el-icon></el-button>
                      <el-button type="primary" @click="like(scope.row,'music')"> 点 赞 </el-button>
                      <el-button type="success" @click="comment(scope.row)"> 评 论 </el-button>
                      <el-button type="success" @click="add(scope.row)"> 添加至 我的歌单 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
<!--              我的上传或未上传的 除：上传失败的-->
              <el-card class="box-card" :style="{ height: '400px' }" style="margin-top: 30px">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">我的歌曲</h1>
                </div>
                <el-table :data="mymusicALL" border stripe :header-cell-class-name="'headerBg'"
                          style="margin-top: 30px">
                  <el-table-column prop="name" label="歌曲名" width="250"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column prop="is_upload_msg" label="审核状态"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
<!--                      均可播放-->
                      <el-button @click="display(scope.row);display2(scope.row.url)"><el-icon><VideoPlay /></el-icon></el-button>
<!--                      未上传可修改，上传，，其他只可查看-->
                      <el-button type="success" v-if="scope.row.is_upload !== 0" @click="openUploadView('had', 'music', scope.row.id)"> 查 看 </el-button>
                      <el-button type="success" v-if="scope.row.is_upload === 0" @click="openUploadView('had', 'music', scope.row.id)"> 修 改 </el-button>
                      <el-button type="success" v-if="scope.row.is_upload === 0" @click="upload('music',  scope.row)"> 上 传 </el-button>
<!--                      上传成功的-->
                      <el-button type="success" v-if="scope.row.is_upload === 3" @click="comment(scope.row)"> 评 论 </el-button>
                      <el-button type="success" v-if="scope.row.is_upload === 3" @click="add(scope.row)"> 添加至 我的歌单 </el-button>
<!--                      审核中的可催办-->
                      <el-button type="success" v-if="scope.row.is_upload === 1" @click="press"> 催 办 </el-button>
<!--                     除审核中的均可删除-->
                      <el-button type="success" v-if="scope.row.is_upload !==　2" @click="delAnyById('music', scope.row.id)"> 删 除 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
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
                  <el-table-column prop="name" label="名称" width="250"></el-table-column>
                  <el-table-column prop="owner" label="所属者"></el-table-column>
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
              <el-card class="box-card" v-if="toType==='songList'" :style="{ height: '1000px' }">
                <el-card class="box-card" >
                  <div slot="header" class="clearfix">
                    <h1 style="text-align: center">歌 单 ：  {{ songListNow.name }}</h1>
                  </div>
                  <div style="margin-top: 20px">
                    <div v-for="(value, key) in songListNow" :key="key" class="text item" style="text-align: center; margin-top: 10px">
                      <div v-if="songListNow.is_upload === 3">
                        <template v-if="key !== 'id' && key !== 'avatar' && key !== 'is_upload' && key !== 'auditContent' && key !== 'is_upload_msg'
                          && key !== 'uid' && key !== 'audit_id' && key !== 'name' &&　key !== 'auditResult'">
                          {{ customKeys[key] }} :  {{ value }}
                        </template>
                      </div>
                      <div v-if="songListNow.is_upload < 2">
                        <template v-if="key !== 'id' && key !== 'avatar' && key !== 'is_upload' && key !== 'auditContent'
                          && key !== 'uid' && key !== 'audit_id' && key !== 'name' &&　key !== 'auditResult'">
                          {{ customKeys[key] }} :  {{ value }}
                        </template>
                      </div>

                    </div>
                  </div>

                  <div style="padding-top: 30px; text-align: right;" >
                    <el-button type="primary" v-if="songListNow.uid !== user.id" @click="like(songListNow,'songList')"> 点 赞 </el-button>
                    <el-button type="primary" v-if="songListNow.uid !== user.id" @click="collect(songListNow)"> 收 藏 </el-button>
                    <el-button type="primary" v-if="songListNow.uid === user.id &&　songListNow.is_upload === 0" @click="upload('songList', songListNow)"> 上 传 </el-button>
                  </div>
                </el-card>
                <!--              歌单的歌曲列表-->
                <el-table :data="songMusicList" border stripe :header-cell-class-name="'headerBg'"
                          style="margin-top: 30px">
                  <el-table-column prop="name" label="歌曲名" width="250"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button style="border: none" @click="display(scope.row);display2(scope.row.id)"><el-icon style="font-size: 28px"><VideoPlay /></el-icon></el-button>
                      <el-button type="primary" @click="like(scope.row, 'music')"> 点 赞 </el-button>
                      <el-button type="success" @click="comment(scope.row)"> 评 论 </el-button>
                      <el-button type="success" v-if="user.id !== songListNow.uid " @click="add(scope.row)"> 添加至 我的歌单 </el-button>
                      <el-button type="success" v-if="user.id === songListNow.uid && songListNow.is_upload === 0" @click="delAnyById('musicCollect', scope.row.id)"> 删 除 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
<!--              单个的播放的歌曲列表-->
              <el-card class="box-card" style="margin-top: 50px" v-if="toType==='music'" :style="{ height: '500px' }">
                <div slot="header" class="clearfix">
                  <h2 style="text-align: center">歌 曲 列 表</h2>
                </div>
                <h4 style="margin-right: 50px;text-align: right;margin-top: 30px">仅展示 15 首</h4>
                <el-table :data="displayMusics" border stripe :header-cell-class-name="'headerBg'"
                          style="margin-top: 5px">
                  <el-table-column prop="name" label="歌曲名" width="250"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                  <el-table-column prop="number" label="播放次数"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button style="border: none" @click="display(scope.row);display2(scope.row.id)"><el-icon style="font-size: 28px"><VideoPlay /></el-icon></el-button>
                      <el-button type="success" @click="comment(scope.row)"> 评 论 </el-button>
                      <el-button type="success" v-if="user.id !== songListNow.uid " @click="add(scope.row)"> 添加至 我的歌单 </el-button>
                      <el-button type="success" v-if="user.id === songListNow.uid && songListNow.is_upload === 0" @click="delAnyById('musicCollect', scope.row.id)"> 删 除 </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </div>

<!--            我的歌单-->
            <div style="margin: 10px 0" v-if="getType==='songList'">
              <el-card class="box-card" :style="{ height: '80px' }">
                <el-input style="width: 200px" placeholder="请输入歌单名" suffix-icon="el-icon-message" class="ml-5"
                          v-model="searchData.serSName" input-style="margin-left: 5px"></el-input>
                <el-button class="ml-5" type="primary" @click="search">搜 索</el-button>
                <el-button type="warning" @click="reset">重 置</el-button>
                <el-button type="danger" @click="openUploadView('new', 'songList',0)">新 建</el-button>
              </el-card>
              <!--              我的歌单-->
              <el-card class="box-card" :style="{ height: '400px' }">
                <div slot="header" class="clearfix">
                  <h1 style="text-align: center">我的歌单</h1>
                </div>
                <el-table :data="songListMine" border stripe :header-cell-class-name="'headerBg'">
                  <el-table-column prop="name" label="名称" width="250"></el-table-column>
                  <el-table-column prop="number" label="歌曲数量"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="is_upload_msg" label="上传阶段"></el-table-column>
                  <el-table-column prop="auditContent" label="审核结果"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button style="border: none" v-if="scope.row.is_upload !== 2" @click="getSongMusic(scope.row);display2(scope.row.id)"> 播放并查看 </el-button>
                      <el-button style="border: none" v-if="scope.row.is_upload === 1" @click="press"> 催 办 </el-button>
                      <el-button style="border: none" v-if="scope.row.is_upload === 0" @click="openUploadView('had', 'songList', scope.row.id)"> 修 改 </el-button>
                      <el-button style="border: none" v-if="scope.row.is_upload === 0" @click="upload('songList', scope.row)"> 上 传 </el-button>
                      <el-button style="border: none" v-if="scope.row.is_upload === 0 || scope.row.is_upload === 2" @click="delAnyById('mine', scope.row.id)"> 删 除 </el-button>
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
                  <el-table-column prop="name" label="名称" width="250"></el-table-column>
                  <el-table-column prop="owner" label="所属者"></el-table-column>
                  <el-table-column prop="number" label="歌曲数量"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button type="primary" @click="getSongMusic(scope.row);display2(scope.row.id)"> 播放并查看 </el-button>
                      <el-button type="primary" @click="delAnyById('collect', scope.row.id)"> 取消收藏 </el-button>
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
                <el-table-column prop="name" label="歌曲名" width="250"></el-table-column>
                <el-table-column prop="singer" label="歌手"></el-table-column>
                <el-table-column prop="listened_time" label="听歌时间"></el-table-column>
                <el-table-column prop="duration_time" label="歌曲时长"></el-table-column>
                <el-table-column label="操作" width="500" align="center">
                  <template #default="scope">
                    <el-button style="border: none" @click="display(scope.row);display2(scope.row.id)"><el-icon style="font-size: 20px"><VideoPlay /></el-icon></el-button>
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
                  <el-table-column prop="name" label="歌曲名" width="150"></el-table-column>
                  <el-table-column prop="singer" label="歌手"></el-table-column>
                  <el-table-column prop="support" label="点赞数"></el-table-column>
                  <el-table-column prop="duration_time" label="歌曲时长" width="150"></el-table-column>
                  <el-table-column label="操作" width="500" align="center">
                    <template #default="scope">
                      <el-button type="primary" @click="display(scope.row);display2(scope.row.id)"> 播 放 </el-button>
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
                          <el-button type="primary" v-if="scope.row.user_id === user.id" @click="delAnyById('comment', scope.row.id)"> 删除 </el-button>
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
                          <el-button type="primary" v-if="scope.row.user_id === user.id" @click="delAnyById('comment', scope.row.id)"> 删除 </el-button>
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
                          <el-button type="primary" v-if="scope.row.is_upload !== 0 " @click="openUploadView('had', 'songList', scope.row.id)"> 查 看 </el-button>
                          <el-button type="primary" v-if="scope.row.is_upload === 0 " @click="openUploadView('had', 'songList', scope.row.id)"> 修 改 </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-card>
                </div>
              </el-card>
              <template #footer>
                <div class="dialog-footer">
                  <el-button type="primary" @click="openUploadView('new','songList', 0)"> 新 增 歌 单 </el-button>
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
import axios from 'axios';
export default {
  name: "adminHomeView",
  data() {
    return {
      mode:'repeat',
      MusicUrls: [],
      MusicNumber:2,
      MusicUrl:[],
      currentIndex:'',
      user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : {},
      getType: this.$route.query.where ? this.$route.query.where : 'home', //home songMusic recommend search songList listened ai upload

      // 推荐
      nameBD: '',
      dialogFormVisibleBD: false, //榜单dialog
      photos: [
        {id: 1, url: photo1},
        {id: 2, url: photo2},
        {id: 3, url: photo3}
      ],
      hotMusic: [], //热歌榜歌曲
      newMusic: [], //新歌榜歌曲
      aiMusic: [], //ai歌曲榜
      songListHot: [], //热歌榜歌单

      // 搜索
      searchData: {
        userId: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")).id : 0,
        type: 'search',
        serName: '',
        serSName: '',
      },
      musicListAll: [], //全部的已上传的歌曲列表/搜索的歌曲列表
      mymusicALL: [], //我的歌曲列表

      // 正在播放
      toType: 'music',
      displayMusics: [],
      songListNow: [],//正在播放的歌单
      songMusicList: [], // 正在播放的歌单的歌曲列表

      // 我的歌单
      songListMine: [], //我的歌单
      songListCollect: [], //收藏歌单

      // 我听过的歌曲列表
      musicListened: [],

      // 评论 热门+最新
      dialogFormVisibleC: false, //评论区dialog
      musicCom: [], //打开评论区的歌曲
      commentHot: [], //热门评论
      commentNew: [], //最新评论
      contentDialogVisible: false, //新增评论dialog
      commentId: 0,
      content: '', //评论内容

      //向我的歌单添加歌曲
      musicToList: '', //歌曲本身数据
      dialogVisibleToList: false, //添加我的歌单dialog

      // key的修改
      customKeys: {
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
        number: '歌曲数量',
        support: '点赞数量',
        is_upload_msg: '上传阶段',
        auditContent: '审核结果',
      },
    }
  },
  mounted() {
    this.getUrls();
  },
  computed: {
    selectedData() {
      return this.nameBD === "热歌榜" ? this.hotMusic : (this.nameBD === "新歌榜" ? this.newMusic : this.aiMusic);
    }
  },
  created() {
    this.load();
  },
  methods: {
    getUrls(){
      fetch('http://127.0.0.1:9001/get_urls/') // 替换为你的实际API端点URL
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
       .then(urls => {
           this.MusicUrls = urls;
        })
     },
    getMusics(type) {
      const data = {
        type: type,
        serName: this.getType === 'search' ? this.searchData.serName : '',
        userId: this.user.id,
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
            if (data.code === 200) {
              if (type === 'hot') this.hotMusic = data.musicList
              else if (type === 'new') this.newMusic = data.musicList
              else if (type === 'ai') this.aiMusic = data.musicList
              else if (type === 'search') this.musicListAll = data.musicList
              else if (type === 'mine') this.mymusicALL = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    getSongLists(type) {
      const data = {
        type: type,
        userId: this.user.id,
        serSName: this.getType === 'songList' ? this.searchData.serSName : '',
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
            if (data.code === 200) {
              if (type === 'get') {
                this.songListMine = data.listMine
                this.songListCollect = data.listCollect
              } else if (type === 'hot')
                this.songListHot = data.listHot
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    getListenedById() {
      fetch('http://127.0.0.1:9001/listHistoryById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({userId: this.user.id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              this.musicListened = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    goToDetail(id) {
      this.nameBD = id === 1 ? "热歌榜" : (id === 2 ? "新歌榜" : "AI榜")
      const type = this.nameBD === "热歌榜" ? 'hot' : (this.nameBD === "新歌榜" ? 'new' : 'ai')
      this.getMusics(type)
      this.dialogFormVisibleBD = true
    },
    load() {
      this.getMusics('hot')
      this.getSongLists('get')
      if (this.getType === 'search') {
        this.getMusics('search')
        this.getMusics('mine')
      }
    },
    songMusicB() {
      this.getType = 'songMusic'
    },
    recommendB() {
      this.getType = 'recommend'
      this.getSongLists('hot')
    },
    searchB() {
      this.getType = 'search'
      this.getMusics('search')
      this.getMusics('mine')
    },
    songListB() {
      this.getType = 'songList'
      this.getSongLists('get')
    },
    listenedB() {
      this.getType = 'listened'
      this.getListenedById()
    },
    aiB() {
      this.getType = 'ai'
    },
    search() {
      if (this.getType === 'search') {
        this.searchB()
      } else {
        this.songListB()
      }
    },
    reset() {
      //   搜索重置
      this.searchData.serName = ''
      this.searchData.serSName = ''
      this.search()
    },
    display(row) {
      let existingRow = this.displayMusics.find(item => item.id === row.id);
      this.currentIndex = row.id;
      if (!existingRow) {
        if (this.displayMusics.length >= 15) {
          this.displayMusics.shift();
        }
        row.number = 1;
        this.displayMusics.push(row);
      } else {
        existingRow.number++;
      }
          //   添加播放记录至"我听过的"
          fetch('http://127.0.0.1:9001/song/listenedMusic/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({mid: row.id, userId: this.user.id}),
          })
              .then(response => response.json())
              .then(data => {
                if (data.code === 200) {
                  this.getListenedById()
                }
                this.$notify({
                  title: data.msg
                });
              })
    },
    display2(id)
    {
      this.currentIndex = id;
      this.MusicUrl = this.MusicUrls[id-1];
      this.$refs.audioplayer.play();
    },
    nextMusic(){
      if(this.currentIndex==this.MusicNumber)
      {
        this.currentIndex = 1;
        this.display2(this.currentIndex);
      }else {
        this.currentIndex = this.currentIndex + 1;
        this.display2(this.currentIndex);
      }
    },
    previousMusic(){
      if(this.currentIndex==1)
      {
        this.currentIndex = this.MusicNumber;
        this.display2(this.currentIndex);
      }else {
        this.currentIndex = this.currentIndex - 1;
        this.display2(this.currentIndex);
      }

    },
    comment(row) {
      //   评论歌曲
      this.musicCom = row
      fetch('http://127.0.0.1:9001/getComments/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({musicId: row.id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              this.commentHot = data.commentListHot
              this.commentNew = data.commentListNew
              this.dialogFormVisibleC = true
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    opencomment(cid) {
      this.contentDialogVisible = true
      this.content = ''
      this.commentId = cid
    },
    addcomment(content) {
      //   新增评论
      const data = {
        mid: this.musicCom.id,
        userId: this.user.id,
        content: content,
        pid: this.commentId,
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
            if (data.code === 200) {
              this.contentDialogVisible = false
              this.comment(this.musicCom)
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    getSongMusic(row) {
      //   歌单的点击播放并查看
      this.toType = 'songList'
      this.getType = 'songMusic'
      this.getsongListFrom(row.id)
      this.getsongMusicList(row.id)
    },
    getsongListFrom(id) {
      fetch('http://127.0.0.1:9001/getFormById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({sid: id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              this.songListNow = data.songList
            }
          })
    },
    getsongMusicList(id) {
      fetch('http://127.0.0.1:9001/getListById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({sid: id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              this.songMusicList = data.musicList
            }
          })
    },
    collect(row) {
      //   收藏歌单
      fetch('http://127.0.0.1:9001/songList/collectSongList/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({sid: row.id, userId: this.user.id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              this.songMusicList = data.musicList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    emptyListened() {
      //   清空我听过的历史
      fetch('http://127.0.0.1:9001/clearHistoryById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({userId: this.user.id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              this.getListenedById()
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    add(row) {
      //   添加至我的歌单  弹框
      this.musicToList = row
      this.dialogVisibleToList = true
    },
    addTo(sid) {
      fetch('http://127.0.0.1:9001/song/collectMusicToList/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({mid: this.musicToList.id, sid: sid}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              this.songListMine = data.songList
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    upload(type, row) {
      fetch('http://127.0.0.1:9001/upload/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({type: type, id: row.id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              if (type === 'music') {
                this.search()
              } else if (type === 'songList') {
                if (this.getType === 'songList') this.getSongLists('get')
                else if (this.getType === 'songMusic') this.getsongListFrom(row.id)
              }
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    like(row, type) {
      //   点赞歌曲
      fetch('http://127.0.0.1:9001/supportById/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({type: type, id: row.id}),
      })
          .then(response => response.json())
          .then(data => {
            if (data.code === 200) {
              if (this.getType === 'search' && type === 'music') this.searchB()
              else if (type === 'comment') this.comment(this.musicCom)
              else if (this.getType !== 'recommend' && type === 'songList') this.getsongListFrom(this.songListNow.id)
              else if (this.getType === 'songMusic' && type === 'music') this.getsongMusicList(this.songListNow.id)
              else if (this.getType === 'recommend' && type === 'music') this.getMusics('hot')
              else if (this.getType === 'recommend' && type === 'songList') this.getSongLists('hot')
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    delAnyById(type, id) {
      const data = {
        getType: type,
        id: id,
        userId: this.user.id,
        sid: this.songListNow.id,
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
            if (data.code === 200) {
              if (type === 'comment') this.comment(this.musicCom)
              if (type === 'music' && this.getType === 'search') this.search()
              if (type === 'mine' || type === 'collect') this.getSongLists('get')
              if (type === 'musicCollect') this.getSongMusic(this.songMusicList)
            }
            this.$notify({
              title: data.msg
            });
          })
    },
    openUploadView(type, mold, id) {
      if (type === 'new') {
        this.$router.push({path: '/uploadPost', query: {uploadMold: mold, where: this.getType}})
      } else if (type === 'had') {
        if (mold == 'songList') this.$router.push({
          path: '/uploadPost',
          query: {uploadMold: mold, sid: id, where: this.getType}
        })
        else if (mold === 'music') this.$router.push({
          path: '/uploadPost',
          query: {uploadMold: mold, mid: id, where: this.getType}
        })
      }
    },
    press() {
      this.$notify({
        title: "已催办，等耐心等待哦~~"
      });
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
.bg-black-light{
  background: #333333;
}
.bg-black-dark{
  background: #0f0f0f;
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
.head-button{
  color: #ffffff;
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
.audio{
  position: fixed;
  top: 790px;
  width: 1700px;
  height: 150px;
  z-index: 2;
}
.audioControler{
  left: 250px;
  width: 1150px;
}
.audioButton{
  top: 800px;
  width: 100px;
  height: 100px;
}
</style>
