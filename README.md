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
1. 为pyreBloom增加scalable bloom filter功能
2. 手动管理bloom filter dump file，避免bloom filter使用内存一直增加
