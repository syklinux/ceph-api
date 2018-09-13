#/usr/bin/env python
# _*_ coding:utf-8 _*_

import rados,sys


class CephAPI(object):
    def __init__(self,conffile):
        self._conffile = conffile
        self.cluster = self.connect()

    def connect(self):
        cluster = rados.Rados(conffile=self._conffile)
        cluster.connect()
        return cluster

    def Ceph_info(self):
    	ceph_info = {}
    	ceph_id = self.cluster.get_fsid()
    	ceph_status = self.Get_Ceph_Stats()
    	ceph_pools = self.Get_Ceph_Pools()
    	ceph_info["ceph_id"]=ceph_id
    	ceph_info["ceph_status"]=ceph_status
    	ceph_info["ceph_pools"]=ceph_pools
    	return ceph_info
    	
    def Get_Ceph_Stats(self):
    	'''
		获取ceph统计数据
    	'''
    	return self.cluster.get_cluster_stats()

    def Get_Ceph_Pools(self):
    	'''
		获取所有的pool
    	'''
    	return self.cluster.list_pools()

    def Creat_Ceph_Pools(self,name):
    	'''
		新建pool
    	'''
    	pools = self.Get_Ceph_Pools()
    	if name in pools:
    		return "error creating pool '%s'"%(name)
    	else:
    		try:
    			self.cluster.create_pool(name):
    			return "pool '%s' create successed"%(name)
    		except Exception as e:
    			return e

    def Delete_Ceph_Pools(self,name):
   	'''
	删除pool
   	'''
        pools = self.Get_Ceph_Pools()
   	if name not in pools:
   		return "error deleting pool '%s'"%(name)
   	else:
   		try:
    		self.cluster.delete_pool(name):
    		return "pool '%s' delete successed"%(name)
    	except Exception as e:
    		return e

    def Get_Pool_FileList(self,name):
    	'''
		获取pool下的文件列表
    	'''
    	file_list = []
        try:
            ioctx = self.cluster.open_ioctx(name)
            object_list = ioctx.list_objects()
            while True:
                try:
                    rados_object = object_list.next()
                    file_list.append(rados_object.key)
                except StopIteration :
                    break
            return file_list
        except Exception as e:
                return e

    def Get_Pool_Key_Context(self,*args):
    	poolname,keyname = args[0],args[1]
    	key_list = self.Get_Pool_FileList(poolname)
    	if Keyname not in key_list:
    		return "key '%s' not created"%(Keyname)
    	try:
    		ioctx = self.cluster.open_ioctx(poolname)
            object_list = ioctx.list_objects()
            while True:
                try:
                    rados_object = object_list.next()
                    if rados_object.key == Keyname:
                    	return rados_object.read()
                except StopIteration :
                    break
        except Exception as e:
                return e


a = CephAPI('/home/ceph/ceph-cluster/ceph.conf')
print a.Get_Pool_FileList('test')
