#D-Octopus
##安装hiredis
```bash
git clone https://github.com/redis/hiredis
cd hiredis && make && sudo make install
sudo ldconfig
```

##安装pyreBloom
```bash
pip install -r requirements.txt
python setup.py install
```

##pyreBloom使用
https://github.com/seomoz/pyreBloom


##TODO
1. 为pyreBloom增加[scalable bloom filter](http://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf)功能
2. 手动管理[bloom filter dump file](https://github.com/seomoz/pyreBloom)，避免bloom filter使用内存一直增加
3. 添加js加载支持
4. 解决任务状态追踪问题（storm，异或）
5. 任务优先级
6. 单点问题
