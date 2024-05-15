<template>
  <div class="nav-bar">
    <nav-bar-item class="navname" path="/main/upload">
      <div slot="nav" class="nav_content">
        <i class="el-icon-upload iconfont sidebar-icon"></i
        ><span class="text">文献管理</span>
      </div>
    </nav-bar-item>

    <nav-bar-item class="navname" path="/main/answer">
      <div slot="nav" class="nav_content">
        <i class="el-icon-s-fold iconfont sidebar-icon"></i
        ><span class="text">问答管理</span>
      </div>
    </nav-bar-item>

    <nav-bar-item class="navname" path="/main/graph">
      <div slot="nav" class="nav_content">
        <i class="el-icon-picture-outline-round iconfont sidebar-icon"></i
        ><span class="text">知识图谱</span>
      </div>
    </nav-bar-item>

    <nav-bar-item
      class="navname"
      path="/main/management"
      v-show="this.$store.getters.getIdentity"
    >
      <div slot="nav" class="nav_content">
        <i class="el-icon-user iconfont sidebar-icon"></i
        ><span class="text">权限管理</span>
      </div>
    </nav-bar-item>

    <div class="bottom">
      <nav-bar-item
        class="navname"
        path="/main/setting"
        @click="showButtons = !showButtons"
      >
        <div slot="nav" class="nav_content">
          <el-menu
            :default-active="activeIndex"
            mode="horizontal"
            @select="handleSelect"
            class="full-size"
            background-color="#f8fafc"
          >
            <el-submenu index="2" class="full-size haha">
              <template slot="title">
                <div slot="nav" class="ah">
                  <span class="text el-icon-s-custom">{{username}} ({{identity}})</span>
                </div>
              </template>
              <el-dropdown-item
                @click.native="layout"
                icon="el-icon-circle-close"
                class="el-dropdown-item"
                style="padding-left: 20px"
              >
                <span class="text" style="text-align: center">退出登录</span>
              </el-dropdown-item>
              <el-dropdown-item
                @click.native="layoff"
                icon="el-icon-delete"
                class="el-dropdown-item"
                style="padding-left: 20px"
                >&nbsp;<span class="text" style="text-align: center"
                  >注销账号</span
                ></el-dropdown-item
              >
            </el-submenu>
          </el-menu>

          <!-- <i class="el-icon-setting iconfont sidebar-icon"></i
          ><span class="text">系统设置</span> -->
        </div>
      </nav-bar-item>
    </div>
  </div>
</template>
<script>
import NavBarItem from "components/NavBarItem.vue";
import { layoff, layout } from "api/user";

export default {
  name: "NavBar",
  components: {
    NavBarItem,
  },
  data() {
    return {
      showButtons: false,
      search: "",
      avatarUrl: "",
      show: false,
      identity: "",
      username: "",
    };
  },
  computed: {
  identity() {
    if (this.$store.getters.getIdentity == 1) {
      return "管理员";
    } else if (this.$store.getters.getIdentity == 0) {
      return "普通用户";
    } else {
      return "超级管理员";
    }
  },
},
watch: {
  '$store.getters.getUser': {
    immediate: true,
    handler(newValue, oldValue) {
      this.username = this.$store.getters.getUser;
      if (this.$store.getters.getIdentity==1) {
        this.identity = "管理员";
      } else if(this.$store.getters.getIdentity==0) {
        this.identity = "普通用户";
      } else{
        this.identity = "超级管理员";
      }
    }
  }
},
  methods: {
    layout() {
      this.$store.commit("clearUser");
      this.$message.success("退出成功");
      this.$router.replace("/login");
    },
    layoff() {
      this.$alert("确定要注销您的账号吗？", "提示", {
        confirmButtonText: "确定",
        callback: (action) => {
          if (action == "confirm") {
            layout().then((res) => {
              if (res.status == 200) {
                this.$store.commit("clearUser");
                this.$message.success("注销成功");
                this.$router.replace("/login");
              }
            });
          }
        },
      });
    },
  },
};
</script>
<style scoped>
* {
  padding: 0;
  margin: 0;
  text-decoration: none;
}

body {
  justify-content: space-evenly;
  align-items: center;
}

.nav-content {
  display: flex;
  overflow: hidden;
}
.nav-bar {
  display: flex;
  flex-direction: column;
  transition: 0.3s;
  overflow: hidden;
  position: fixed;
  top: 50px;
  height: 93%;
  width: 270px;
  background-color: #f8fafc;
  padding-top: 50px;
}
.navname {
  border-radius: 7px;
  font-family: bold;
  display: block;
  height: 50px;
  position: relative;
  transition: 0.3s;
  line-height: 50px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 15px;
}

.navname span {
  position: relative;
  left: 60px;
  opacity: 1;
  transition: 0.1s;
}

.iconfont {
  position: absolute;
  margin: 0px 10px 0 0px;
}

.nav-bar:hover {
  width: 280px;
}

.nav-bar:hover span {
  opacity: 1;
}

.navname:hover {
  background-color: #e0e7ff;
  box-shadow: 0 0 5px rgba(52, 52, 205, 0.1);
  color: #4338ca;
  scale: 1.02;
}

.nav-bar {
  padding: 8px 12px;
}

.nav_content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
}

.sidebar-icon {
  margin: 5%;
}

.navname span.text {
  left: 40px;
}

.bottom {
  margin-top: auto;
}

.full-size {
  width: 100%;
  height: 100%;
}

.el-dropdown-item {
  width: 250px;
  height: 50px;
}

.el-dropdown-item:hover {
  color: #4338ca;
  background-color: #e0e7ff;
}
</style>
