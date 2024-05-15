<template>
  <div class="top-container">
    <!-- <el-dropdown class="avatar">
      <img src="https://github.githubassets.com/favicons/favicon.svg" />
      <span>{{ this.$store.getters.getUser }} ({{ identity }})</span>
      <el-dropdown-menu slot="dropdown" class="menu">
        <el-dropdown-item @click.native="layout" icon="el-icon-circle-close">
          退出登录</el-dropdown-item
        >
        <el-dropdown-item @click.native="layoff" icon="el-icon-delete"
          >&nbsp;注销账号</el-dropdown-item
        >
      </el-dropdown-menu>
    </el-dropdown> -->
    <mallki
      class-name="mallki-text username"
      text="HZAU知识工程与元学习团队"
      style="font-size: 20px"
    />
  </div>
</template>
<script>
import { layoff, layout } from "api/user";
import Mallki from "./TextHoverEffect/Mallki.vue";
export default {
  name: "TopBar",
  components: {
    Mallki,
  },
  data() {
    return {
      search: "",
      avatarUrl: "",
      show: false,
    };
  },
  computed: {
    identity() {
      if(this.$store.getters.getIdentity == 1) {
        return "管理员";
      } else if(this.$store.getters.getIdentity == 0) {
        return "普通用户";
      } else {
        return "超级管理员";
      }
    },
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
.top-container {
  width: 100%;
  height: 60px;
  background-color: #e0e7ff;
  color: #181818;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add box shadow */
  transition: transform 0.3s ease-in-out; /* Add transition */
}

.top-container:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.005);
}
.avatar {
  position: absolute;
  top: 5px;
  right: 100px;
  cursor: pointer;
  width: 120px;
  height: 50px;
  line-height: 50px;
  color: #000000;
  /* background-color: #fff; */
}
.avatar img {
  width: 50px;
  height: 50px;
}
.username {
  float: left;
  .username {
    float: left;
    margin: 20px 0 0 30px;
    color: #000000;
    font-weight: bold;
  }
  margin: 20px 0 0 30px;
}
.layout {
  float: right;
  margin: 13px 20px 0 0;
  cursor: pointer;
  color: #5e85bf;
  border-radius: 20px;
  width: 80px;
  text-align: center;
  font-size: 14px;
}
</style>
