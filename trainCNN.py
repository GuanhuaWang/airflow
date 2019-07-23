# Sample code for triggering sagemaker session functions using airflow.

from sagemaker import get_execution_role
import sagemaker

import sys
import os
import shutil
import numpy as np

import chainer
from chainer.datasets import get_cifar10

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator 

sys.path.insert(0, '/home/ec2-user/anaconda3/envs/chainer_p36/lib/python3.6/site_packages')

def data_pre():
	train, test = get_cifar10()
	train_data = [element[0] for element in train]
	train_labels = [element[1] for element in train]
	test_data = [element[0] for element in test]
	test_labels = [element[1] for element in test]

	os.makedirs('/tmp/data/train_cifar')
	os.makedirs('/tmp/data/test_cifar')

	np.savez('/tmp/data/train_cifar/train.npz', data = train_data, labels = train_labels)
	np.savez('/tmp/data/test_cifar/test.npz', data = test_data, labels = test_labels)

def train_model():
	sagemaker_session = sagemaker.Session()
	role = get_execution_role()

	train_input = sagemaker_session.upload_data(
		path = os.path.join('/tmp','data','train_cifar'), 
		key_prefix = 'notebook/chainer_cifar/train')
	test_input = sagemaker_session.upload_data(
		path = os.path.join('/tmp','data','test_cifar'), 
		key_prefix = 'notebook/chainer_cifar/test')
	shutil.rmtree('/tmp/data')

	chainer_estimator = Chainer(
		entry_point = 'chainer_cifar_vgg_single_machine.py', 
		source_dir = "/home/ec2-user/airflow/dags/src", 
		role = role, 
		sagemaker_session = sagemaker_session, 
		train_instance_count = 1,
		train_instance_type = 'ml.p2.8xlarge',
		hyperparameters = {'epochs': 50, 'batch_size': 64})

	chainer_estimator.fit({'train': train_input, 'test': test_input})

# airflow part
args = {
	'owner': 'airflow',
	'start_date': aiflow.utils.dates.days_ago(2),
#	'provide_context': True
}

dag = DAG('GH_chainer', default_args = args, schedule_interval = None)

dataLoader_op = PythonOperator(
	task_id = 'data_prepare',
	python_callable = data_pre,
	dag = dag,
	)

trainTest_op = PythonOperator(
	task_id = 'model_train_test',
	python_callable = train_model,
	dag = dag,
	)

trainTest_op.set_upstream(dataLoader_op)