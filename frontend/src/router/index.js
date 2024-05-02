import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/SignUp.vue"),
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("../views/DashBoard.vue"),
  },
  {
    path: "/dashboard/admin",
    name: "admin",
    component: () => import("../views/AdminView.vue"),
  },
  {
    path: "/dashboard/message",
    name: "message",
    component: () => import("../views/MessageView.vue"),
    props: true,
  },
  {
    path: "/message/:recipient",
    name: "test",
    component: () => import("../views/TestingView.vue"),
    props: true,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
