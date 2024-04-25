<template>
  <div class="root">
    <div class="body">
      <div class="bg"></div>
      <div
        class="container"
        :class="{ 'right-panel-active': isRightPanelActive }"
      >
        <!-- Sign In -->
        <div class="container__form container--signin">
          <form action="#" class="form" id="form2">
            <h2 class="form__title">Sign In</h2>
            <input
              type="email"
              v-model="email"
              placeholder="Email"
              class="input"
            />
            <input
              type="password"
              v-model="password"
              placeholder="Password"
              class="input"
            />
            <button class="btn" @click="login">sign in</button>
            <div class="link">
              New here? <a class="linka" href="#" @click="goSignUp">Sign Up</a>
            </div>
            <!-- <a href="#" class="link">Forgot your password?</a> -->
          </form>
        </div>

        <!-- Sign Up -->
        <div class="container__form container--signup" v-if="showSignup">
          <form action="#" class="form" id="form1">
            <h2 class="form__title">Sign Up</h2>
            <input
              type="email"
              v-model="email"
              placeholder="Email"
              class="input"
            />
            <input
              type="text"
              v-model="username"
              placeholder="User Name"
              class="input"
            />
            <input
              type="password"
              v-model="password"
              placeholder="Password"
              class="input"
            />
            <input
              type="text"
              v-model="code"
              placeholder="Verification Code"
              class="input verify"
            />
            <div
              class="code el-icon-message"
              v-if="showTime === null"
              @click="sendCode"
            ></div>
            <div class="code data" v-else>{{ showTime }}</div>
            <button class="btn" @click="register">sign up</button>
            <div class="link">
              Already have an account?
              <a class="linka" href="#" @click="goSignIn">Sign In</a>
            </div>
          </form>
        </div>

        <!-- Overlay -->
        <div class="container__overlay">
          <div class="overlay">
            <div class="overlay__panel overlay--left">
              <h1 class="overlay-content">Welcome Back!</h1>
            </div>
            <div class="overlay__panel overlay--right">
              <h1 class="overlay-content">Hello, Friend!</h1>
              <p>
                Enter your personal details and start journey with knowledge
                graph
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { login, register, sendCode } from "api/user";
export default {
  name: "Login",
  components: {},
  data() {
    return {
      isRightPanelActive: true,
      showSignup: false,
      email: "",
      password: "",
      username: "",
      code: "",
      timeCounter: null, //计时器
      showTime: null, //剩余时间
      checked: false,
    };
  },
  methods: {
    goSignIn() {
      this.isRightPanelActive = true;
      this._switch();
    },

    goSignUp() {
      this.isRightPanelActive = false;
      this.showSignup = true;
      this._switch();
    },
    _switch() {
      this.email = "";
      this.password = "";
      this.username = "";
    },
    async login() {
      if (this.email == "" || this.password == "") {
        this.$message.error("请输入邮箱和密码");
        return;
      }
      const res = await login({ email: this.email, password: this.password });
      this.$store.commit("updateUser", res.data.data);
      this.$message.success("登录成功");
      this.$router.push("/main/upload");
    },
    async register() {
      if (
        this.email == "" ||
        this.password == "" ||
        this.username == "" ||
        this.code == ""
      ) {
        this.$message.error("请输入完整信息");
        return;
      }
      const res = await register({
        email: this.email,
        password: this.password,
        username: this.username,
        verificationCode: this.code,
      });
      if (res.status == 200) {
        this.login();
      }
    },
    sendCode() {
      if (this.showTime != null) {
        return;
      }
      if (this.email == "") {
        this.$message.error("请输入邮箱");
        return;
      }
      sendCode({ email: this.email }).then((res) => {
        this.$message.success("验证码已发送");
        this.countDown(300);
      });
    },
    // 倒计时显示处理
    countDownText(s) {
      this.showTime = `${s}s`;
    },
    // 倒计时60秒
    countDown(times) {
      const self = this;
      // 时间间隔 1秒
      const interval = 1000;
      let count = 0;
      self.timeCounter = setTimeout(countDownStart, interval);
      function countDownStart() {
        if (self.timeCounter == null) {
          return false;
        }
        count++;
        self.countDownText(times - count + 1);
        if (count > times) {
          clearTimeout(self.timeCounter);
          self.showTime = null;
        } else {
          self.timeCounter = setTimeout(countDownStart, interval);
        }
      }
    },
  },
};
</script>

