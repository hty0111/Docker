# Docker 尚硅谷2022版

```shell
docker images [image]	# 列出镜像
docker search --limit <n> <image>	# 查找前n条镜像
docker pull <image[:tag]>	# tag默认为latest
docker rmi <image>

docker run -p <主机端口>:<容器端口> --name <name> -it -d <image>	# i:interactive，t:terminal，-d:detach(后台)  本机没有镜像时从仓库寻找后生成容器
docker exec <container> /bin/bash	# 进入未停止的容器，不会启动新的终端
exit	# 停止并退出容器，配合exec
docker attach <container>			# 进入未停止的容器，会启动新的终端
ctrl+p+q	# 退出容器但继续运行，配合attach

docker start <container>	# 进入已停止的容器
docker restart <container>
docker stop <container>
docker kill <container>

docker ps -aql	# 查看所有容器+只显示ID号+最新的一个容器
docker rm -f $(docker ps -aq)	# 强制删除所有容器
docker ps -aq | xargs docker rm # 同上

docker logs <container>
docker top <container>		# 查看容器内部进程
docker inspect <container>/<image>	# 查看内部细节
docker system df	# 查看各部分内存

docker cp <container>:<path> <path>	# 从容器中复制文件到主机
docker export <container> > <file>.tar	# 导出镜像
cat <file>.tar | docker import - <镜像用户>/<镜像名>:<镜像版本号>	# 导入镜像
docker commit -m "<info>" -a "<author>" <镜像用户>/<镜像名>:<镜像版本号>	# 创建镜像

docker login --username=hty0111 registry.cn-hangzhou.aliyuncs.com
docker pull registry.cn-hangzhou.aliyuncs.com/hty_learning_docker/ubuntu:<镜像版本号>	# 拉取镜像
docker tag <image> registry.cn-hangzhou.aliyuncs.com/<命名空间>/<仓库名称>:<镜像版本号>	# src->dst
docker push registry.cn-hangzhou.aliyuncs.com/<命名空间>/<仓库名称>:<镜像版本号>

docker run -d -p 5000:5000 -v <主机路径>:<容器路径> --privileged=true registry	# 运行私有库
docker tag <仓库名称>:<镜像版本号> localhost:5000/<仓库名称>:<镜像版本号>
docker push/pull localhost:5000/<仓库名称>:<镜像版本号>
```

