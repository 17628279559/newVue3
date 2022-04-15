import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('../views/home/home.vue')
    },
    {
        path: '/tree1',
        name: 'tree1',
        component: () => import('../views/tree1/tree1.vue')
    },
    {
        path: '/tree2',
        name: 'tree2',
        component: () => import('../views/tree2/tree2.vue')
    },
    {
        path: '/tree3',
        name: 'tree3',
        component: () => import('../views/tree3/tree3.vue')
    },
    {
        path: '/his',
        name: 'his',
        component: () => import('../views/his/his.vue')
    },
    {
        path: '/pie',
        name: 'pie',
        component: () => import('../views/pie/pie.vue')
    },
    {
        path: '/wordCloud',
        name: 'wordCloud',
        component: () => import('../views/wordCloud/wordCloud.vue')
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