<style scoped>
.root {
  /* COLORS */
  --white: #e9e9e9;
  --gray: #333;
  --blue: #0367a6;
  --lightblue: #008997;

  /* RADII */
  --button-radius: 0.7rem;

  /* SIZES */
  --max-width: 830px;
  --max-height: 470px;

  font-size: 16px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.body {
  position: relative;
  align-items: center;
  background-color: var(--white);
  display: grid;
  height: 100vh;
  place-items: center;
  margin: 0;
  padding: 0;
  top: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
}

.body .bg {
  transform: scale(1.2);
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url("../assets/img/background3.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  filter: blur(4px);
}

.form__title {
  font-weight: 300;
  margin: 0;
  margin-bottom: 1.25rem;
}

.link {
  color: var(--gray);
  font-size: 0.9rem;
  margin: 1.5rem 0;
  text-decoration: none;
}

.container {
  /* background-color: var(--white); */
  border-radius: var(--button-radius);
  box-shadow: 0 0.9rem 1.7rem rgba(0, 0, 0, 0.25),
    0 0.7rem 0.7rem rgba(0, 0, 0, 0.22);
  height: var(--max-height);
  max-width: var(--max-width);
  overflow: hidden;
  position: relative;
  width: 100%;
  backdrop-filter: blur(5px);
}

.container__form {
  height: 100%;
  position: absolute;
  top: 0;
  transition: all 0.6s ease-in-out;
}

.overlay-content {
  font-weight: 800;
  margin: 0;
  margin-bottom: 1.25rem;
}

.code {
  position: absolute;
  top: 248px;
  left: 338px;
  color: #4aa4ad;
  font-size: 40px;
  transform: translate(-50%);
  cursor: pointer;
}

.verify {
  margin-left: -78px !important;
  width: 75% !important;
  /* background-color: #59c2c5; */
}

.linka {
  color: rgb(60, 60, 228);
  /* 设置链接的颜色为蓝色 */
  text-decoration: underline;
  /* 添加下划线 */
}

h1 {
  font-weight: bold;
  margin: 0;
  color: var(--white);
}

p {
  color: var(--white);
  font-size: 18px;
  font-weight: 100;
  line-height: 30px;
  letter-spacing: 1px;
  margin: 17px 10px 30px;
}

.container--signup {
  left: 0;
  width: 50%;
  z-index: 2;
}

.container.right-panel-active .container--signup {
  transform: translateX(100%);
}

.container--signin {
  left: 0;
  opacity: 0;
  width: 50%;
  z-index: 1;
}

.container.right-panel-active .container--signin {
  animation: show 0.6s;
  opacity: 1;
  transform: translateX(100%);
  z-index: 5;
}

.container__overlay {
  height: 100%;
  left: 50%;
  overflow: hidden;
  position: absolute;
  top: 0;
  transition: transform 0.6s ease-in-out;
  width: 50%;
  z-index: 100;
}

.container.right-panel-active .container__overlay {
  transform: translateX(-100%);
}

.overlay {
  background-color: var(--lightblue);
  background: url("../assets/img/background3.jpg");
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 100%;
  left: -100%;
  position: relative;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
  width: 200%;
}

.container.right-panel-active .overlay {
  transform: translateX(50%);
}

.overlay__panel {
  align-items: center;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  position: absolute;
  text-align: center;
  top: 0;
  transform: translateX(0);
  transition: transform 0.6s ease-in-out;
  width: 50%;
}

.overlay--left {
  transform: translateX(-20%);
}

.container.right-panel-active .overlay--left {
  transform: translateX(0);
}

.overlay--right {
  right: 0;
  transform: translateX(0);
}

.container.right-panel-active .overlay--right {
  transform: translateX(20%);
}

.btn {
  background-color: rgb(24, 122, 146);
  border-radius: 20px;
  border: 1px solid rgb(24, 122, 146);
  color: var(--white);
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: bold;
  letter-spacing: 0.1rem;
  padding: 0.9rem 4rem;
  /* text-transform: uppercase; */
  transition: transform 80ms ease-in;
}

.form > .btn {
  margin-top: 1.5rem;
}

.btn:active {
  transform: scale(0.95);
}

.btn:focus {
  outline: none;
}

.form {
  background-color: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 0 3rem;
  height: 100%;
  text-align: center;
}

.input {
  background-color: #fff;
  display: block;
  padding: 0.6rem 0.9rem;
  font-size: 14px;
  line-height: 20px;
  /* color: #c9d1d9; */
  /* background-color: #0d1117; */
  border: 1px solid #cfe0f4;
  border-radius: 6px;
  outline: none;
  box-shadow: 0 0 transparent;
  width: 100%;
  margin-bottom: 16px;
}

@keyframes show {
  0%,
  49.99% {
    opacity: 0;
    z-index: 1;
  }

  50%,
  100% {
    opacity: 1;
    z-index: 5;
  }
}
</style>
