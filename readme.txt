1. 在线版是第一版，通过Flask运行在线MACE模型并保持，返回能量和力，网络速度可能成为运行瓶颈
使用方式：
激活rmlp虚拟环境
运行python server.py激活在线RMLP在线服务器
在另一个命令行运行gaussian计算任务，使用gaussian 的gjf调用runner.py

2. 本地版用了双线程的操作
使用方式：
激活rmlp虚拟环境
运行本地app
gunicorn --bind unix:/home/tangkun/tmp/flask_server.sock server:app
/home/tangkun/tmp这个路径可以自行制定，确保有读写权限
在另一个命令行运行gaussian计算任务，使用gaussian 的gjf调用runner.py


依赖库特别说明：
本地版需要安装requests_unixsocket库，采用这个命令安装：
pip install requests_unixsocket2==0.4.1 必须要这个版本

运行速度加速的方式来源于：
1. 模型在线保持
2. xyz坐标文件不本地保存而是直接通过内存上传到server
3. app会话在线保持，而不是反复开启新的会话
本地版相对于在线版快了一点点