# Docker  官网 & 尚硅谷2022版



## 命令行

```shell
docker images [image]				# 列出镜像
docker search --limit <n> <image>	# 查找前n条镜像
docker pull <image[:tag]>			# tag默认为latest
docker rmi <image>					# 删除镜像

docker run -p <主机端口>:<容器端口> --name <name> -it -d <image>	# i:interactive, t:terminal, d:detach(后台)  本机没有镜像时从仓库寻找后生成容器
docker exec <container> /bin/bash	# 进入未停止的容器，不会启动新的终端
exit								# 停止并退出容器，配合exec
docker attach <container>			# 进入未停止的容器，会启动新的终端
ctrl+p+q							# 退出容器但继续运行，配合attach

docker start <container>			# 进入已停止的容器
docker restart <container>
docker stop <container>
docker kill <container>

docker ps -aql						# 查看所有容器+只显示ID号+最新的一个容器
docker rm -f $(docker ps -aq)		# 强制删除所有容器
docker ps -aq | xargs docker rm 	# 同上

# volume mounts
docker volume create <volume>		# 创建容器卷
docker volume ls					# 列出所有
docker volume inspect <volume>		# 查看内部细节
docker volume rm <volume>			# 删除
docker run <image> --mount type=volume,src=<volume>,target=<dst>

# bind mounts
docker run -it --mount type=bind,src=<local_dir>,target=<docker_dir> ubuntu bash
docker run -dp 3000:3000 -w /app --mount "type=bind,src=$pwd,target=/app" node:18-alpine sh -c "yarn install && yarn run dev"	# 无需编译就可以改app内容

docker logs <container>
docker top <container>				# 查看容器内部进程
docker inspect <container>/<image>	# 查看内部细节
docker system df					# 查看各部分内存

docker cp <container>:<path> <path>	# 从容器中复制文件到主机
docker export <container> > <file>.tar									# 导出镜像
cat <file>.tar | docker import - <镜像用户>/<镜像名>:<镜像版本号>			# 导入镜像
docker commit -m "<info>" -a "<author>" <镜像用户>/<镜像名>:<镜像版本号>	# 创建镜像

docker login --username=hty0111 registry.cn-hangzhou.aliyuncs.com
docker pull registry.cn-hangzhou.aliyuncs.com/hty_learning_docker/ubuntu:<镜像版本号>	# 拉取镜像
docker tag <image> registry.cn-hangzhou.aliyuncs.com/<命名空间>/<仓库名称>:<镜像版本号>		# src->dst
docker push registry.cn-hangzhou.aliyuncs.com/<命名空间>/<仓库名称>:<镜像版本号>

docker run -d -p 5000:5000 -v <主机路径>:<容器路径> --privileged=true registry				# 运行私有库
docker tag <仓库名称>:<镜像版本号> localhost:5000/<仓库名称>:<镜像版本号>
docker push/pull localhost:5000/<仓库名称>:<镜像版本号>
```



## Dockerfile

### 解析器指令（parser directives）

- 格式：`# directive=value`
- 文件开头
- 不能有换行符
- 不能重复
- 大小写不敏感
- 可以有空格
- **不适用于`RUN`命令**

#### 转义字符（escape）

​		转义字符的作用转义或换行，是默认是`\`，但Windows中目录的分隔符也是`\`，所以在行末出现`C:\\`时，第二个`\`会被认为是换行符，而不是被转义后目录分隔符，因此一般设置转义字符为`` `。

```dockerfile
# escape=` (backtick)
```



### .dockerignore

​		语法跟`.gitignore`一样，在构建到守护进程时忽略文件。



### 语法

#### FROM

- 初始化一个 build stage
- 设置 base image

```dockerfile
FROM [--platform=<platform>] <image>[:tag]/[@<digest>] [AS <name>]
# tag: latest(default)
# platform: linux/amd64, linux/arm64, windows/amd64
```

#### RUN

- 在当前镜像的最上方生成一个新的层

```dockerfile
# (1) shell form
RUN <command>	# run a shell, '/bin/sh -c' on Linux or 'cmd /S /C' on Windows
# example
RUN /bin/bash -c 'source $HOME/.bashrc && echo $HOME'

# (2) exec form
RUN ["executable", "param1", "param2"]	# parsed as JSON array, so using "" rather ''
# example
RUN ["/bin/bash", "-c", "echo hello"]
```

#### CMD

- 一个Dockerfile中只能出现一次，最后出现的CMD生效

```dockerfile
# (1) exec form, preferred
CMD ["executable", "param1", "param2"]

# (2) as default parameters to ENTRYPOINT
CMD ["param1", "param2"]

# (3) shell form
CMD command param1 param2
```

#### LABEL

- 添加 metadata
- 可被镜像继承或重载

```dockerfile
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

#### EXPOSE

- 设置运行时特定的监听端口和协议

```dockerfile
EXPOSE <port> [<port>/<protocol>...]	# default by TCP
```

#### ENV

- 定义：`ENV foo=/bar`
- 引用：`${foo}, $foo, ${foo}_bar, \${foo}, \&foo`

```dockerfile
ENV abc=hello
ENV abc=bye def=$abc	# def=hello
ENV ghi=$abc			# ghi=bye
```

#### ADD & COPY

- 将主机上的资源复制或加入到容器镜像中
- `ADD`支持通过URL从远程服务器读取资源，但是建议用`RUN curl`

```dockerfile
ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>
ADD [--chown=<user>:<group>] [--chmod=<perms>] ["<src>",... "<dest>"]	# for paths containing whitespace

COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>
COPY [--chown=<user>:<group>] [--chmod=<perms>] ["<src>",... "<dest>"]	# for paths containing whitespace
```


