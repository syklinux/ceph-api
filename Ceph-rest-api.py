#/usr/bin/env python
# _*_ coding:utf-8 _*_

import urllib, json
import requests
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



class CephAPI(object):
	def __init__(self,url):
		self.__url = url.rstrip('/')

	def postRequest(self,obj,methond='PUT',params=None,prefix='/'):
		'''
		处理请求
		'''
		if params:
			#### python 3需要使用urllib.parse.urlencode
			# params = urllib.parse.urlencode(params)
			params = urllib.urlencode(params)
		url = self.__url + prefix + obj
		if methond == 'GET':
			content = requests.get(url,params=params)
		else:
			content = requests.put(url,params=params)
		return content.text

	def Get_Ceph_Status(self):
		'''
		ceph 集群的状态
		类似于： ceph -s
		'''
		obj = "status"
		content = self.postRequest(obj,methond='GET')
		return content

	def Get_Ceph_Version(self):
		'''
		ceph 版本信息
		'''
		obj = "version"
		content = self.postRequest(obj,methond='GET')
		return content


	def Get_Auth_List(self):
		'''
		列出所有认证信息
		'''
		obj = "auth/list"
		content = self.postRequest(obj,methond='GET')
		return content


	def Add_auth(self,entity,caps=None):
		'''
		为特定实体增加认证信息,如有则返回已有的认证信息
		caps为指定密钥，为空则随机生成
		'''
		obj = "auth/get-or-create"
		if caps:
			params = {'entity':entity,'caps':caps}
		else:
			params = {'entity':entity}
		content = self.postRequest(obj,params=params)
		return content

	def Delete_Auth(self,entity):
		'''
		删除指定的实体的认证信息
		'''
		obj = "auth/del"
		params = {'entity':entity}
		content = self.postRequest(obj,params=params)
		return "{} has delete successed".format(entity)

	def Update_Auth(self,entity,caps):
		'''
		更新指定实体的caps信息
		'''
		obj = "auth/caps"
		params = {'entity':entity,'caps':caps}
		content = self.postRequest(obj,params=params)
		return content


	def Get_Pool_List(self):
		'''
		列出所有pool的详细信息
		'''
		obj = "osd/pool/ls"
		params = {'detail':'detail'}
		content = self.postRequest(obj,methond='GET',params=params)
		return content

	def Get_Pool_Stats(self,poolname):
		'''
		列出pool的状态
		'''
		obj = "osd/pool/stats"
		params = {'name':poolname}
		content = self.postRequest(obj,methond='GET',params=params)
		return content

	def Rename_Pool(self,srcpoolname,destpoolname):
		'''
		修改pool的名字
		'''
		obj = "osd/pool/rename"
		params = {'srcpool':srcpoolname,'destpool':destpoolname}
		content = self.postRequest(obj,params=params)
		return "pool {} has rename {}".format(srcpoolname,destpoolname)



a = CephAPI('http://10.1.0.229:5000/api/v0.1/')
# print a.Get_Ceph_Version()
# print a.Add_auth(entity='client.test1')
# print a.Delete_Auth(entity='client.test1')
# print a.Get_Ceph_Status()
# print a.Rename_Pool(srcpoolname='test',destpoolname='test2')
