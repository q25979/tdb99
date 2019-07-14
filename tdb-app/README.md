# 环境依赖
>node
```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
# 重开 Terminal
nvm install node
nvm alias default node
```

>webpack
```bash
npm install -g webpack
```

# 运行

```bash
npm install
npm run dev
```

# 组件规则
  props data 钩子函数 computed watch methods components

# 目录结构
```
build                   build 脚本
config                  配置
dist                    打包目标目录
src                     源码
    app                 客户端代码
        apollo          apollo 客户端配置
        assets          资源文件
        components      vue 组件
        data            graphql 查询定义文件
        router          路由定义
        main.js         入口
    server              服务端代码
        app.js          express 初始化
        graphql         graphql 服务端
            api         api 调用封装
            data        api 结果组装
            types       graphql 类型定义
            schema      graphql 接口导出
index.html              入口 html
```
# 资料
* [Vue Apollo](https://github.com/Akryum/vue-apollo)
* [GraphQL](http://graphql.org/learn/)
* [Vue Router](https://github.com/vuejs/vue-router)
* [ES6](http://es6-features.org/)
