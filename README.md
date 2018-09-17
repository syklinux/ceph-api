#### Ceph-api 是使用了rados模块写的，需要依赖服务器的ceph，
# ceph-api

### ceph的python接口，刚开始写，慢慢更新。


#### Ceph-api 是使用了rados模块写的，需要依赖服务器的ceph
- yum install python-rados



#### ceph-rest-api 是使用了ceph的http-api
- 使用(ceph-rest-api是ceph本身就带的包，直接使用就行)
    ```
     ceph-rest-api -n client.admin
    ```
  * Running on http://0.0.0.0:5000/
  会使用系统的5000端口
